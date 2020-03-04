#!/usr/bin/env python
import rospy
import numpy as np
from numpy import inf
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan

scanrange = 60   #even number
x  = np.zeros((360))

y_l = 0
y_r = 0

kp = 0.5
kd = 10
ki = 0

k1 = kp + ki + kd
k2 = -kp - 2*kd
k3 = kp

distancefromwall = 0.4

def callback(data):
	global y_l, y_r,avg_range,x
	#rospy.loginfo(rospy.get_caller_id(), data.ranges)

	x  = list(data.ranges)

	i_min = 0 #int(90-scanrange/2)
	i_max = int(90+scanrange/2)
	y_l= min(x[i_min:i_max])
	y_r= min(x[180+i_min:180+i_max])

	#print('right side distance = ',format(y_r))
	#print('left ',format(x[85:95]))
	#print('right ',format(x[265:275]))

def tmnt_controller():
	#Setup
	global k1,k2,k3,kp,kd
	global x
	global distancefromwall
	global y_r

	prev_PID_output = 0
	prev_error = 0
	prev_prev_error = 0

	rospy.init_node('tmnt_control', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
	rate = rospy.Rate(20) # 5hz

	while not rospy.is_shutdown():

		#error
		delta = distancefromwall-y_r

		#PID controller
		#PID_output = prev_PID_output + k1*delta + k2*prev_error + k3*prev_prev_error
		PID_output = kp*delta + kd*(delta-prev_error)

		#stored states
		prev_PID_output = PID_output
		prev_error = delta
		prev_prev_error = prev_error

		# clip PID output
		angular_zvel = np.clip(PID_output ,-1,1)

		print('angular vel = ',format(angular_zvel))
		print('right side distance = ',format(y_r))
		print('kd factor',format(k2*prev_error))
		#print('right ',format(x[85:95]))

		vel_msg = Twist(Vector3(0.1,0,0), Vector3(0,0,angular_zvel))
		velocity_publisher.publish(vel_msg)
		rate.sleep()

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('Turtlebot stopped')

if __name__ == '__main__':
	try:
		#Testing our function
		tmnt_controller()
	except rospy.ROSInterruptException: pass
