#!/usr/bin/env python
import rospy
import numpy as np
from numpy import inf
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan

y_l = 0
y_r = 0
scanrange = 70   #even number
x  = np.zeros((360))
kp = 0.1
kd = 0.6
distancefromwall = 0.5

def callback(data):
	global y_l, y_r,avg_range,x
	#rospy.loginfo(rospy.get_caller_id(), data.ranges)

	x  = list(data.ranges)

	i_min = int(90-scanrange/2)
	i_max = int(90+scanrange/2)
	y_l= min(x[i_min:i_max])
	y_r= min(x[180+i_min:180+i_max])

	#print('right side distance = ',format(y_r))
	#print('left ',format(x[85:95]))
	#print('right ',format(x[265:275]))

def tmnt_controller():
	#Setup
	global kp,kd
	global x
	global distancefromwall
	global y_r
	t1 = 1
	t2 = 0
	previousdelta=0
	delta = 0
	rospy.init_node('tmnt_control', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
	rate = rospy.Rate(10) # 5hz

        t0 = float(rospy.Time.now().to_sec())
	while not rospy.is_shutdown():
		delta = distancefromwall-y_r

		#PID controller
		PD_output = kp*delta + kd*(delta-previousdelta)/(t1-t2)

		kdprint = kd*(delta-previousdelta)/(t1-t2)

		previousdelta=delta
		#rospy.loginfo(vel_msg)
		angular_zvel = np.clip(PD_output ,-2,2)

		print('angular vel = ',format(angular_zvel))
		print('right side distance = ',format(y_r))
		print('kd factor',format(kdprint))
		#print('right ',format(x[85:95]))

		vel_msg = Twist(Vector3(0.05,0,0), Vector3(0,0,angular_zvel))
		velocity_publisher.publish(vel_msg)
		rate.sleep()
		t1 = float(rospy.Time.now().to_sec())
		t2 = t0

	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('Turtlebot stopped')

if __name__ == '__main__':
	try:
		#Testing our function
		tmnt_controller()
	except rospy.ROSInterruptException: pass
