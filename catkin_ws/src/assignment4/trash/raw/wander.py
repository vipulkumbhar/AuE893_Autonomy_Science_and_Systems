#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
import numpy as np
from numpy import inf
import random

front_range = 20
front_limit = 0.6
move_flag   = 1
kp  = 2
y_l = 0
l_l = 0
r_l = 0

def callback(data):
	global y_l, front_range, front_limit,l_l,r_l
	x  = list(data.ranges)
	y_l= min(min(x[0:front_range/2],x[360-front_range/2:359]))
	
	l_l = min(x[30:60])
	r_l = min(x[300:330])

def wander_controller_move():
	global y_l,front_limit,l_l,r_l
	while not rospy.is_shutdown():

		#linear_vel = np.clip((y_l-front_limit-0.2)/5,0,0.3)
		linear_vel = 0.2

		angular_vel_add1 = 0
		angular_vel_add2 = 0
		
		if l_l < 0.5:
			angular_vel_add1 = -0.05

		if r_l < 0.5:
			angular_vel_add2 = 0.05

		angular_vel = 0 + angular_vel_add1 + angular_vel_add2

		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_vel))
		velocity_publisher.publish(vel_msg)

		print('moving turtlebot with speed =',format(linear_vel))
		print('distance from front obstacle =',format(y_l))
		rate.sleep()

		if y_l < front_limit:
			break

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('rotating turtlebot')
	wander_controller_rotate()

def wander_controller_rotate():
	global y_l
	vip = random.randint(1,101)
	while not rospy.is_shutdown():
		if vip > 50:
			turn = -1
		if vip < 50:
			turn = 1
                angular_vel = 0.2*turn
		vel_msg = Twist(Vector3(0,0,0), Vector3(0,0,angular_vel))
		velocity_publisher.publish(vel_msg)
		print('rotating turtlebot with speed =',format(angular_vel))
		print('distance from front obstacle =',format(y_l))
		rate.sleep()

		if y_l>front_limit:
			break
 		

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('moving turtlebot')
	wander_controller_move()

if __name__ == '__main__':
	try:
		rospy.init_node('wander_control', anonymous=True)
		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
		rate = rospy.Rate(20) # 20hz

		#Testing our function
		wander_controller_move()
	except rospy.ROSInterruptException: pass
