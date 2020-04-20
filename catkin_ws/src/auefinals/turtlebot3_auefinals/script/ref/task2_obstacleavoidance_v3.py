#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int64
from functools import reduce
from numpy import inf
import numpy as np
import random

# main mission
mission_stage = 0
current_tag   = 0

# distances
f_d  = 0
l_d  = 0
r_d  = 0
b_d  = 0
xmin = 0
fl_d = 0
fr_d = 0

# distance limits
front_limit   = 0.2
side_limit    = 0.25

# speed
angular_speed = 0.2
linear_vel    = 0.1

def callback(data):
	global f_d,l_d,r_d,b_d,xmin
	x  = list(data.ranges)

	for i in range(360):
		if x[i] == inf:
			x[i] = 7
		if x[i] == 0:
			x[i] = 6

	f_d   = min(min(x[0:15],x[360-15:359])) # front distance
	l_d   = min(x[10:50])                   # left  distance
	r_d   = min(x[310:350])                 # right distance
	b_d   = min(x[165:195])                 # back  distance

	xmin  = min(x[1:359])
	fl_d  = min(x[30:120])
	fr_d  = min(x[360-120:360-30]) 

	print('all distance',format(f_d),' ',format(l_d),' ',format(r_d),' ',format(b_d))  

def wander_controller_move():
	global f_d,l_d,r_d,b_d,front_limit,mission_stage,side_limit,fl_d,fr_d

	while not rospy.is_shutdown():
		rospy.loginfo('move')
		linear_vel = np.clip((f_d-front_limit),-0.1,0.2)

		# turn a bit in opposite direction if object is on right or left side
		angular_vel        = 0
		angular_vel_1      = 0
		angular_vel_2      = 0

		if r_d < 0.4:
			angular_vel_1 =  0.2
 	
		if l_d < 0.4:
			angular_vel_2 = -0.2

		angular_vel = (angular_vel + angular_vel_1 + angular_vel_2)
		linear_vel  = ((0.2 - abs(angular_vel))/0.2)*linear_vel 

		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_vel))
		velocity_publisher.publish(vel_msg)

		# brake if obstacle ahead
		if f_d < front_limit: # or l_d<0.15 or r_d<0.15:
			break
		rate.sleep()

	# state transition
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('rotating turtlebot')
	wander_controller_rotate()

def wander_controller_rotate():
	global l_d,r_d,f_d,front_limit,linear_vel,mission_stage,fl_d,fr_d
	
	while not rospy.is_shutdown():
                rospy.loginfo('rotate')

                turn = 1
		if fl_d < fr_d:
			turn = -1 

		linear_vel  = np.clip((f_d - front_limit),-0.2,0.1)		
                angular_vel = 0.2*turn*(linear_vel/abs(linear_vel))

		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_vel))

		if f_d>1.3*front_limit:
			break
		rate.sleep()

	# state transition 2
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	wander_controller_move()
		
def callback_mission_stage(msg):
    global mission_stage
    mission_stage =  msg.data

def callback_current_tag(msg):
    global current_tag
    current_tag =  msg.data 

if __name__ == '__main__':
	try:
		rospy.init_node('wander_control', anonymous=True)
		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=3)
		scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
		sub_status = rospy.Subscriber("/mission_stage", Int64, callback_mission_stage)
		sub_tag    = rospy.Subscriber("/current_tag", Int64, callback_current_tag)
		rate = rospy.Rate(10)

		#Testing our function
		wander_controller_move()

	except rospy.ROSInterruptException: pass



























