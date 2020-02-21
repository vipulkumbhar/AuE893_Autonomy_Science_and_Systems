#!/usr/bin/env python

import rospy  
from std_msgs.msg import String #for publishing messages 

if __name__ == '__main__':
     
     rospy.init_node('radio_2', anonymous=True) #node name can be recalled as $ rosnode list

     pub = rospy.Publisher("/robot_radio", String, queue_size=10) #rostopic , $ rostopic list, $rostopic echo /robot_radio 

     #queue size for defining maximum backlog of messages 
     
     #rospy.loginfo("this node has been started")
      
     rate = rospy.Rate(2) #update rate/ refresh rate

     while not rospy.is_shutdown():
           
           msg=String()     #define message type
           msg.data="2 This is publishing test oops" #define message
           pub.publish(msg) #publish message

           #rospy.loginfo("Hello")

           rate.sleep()     # set sleep interval

     rospy.loginfo("node has been stopped") #after while loop gives notification
