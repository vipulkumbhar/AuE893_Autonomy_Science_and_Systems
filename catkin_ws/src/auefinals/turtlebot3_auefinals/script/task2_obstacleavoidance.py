#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int64
from functools import reduce
from numpy import inf
import numpy as numpy
import random

# main mission
mission_stage = 0
current_tag   = 0

# speed
#angular_speed = 0.2
#linear_vel    = 0.1

delta    = 0
f_l_dist = 0
f_r_dist = 0 
l_dist   = 0
r_dist   = 0

def wander_controller_move():
	global delta, f_l_dist,f_r_dist,l_dist,r_dist
	while not rospy.is_shutdown():
		Head_on_threshold        = 0.4
		side_obstacle_confidence = 0.7
		#print(x)
	
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
		
		angular_vel  = delta
		linear_vel   = 0.2
		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_vel))
	
		velocity_publisher.publish(vel_msg)
		rate = rospy.Rate(10)
		rate.sleep()
		rospy.loginfo('Obstacle avoidance mode')

def callback(data):
	global f_l_dist,f_r_dist,l_dist,r_dist
	x  = list(data.ranges)
	f_l      = numpy.array(x[0:30])
	f_l[f_l  == inf] = 3.5
	f_l_dist = sum(f_l)/len(f_l)

	f_r      = numpy.array(x[330:360])
	f_r[f_r  == inf] = 3.5
	f_r_dist = sum(f_r)/len(f_r)

	l      = numpy.array(x[30:90])
	l[l    == inf] = 3.5
	l_dist = sum(l)/len(l)

	r = numpy.array(x[270:330])
	r[r == inf] = 3.5
	r_dist = sum(r)/len(r)	
		
def callback_mission_stage(msg):
    global mission_stage
    mission_stage =  msg.data

def callback_current_tag(msg):
    global current_tag
    current_tag =  msg.data 

if __name__ == '__main__':
	try:
		rospy.init_node('wander_control', anonymous=True)
		sub_status = rospy.Subscriber("/mission_stage", Int64, callback_mission_stage)
		sub_tag    = rospy.Subscriber("/current_tag", Int64, callback_current_tag)
		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=3)
		scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
		
		#Testing our function
		while not rospy.is_shutdown():
			wander_controller_move()
				
		velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))

	except rospy.ROSInterruptException: pass



























