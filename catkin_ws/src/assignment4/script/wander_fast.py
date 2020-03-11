#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
import numpy as np
from numpy import inf
import random
from functools import reduce

front_range   = 30
front_limit   = 0.5 #0.8
side_limit    = 0.3 #0.3

move_flag     = 1
linear_speed  = 0.2
angular_speed = 0.2
kp   = 2
y_l  = 0
l_l  = 0
r_l  = 0
fast = 1
y_b  = 0

def Average(lst): 
    return reduce(lambda a, b: a + b, lst) / len(lst)

def callback(data):
	global y_l, front_range, front_limit,l_l,r_l,y_b

	x  = list(data.ranges)
	for i in range(360):
		if x[i] == inf:
			x[i] = 7
		if x[i] == 0:
			x[i] = 6


	y_l   = min(min(x[0:front_range/2],x[360-front_range/2:359]))
	l_l   = min(x[10:50])
	r_l   = min(x[310:350])
	y_b   = min(x[165:195])

	print('all distance',format(y_l),' ',format(l_l),' ',format(r_l),' ',format(y_b))  


def wander_controller_move():
	global y_l,front_limit,l_l,r_l,fast,linear_speed,angular_speed,side_limit
	while not rospy.is_shutdown():

		linear_vel = np.clip((y_l-front_limit+0.2)/5,-0.2,0.5)
		#linear_vel = linear_speed*fast
		angular_vel_add1 = 0
		angular_vel_add2 = 0
		
		#turn a bit in opposite direction if object is on right or left side
		if l_l < side_limit:
			angular_vel_add1 = -angular_speed

		if r_l < side_limit:
			angular_vel_add2 = angular_speed
		
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
	global y_l,fast, y_b,angular_speed,linear_speed,front_limit

	v = random.randint(1,101)
	while not rospy.is_shutdown():
                turn = 0

		if v > 40:
			turn = -1
		if v < 40:
			turn = 1
		turn = 1

                angular_vel = angular_speed*turn*fast
		linear_vel  = np.clip((y_l - front_limit*2/3),-0.2,0.1)  
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
			if l_l>0.15:
				if r_l >0.15:
					break

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('moving turtlebot')
	wander_controller_move()

def stuck():
	global y_l,fast,linear_speed,angular_speed

	while not rospy.is_shutdown():

		sign =1
		if y_b < 0.1:
			sign = -1

		vel_msg = Twist(Vector3(-0.1*sign,0,0), Vector3(0,0,0))
		velocity_publisher.publish(vel_msg)
		print('oops')
		rate.sleep()

		if y_l > 0.4:
			if y_b > 0.1:
				break
	
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))	
	wander_controller_rotate()

if __name__ == '__main__':
	try:
		rospy.init_node('wander_control', anonymous=True)
		velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
		rate = rospy.Rate(10) # 20hz

		#Testing our function
		wander_controller_move()

	except rospy.ROSInterruptException: pass



























