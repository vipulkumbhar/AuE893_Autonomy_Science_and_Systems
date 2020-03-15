#!/usr/bin/env python
import rospy
import numpy as np
from numpy import inf
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan

scanrange = 80          #
front_scanrange = 5
distancefromwall = 0.2

x  = np.zeros((360))
s_d = 0
y_l = 0
y_r = 0

kp = 1
kd = 100
ki = 0

k1 = kp + ki + kd
k2 = -kp - 2*kd
k3 = kp


def callback(data):
	global y_l, y_r,x,s_d

	x  = list(data.ranges)                # store scan data 
	y_l= min(x[20:100])                   # left wall distance
	y_r= min(x[260:340])                  # right wall distance
	s_d = min(min(x[0:20],x[340:360]))    # front wall distance

def tmnt_controller():

	#Setup
	global k1,k2,k3,kp,kd,ki,s_d,x,y_r,y_l
	global distancefromwall

	# Initialize parameters used in PID controller
	prev_PID_output = 0
	prev_error = 0
	prev_prev_error = 0

	rospy.init_node('tmnt_wallfollowing_control', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
	rate = rospy.Rate(20)                  # 20hz

	while not rospy.is_shutdown():

		delta = distancefromwall-y_r   # distance error

		#PID controller
		#PID_output = prev_PID_output + k1*delta + k2*prev_error + k3*prev_prev_error

		#PD controller
		PID_output = kp*delta + kd*(delta-prev_error)

		#stored states
		prev_PID_output = PID_output
		prev_error = delta
		prev_prev_error = prev_error

		# if bot is heading towards wall
		add_angular_vel = 0
		if s_d < distancefromwall:
			add_angular_vel = 0.2
			print('wall ahead')

		if s_d < 0.1:
			linear_vel      = -0.1
			angular_zvel    = 0.1
			if y_l > y_r:
				angular_zvel = -0.1 
			add_angular_vel = 0
			print('too close to front wall')

		#clip PID output
		angular_zvel = np.clip((PID_output+add_angular_vel),-1,1)
		linear_vel   = np.clip((s_d-0.3),-0.1,0.5)

		#check IOs
		print('in cm','right=',format(int(y_r*100)),' left=',format(int(100*y_l)),' front distance=',format(int(100*s_d)))
		print('linear_vel=',format(linear_vel),' angular_vel=',format((int(angular_zvel*1000))/1000))
		rospy.loginfo('\n') 

		#publish cmd_vel
		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_zvel))
		velocity_publisher.publish(vel_msg)
		rate.sleep()

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('Turtlebot stopped')

if __name__ == '__main__':
	try:
		#start turtllebot
		tmnt_controller()

	except rospy.ROSInterruptException: pass
