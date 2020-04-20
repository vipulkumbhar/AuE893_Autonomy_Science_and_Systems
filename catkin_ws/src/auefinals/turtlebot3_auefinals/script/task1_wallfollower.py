#!/usr/bin/env python
import rospy
import numpy as np
from numpy import inf
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int64

distancefromwall     = 0.20
x    = np.zeros((360))# lidar scan data
f_d  = 0              # front wall distance
r_d  = 0              # right wall distance
fr_d = 0
prev_err = 0
mission_stage = 0

def callback(data):
	global x,f_d,r_d,fr_d

	x  = list(data.ranges)
	for i in range(360):
		if x[i] == inf:
			x[i] = 7
		if x[i] == 0:
			x[i] = 6

        # store scan data 
	r_d  = min(x[270:340])              # right wall distance
	f_d  = min(min(x[0:10],x[350:359])) # front wall distance
	fr_d = min(x[340:359])              # front right distance

def tmnt_controller():

	#Setup
	global x,r_d,f_d,fr_d,prev_err
	global distancefromwall
	

	rospy.init_node('auefinals', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=3)
	scan_subscriber    = rospy.Subscriber('/scan', LaserScan, callback)
	rate               = rospy.Rate(10)                  

	while not rospy.is_shutdown():

		delta = distancefromwall-r_d   # distance error 
		#PD controller
		PID_output  = delta*1.8 + (delta-prev_err)*40
		prev_err    = delta

		#clip PID output
		angular_zvel = np.clip(PID_output,-1.0,1.0)

		vel_factor   = np.clip((1-abs(delta)/1.2),0,1)
		linear_vel   = np.clip((f_d-0.15)*vel_factor,-0.1,0.2)   #0.15

		if f_d < 0.5 and fr_d < 0.4:
			angular_zvel = 0.6               #0.5
			print('turn')

		if linear_vel < 0:
			angular_zvel = -1*angular_zvel

		if r_d ==0:
			angular_zvel = 0
			
		#check IOs
		print('distance from right wall in cm =',format(int(r_d*100)),'/',format(distancefromwall*100))
		print('distance from front wall in cm =',format(f_d*100))
		print('linear_vel=',format(linear_vel),' angular_vel=',format(angular_zvel))
		rospy.loginfo(r_d)
		rospy.loginfo('\n') 

		#publish cmd_vel
		vel_msg = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_zvel))
		sub_status = rospy.Subscriber("/mission_stage", Int64, callback_mission_stage)
		if mission_stage ==2:
			vel_msg = Twist(Vector3(0,0,0), Vector3(0,0,0))
		velocity_publisher.publish(vel_msg)
		rate.sleep()
		if mission_stage==2:
			break
		
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	rospy.loginfo('Turtlebot stopped')

def callback_mission_stage(msg):
    global mission_stage
    mission_stage =  msg.data

if __name__ == '__main__':
	try:
		#start turtllebot
		tmnt_controller()
	except rospy.ROSInterruptException: pass
