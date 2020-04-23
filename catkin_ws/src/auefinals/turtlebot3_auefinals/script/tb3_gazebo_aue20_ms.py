#!/usr/bin/env python

import cv2
import math
import time
import rospy
import numpy
import random
from numpy import inf
from subprocess import call
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg  import Twist, Vector3
from darknet_ros_msgs.msg import BoundingBoxes
from people_msgs.msg import PositionMeasurementArray

rospy.loginfo('tb3_gazebo_aue20_ms node started')
rospy.loginfo('wait for other processes to finish - start')
time.sleep(15)
rospy.loginfo('wait for other processes to finish - end')

delta        = 0
linear_speed = 0.20
k_p          = 0.8
cvbridge     = CvBridge()
stopped      = False
under_camera_control  = 0
already_stopped_once  = False
following_person      = False
person_in_camera_view = False
person_absconding     = 0

# How the code works?
# ---------------------
# The objective of the robot is to avoid collisions with two exceptions:
#  - Following a yellow line - Think of this as a no-obstacle highway
#  - Following a person. Note: If a person is not detected for 10 seconds 
# after initial detection, it will treat the person as an obstacle and resume obstacle avoidance.
# 
#  An added nuance is that it will stop at a Stop Sign once, meaning that if it
#  encounters the same/different stop sign again, it will ignore it.(Was coded for a 
#  given scenario and don't want to make any changes that jeopardize the code before demo!)

def leg_detector_callback(data):
	global delta, following_person, linear_speed, person_in_camera_view, person_absconding

	if under_camera_control==0 and already_stopped_once and person_in_camera_view:

		try:
			person_x_dist = data.people[0].pos.x
			person_y_dist = data.people[0].pos.y

		except Exception:
			print "No person to follow."
			if person_absconding == 0:
				print "Iniating obstacle avoidance in 10 sec"
				time.sleep(1)
				person_absconding  = 1
				return
			elif 0 < person_absconding < 10:
				print "Time remaining: %d seconds" %(10 - person_absconding)
				time.sleep(1)
				person_absconding += 1
				return
			else:
				following_person = False
				person_in_camera_view = False
				print "Avoiding obstacles."
				linear_speed = 0.20
				return
		
		print "Following person now.", person_x_dist , person_y_dist

		following_person     = True
		person_absconding    = 0
		if math.sqrt(person_x_dist*person_x_dist + person_y_dist*person_y_dist) > 0.5:
			linear_speed = 0.20
			delta        = person_y_dist

		if math.sqrt(person_x_dist*person_x_dist + person_y_dist*person_y_dist) < 0.3:
			linear_speed = -0.20
			delta        = person_y_dist
		else:
			linear_speed = 0
			delta        = 0

def obj_detector_callback(data):
	global delta, linear_speed, stopped, already_stopped_once, person_in_camera_view
	
	for box in data.bounding_boxes:

		if box.Class == "stop sign" and not already_stopped_once:
			print('STOP sign ahead')

			for i in range(20,-5,-5):
				linear_speed = i * 0.01
				time.sleep(1)
			stopped = True
			print('Stopped for stop sign')
			
			time.sleep(5)
			print('Starting movement after stop sign')
			stopped = False
			already_stopped_once = True

			for i in range(0,25,5):
				linear_speed = i * 0.01
				time.sleep(1)

		elif box.Class == "person":
			print('Person in camera view.')
			person_in_camera_view = True


def camera_callback(data):
	global cvbridge,delta,under_camera_control,stopped
	cv_image = cvbridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

	# We get image dimensions and crop the parts of the image we dont need
	height, width, channels = cv_image.shape
	crop_img = cv_image[(height)/2+100:(height)/2+120][1:width]

	# Convert from RGB to HSV
	hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

	# Define the Yellow Colour in HSV

	# Threshold the HSV image to get only yellow colors
	lower_yellow = numpy.array([20,100,100])
	upper_yellow = numpy.array([50,255,255])
	mask         = cv2.inRange(hsv, lower_yellow, upper_yellow)

	# Calculate centroid of the blob of binary image using ImageMoments
	m = cv2.moments(mask, False)

	try:
	    cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
	    
	except ZeroDivisionError:
		under_camera_control = 0
		return
	    #cx, cy = width/2, height/2
	under_camera_control += 1
	
	cv2.imshow("Original", cv_image)
	# cv2.imshow("MASK", mask)
	cv2.waitKey(1)

	# Controller
	# self.move_robot(Twist(Vector3(0.3,0,0),Vector3(0,0,0))) # Should not do any publishing
	# in a callback function becuase that executes in a separate thread!

	raw_delta = width/2 -cx
	if not stopped:
		delta =  0.01* raw_delta if  raw_delta < -2 or raw_delta > 2 else 0
	else:
		delta = 0

def callback(data):
	if under_camera_control==0 and not following_person: #Not under cam control

		global delta

		#Higher values of the the parameters below allow for higher speeds in the death arena
		#Lower value of head on threshold indicates more confidence in driving ability
		Head_on_threshold        = 0.4
		side_obstacle_confidence = 0.7
		#rospy.loginfo(rospy.get_caller_id(), data.ranges)

		x        = list(data.ranges)

		f_l = numpy.array(x[0:30])
		f_l[f_l == inf] = 3.5
		f_l_dist = sum(f_l)/len(f_l)

		
		f_r      = numpy.array(x[330:360])
		f_r[f_r == inf] = 3.5
		f_r_dist = sum(f_r)/len(f_r)

		l        = numpy.array(x[30:90])
		l[l     == inf] = 3.5
		l_dist   = sum(l)/len(l)

		r        = numpy.array(x[270:330])
		r[r     == inf] = 3.5
		r_dist   = sum(r)/len(r)

		delta    = l_dist - r_dist

		if min(f_l_dist, f_r_dist) < 3.5: # obstacle ahread

			print "f_l_dist: %.2f f_r_dist: %.2f delta: %.2f" %(f_l_dist,f_r_dist,delta),
			approach  = f_l_dist - f_r_dist
			
			if approach > 1: # Obstacle on the right
				delta = min(3.5,delta + 1/f_r_dist)

			elif approach < -1: #Obstacle on the left
				delta = max(-3.5, delta - 1/f_l_dist)

			else: #Head-on
				
				# delta = random.choice([min(3.5, fwd_wt/f_l_dist), max(-3.5,-1 * fwd_wt/f_l_dist)]) #f_l_dist is the same as f_r_dist
				# Don't over react if the head on collision is not imminent

				if min(f_l_dist,f_r_dist)<Head_on_threshold: #imminent collision
					print "Alert!!!!",	
					if -1*side_obstacle_confidence<delta<side_obstacle_confidence: #No danger of side collision
						print "Delta ignored" ,
						if f_l_dist < f_r_dist:
							delta = -3.5
						elif f_l_dist > f_r_dist:
							delta = +3.5
						else:
							delta = random.choice([-3.5,3.5]) 
					else:
						delta = numpy.sign(delta) * 3.5 #side collision danger


def p_controller():

	global delta
	global linear_speed
	global k_p

	#Setup
	rospy.init_node('p_control', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
	image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image, camera_callback)
	obj_detector_sub = rospy.Subscriber("/darknet_ros/bounding_boxes",BoundingBoxes, obj_detector_callback)
	leg_tracker_sub = rospy.Subscriber("/people_tracker_measurements",PositionMeasurementArray, leg_detector_callback, queue_size=1)
	rate = rospy.Rate(5)

	while not rospy.is_shutdown():
		vel_msg = Twist(Vector3(linear_speed,0,0), Vector3(0,0,delta*k_p))
		print "Control: %.2f" %(delta)
		#Burger's max translational velocity = 0.22m/s
		#Burger's max rotational velocity = 2.84rad/s
		# rospy.loginfo(vel_msg)
		velocity_publisher.publish(vel_msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		p_controller()
	except rospy.ROSInterruptException: pass
