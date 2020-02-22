#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

def move():
    # Starts a new node
    rospy.init_node('turtlewall', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    length = 999
    first=[]
    second=[]
    angles=5
    while length >= 1:
        scan = rospy.wait_for_message('scan',LaserScan)
        x=len(scan.ranges)
        for i in range(angles):
            first.append(scan.ranges[(angles-1)-i])
            second.append(scan.ranges[(x-1)-i])

        final_scan=first+second
        y=len(final_scan)
        
        #Checking the lowest of the two middle values as even number of elements
        if final_scan[y/2] <= final_scan[(y/2) - 1]:
            length = final_scan[y/2]
        else:
            length = final_scan[(y/2) - 1]

        vel_msg.linear.x = 1
        velocity_publisher.publish(vel_msg)
    
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)



if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
