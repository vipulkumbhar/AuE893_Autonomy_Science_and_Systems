#!/usr/bin/env python
import rospy
import math
import numpy as np
from std_msgs.msg import Int64
from math import pow,atan2,sqrt
from geometry_msgs.msg  import Twist, Vector3
from people_msgs.msg import PositionMeasurementArray
from geometry_msgs.msg import PoseWithCovarianceStamped

leg_detected = False
leg_x   = 0
leg_y   = 0
leg_distance = 0

#Edit below
def leg_detection_callback(data):
	pos_ar = np.empty([0, 3])      # x,y, distance from bot
	for people2 in data.people:
		distance = math.sqrt( (people2.pos.x)*(people2.pos.x) + (people2.pos.y)*(people2.pos.y))
		pos_ar   = np.append( pos_ar,[people2.pos.x,people2.pos.y,distance])
	pos_ar_size = pos_ar.size
	pos_ar      = pos_ar.reshape((int(pos_ar_size/3),3))

	leg_param    = [0,0,0]
	global leg_detected
	global leg_x
	global leg_y
	global leg_distance

	if pos_ar_size/3 > 0:
		leg_detected = True
		index_min = np.argmin(pos_ar[:,2])

		#find nearest leg pose
		leg_param = pos_ar[index_min,:]
		leg_x = leg_param[0]
		leg_y = leg_param[1]
		leg_distance = leg_param[2]
		#print(pos_ar[index_min,:])

	print(leg_detected,leg_x,leg_y)

	linear_vel   = 0
	angular_zvel = 0
	
	if leg_detected ==False:
		leg_x = 0
		leg_y = 0
		linear_vel   = 0
		angular_zvel = 0   # just to rotate bot/ until it detects leg
		rospy.loginfo('leg not detected')

	if leg_detected and leg_x> 1000:
		linear_vel   = 0
		angular_zvel = 0.4 #*leg_y/abs(leg_y)
		rospy.loginfo('leg detected, move back motion')

	if leg_detected and leg_distance > 0.3:
		linear_vel   = 0.2
		angular_zvel = np.clip(leg_y*2,-0.2,0.2) *linear_vel/abs(linear_vel)
		rospy.loginfo('leg detected, leg follower mode')
	
	print(linear_vel,angular_zvel)

	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	vel_msg            = Twist(Vector3(linear_vel,0,0), Vector3(0,0,angular_zvel))
	velocity_publisher.publish(vel_msg)
				    
def main():
    rospy.init_node('leg_detector_and_follower', anonymous=True)
    
    while not rospy.is_shutdown():
    	ts_sub   = rospy.Subscriber("/people_tracker_measurements",PositionMeasurementArray,leg_detection_callback)
    	rate = rospy.Rate(10)
    	rate.sleep()
    
    #ctrl_c = False
    #def shutdownhook():
        # works better than the rospy.is_shut_down()
        # line_follower_object.clean_up()
      #  rospy.loginfo("shutdown time!")
     #   ctrl_c = True
    
    #rospy.on_shutdown(shutdownhook)
    #while not ctrl_c:
    #    rate.sleep()
    
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass






