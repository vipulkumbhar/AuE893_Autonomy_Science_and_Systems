#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Vector3

def move_circle():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) #10Hz

    vel_msg = Twist(Vector3(1,0,0), Vector3(0,0,1))
    

    while not rospy.is_shutdown():
    	rospy.loginfo(vel_msg)
    	velocity_publisher.publish(vel_msg)
    	rate.sleep()

if __name__ == '__main__':
    try:
        #Testing our function
        move_circle()
    except rospy.ROSInterruptException: 
    	pass
