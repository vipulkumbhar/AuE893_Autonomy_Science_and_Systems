#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
import numpy as np
from numpy import inf
import random

front_range = 20
front_limit = 1
move_flag   = 1
kp  = 2
y_l = 0
l_l = 0
r_l = 0
fast = 4
y_b = 0

def callback(data):
	global y_l, front_range, front_limit,l_l,r_l,y_b
	x  = list(data.ranges)
	y_l= min(min(x[0:front_range/2],x[360-front_range/2:359]))
	
	l_l = min(x[10:50])
	r_l = min(x[310:350])
	y_b = min(x[165:195])

def wander_controller_move():
	global y_l,front_limit,l_l,r_l,fast
	while not rospy.is_shutdown():

		#linear_vel = np.clip((y_l-front_limit-0.2)/5,0,0.3)
		linear_vel = 0.2*fast

		angular_vel_add1 = 0
		angular_vel_add2 = 0
		
		if l_l < 0.5:
			angular_vel_add1 = -0.15

		if r_l < 0.5:
			angular_vel_add2 = 0.15

		angular_vel = (0 + angular_vel_add1 + angular_vel_add2)*fast

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
	global y_l,fast, y_b
	v = random.randint(1,101)
	while not rospy.is_shutdown():
                turn = 0

		if v > 40:
			turn = -1
		if v < 40:
			turn = 1

                angular_vel = 0.2*turn*fast

		linear_vel = np.clip((y_l - 0.4),0,0.2)  

		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_vel))
		velocity_publisher.publish(vel_msg)
		print('rotating turtlebot with angular speed =',format(angular_vel))
		print('rotating turtlebot with speed =',format(linear_vel))
		print('distance from front obstacle =',format(y_l))
		print('distance from back obstacle =',format(y_b))
		rate.sleep()

		if y_l<front_limit/4 or y_b < 0.1:
			stuck()

		if y_l>front_limit:
			break

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('moving turtlebot')
	wander_controller_move()

def stuck():
	global y_l,fast
	while not rospy.is_shutdown():

		sign =1
		if y_b < 0.1:
			sign = -1

		vel_msg = Twist(Vector3(-0.1*sign,0,0), Vector3(0,0,0))
		velocity_publisher.publish(vel_msg)
		print('oops')
		rate.sleep()

		if y_l > 0.4 and y_b > 0.1:
			break
	
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))	
	wander_controller_rotate()

if __name__ == '__main__':
	try:
		rospy.init_node('wander_control', anonymous=True)
		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
		rate = rospy.Rate(20) # 20hz

		#Testing our function
		wander_controller_move()
	except rospy.ROSInterruptException: pass



























