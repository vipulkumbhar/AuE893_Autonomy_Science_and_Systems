#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI= 3.1415926535897

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    #Receiveing the user's input
    print("Let's move robot in 2X2 square with 0.2 linear velocity and 0.2 rad/s angular velocity. ")

    speed = 0.2
    angular_velocity = 0.2
    isForward = 1

    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    
    while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_time = 0
        current_angle_z =0

        #Loop to move the turtle in an specified distance
        while(current_time < 10):

            vel_msg.linear.x = speed
            vel_msg.angular.z = 0

            #Publish the velocity
            velocity_publisher.publish(vel_msg)

            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())

            #Calculates distancePoseStamped
            current_time=current_time+(t1-t0)

        while (current_time > 10) and (current_angle_z < PI/2):
              vel_msg.linear.x = 0
              vel_msg.angular.z = angular_velocity

              velocity_publisher.publish(vel_msg)
              t1=float(rospy.Time.now().to_sec())
              current_time=current_time+(t1-t0)


        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass


## trash

    #Checking if the movement is forward or backwards
    
