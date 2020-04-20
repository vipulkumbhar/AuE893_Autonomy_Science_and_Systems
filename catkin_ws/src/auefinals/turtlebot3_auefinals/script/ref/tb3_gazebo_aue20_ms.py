#!/usr/bin/env python
# license removed for brevity
import rospy
import math
import numpy
from numpy import inf
import random
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from subprocess import call
import time
from people_msgs.msg import PositionMeasurementArray

delta = 0
linear_speed = 0.20
#k_p = 0.70325
k_p = 0.8
cvbridge = CvBridge()
under_camera_control=0
stopped = False
already_stopped_once = False
following_person = False


def leg_detector_callback(data):
	if under_camera_control==0 and already_stopped_once:
		global delta, following_person, linear_speed
		# if len(data.people)>0:
		# 	global delta, following_person, linear_speed
		# 	for person in data.people:
		# 		person_x_dist = data.person.pos.x
		# 		person_y_dist = data.person.pos.y
		# 		if person_x_dist < 0:
		# 			continue
		# 		print "Person-Following mode activated!", person_x_dist , person_y_dist
		# 		following_person = True
		# 		if person_x_dist > 1:
		# 			linear_speed = 0.20
		# 			delta  = person_y_dist
		# 		else:
		# 			linear_speed = 0
		# 			delta = 0
		# else:
		# 	following_person = False
		# 	print "Person-Following mode de-activated!"

		# if len(data.people) == 0:
		# 	following_person = False
		# 	print "Person-Following mode de-activated!"

		try:
			person_x_dist = data.people[0].pos.x
			person_y_dist = data.people[0].pos.y
		except Exception:
			following_person = False
			print "No person to follow."
			return
		print "Following person now.", person_x_dist , person_y_dist

		following_person = True
		if math.sqrt(person_x_dist*person_x_dist + person_y_dist*person_y_dist) > 0.5:
			linear_speed = 0.20
			delta  = person_y_dist
		else:
			linear_speed = 0
			delta=0

def obj_detector_callback(data):
	global delta, linear_speed, stopped, already_stopped_once
	# try:
	for box in data.bounding_boxes:
		if box.Class == "stop sign" and not already_stopped_once:
			print('STOP sign ahead')
			already_stopped_once = True
			for i in range(20,0,-5):
				linear_speed = i * 0.01
				time.sleep(1)
			stopped = True
			#delta = 0
			time.sleep(5)
			stopped = False
			for i in range(0,20,5):
				linear_speed = i * 0.01
				time.sleep(1)
			# rospy.loginfo("Xmin: {}, Xmax: {} Ymin: {}, Ymax: {}".format(box.xmin, box.xmax, box.ymin, box.ymax)
	# except e:
	# 	return


def camera_callback(data):
	global cvbridge,delta,under_camera_control,stopped
	cv_image = cvbridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

	# We get image dimensions and crop the parts of the image we dont need
	height, width, channels = cv_image.shape
	crop_img = cv_image[(height)/2+100:(height)/2+120][1:width]

	# Convert from RGB to HSV
	hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

	# Define the Yellow Colour in HSV

	"""
	To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
	"""

	# Threshold the HSV image to get only yellow colors
	lower_yellow = numpy.array([20,100,100])
	upper_yellow = numpy.array([50,255,255])
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

	# Calculate centroid of the blob of binary image using ImageMoments
	m = cv2.moments(mask, False)

	try:
	    cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
	    
	except ZeroDivisionError:
		under_camera_control = 0
		return
	    #cx, cy = width/2, height/2
	under_camera_control += 1
	# if under_camera_control == 1: #Yellow line detection for the first time
	# 	start_object_detection(ob_d_cb)
		
	# Draw the centroid in the resultut image
	# cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
	# cv2.circle(mask,(int(cx), int(cy)), 10,(0,0,255),-1)

	cv2.imshow("Original", cv_image)
	# cv2.imshow("MASK", mask)
	cv2.waitKey(1)

	# Controller
	# self.move_robot(Twist(Vector3(0.3,0,0),Vector3(0,0,0))) # Should not do any publishing
	# in a callback function becuase that executes in a separate thread!
	raw_delta = width/2 -cx
	if not stopped:
		delta =  0.01* raw_delta if  raw_delta < -2 or raw_delta > 2 else 0
	#self.delta =  cy
	#print self.delta


# def start_object_detection(ob_d_cb):
# 	ob_d_cb()

# def ob_d_cb():
# 	#call(['xterm', '-e', 'roslaunch darknet_ros darknet_ros.launch'])
# 	call('roslaunch darknet_ros darknet_ros.launch')

def callback(data):
	if under_camera_control==0 and not following_person: #Not under cam control
		global delta
		#Higher values of the the parameters below allow for higher speeds in the death arena
		#Lower value of head on threshold indicates more confidence in driving ability
		Head_on_threshold = 0.4
		side_obstacle_confidence = 0.7
		#rospy.loginfo(rospy.get_caller_id(), data.ranges)
		x = list(data.ranges)

		f_l = numpy.array(x[0:30])
		f_l[f_l == inf] = 3.5
		f_l_dist = sum(f_l)/len(f_l)

		
		f_r = numpy.array(x[330:360])
		f_r[f_r == inf] = 3.5
		f_r_dist = sum(f_r)/len(f_r)

		l = numpy.array(x[30:90])
		l[l == inf] = 3.5
		l_dist = sum(l)/len(l)

		r = numpy.array(x[270:330])
		r[r == inf] = 3.5
		r_dist = sum(r)/len(r)

		
		delta = l_dist - r_dist

		if min(f_l_dist, f_r_dist) < 3.5: # obstacle ahread
			print "f_l_dist: %.2f f_r_dist: %.2f delta: %.2f" %(f_l_dist,f_r_dist,delta),
			approach  = f_l_dist - f_r_dist
			
			if approach > 1: # Obstacle on the right
				delta = min(3.5,delta + 1/f_r_dist)
			elif approach < -1: #Obstacle on the left
				delta = max(-3.5, delta - 1/f_l_dist)
			else: #Head-on
				
				# delta = random.choice([min(3.5, fwd_wt/f_l_dist), max(-3.5,-1 * fwd_wt/f_l_dist)]) #f_l_dist is the same as f_r_dist
				#Don't over react if the head on collision is not imminent

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
	rate = rospy.Rate(5) # 10hz
	image_sub = rospy.Subscriber("/camera/image",Image, camera_callback)
	obj_detector_sub = rospy.Subscriber("/darknet_ros/bounding_boxes",BoundingBoxes, obj_detector_callback)
	leg_tracker_sub = rospy.Subscriber("/people_tracker_measurements",PositionMeasurementArray, leg_detector_callback)
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
		#Testing our function
		p_controller()
	except rospy.ROSInterruptException: pass
