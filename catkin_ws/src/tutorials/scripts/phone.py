#!/usr/bin/env python

import rospy  
from std_msgs.msg import String 

def callback_receive_radio_data(msg):
    rospy.loginfo("message received : ")
    rospy.loginfo(msg)

if __name__ == '__main__':
     
     rospy.init_node('mobile') 
    
     sub = rospy.Subscriber("/robot_radio",String, callback_receive_radio_data) 
     
     rospy.spin() # allows code to run till given topic publishes

