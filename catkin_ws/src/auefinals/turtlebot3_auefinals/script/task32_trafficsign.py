#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Int64
from darknet_ros_msgs.msg import BoundingBoxes
traffic_sign_c = 0 # false

def traffic_sign_callback(data):

	global traffic_sign_c 
	for box in data.bounding_boxes:
		#rospy.loginfo(box.id)
		if box.id ==11:
			traffic_sign_c=1 
			rospy.loginfo('Traffic sign detected')
		if box.id !=11:
			rospy.loginfo('Sign not detected')

	pub      = rospy.Publisher("/stop_sign", Int64, queue_size=10)
	msg      = Int64()
	msg.data = traffic_sign_c
	pub.publish(msg)
	    
def main():
    rospy.init_node('traffic_sign_detector', anonymous=True)
    while not rospy.is_shutdown():	
    	ts_sub = rospy.Subscriber("/darknet_ros/bounding_boxes",BoundingBoxes,traffic_sign_callback)
    	rate = rospy.Rate(10)
	rate.sleep()
        
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass
	




