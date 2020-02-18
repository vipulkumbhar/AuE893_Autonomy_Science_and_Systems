#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.14159
import time
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
import math

########################################################

# initialize global variables
x_pos =0
y_pos =0
yaw_pos =0
x=0
y=0
yaw=0

###############################################################################################
# go to goal

def moveGoal(goal_pose, distance_tolerance):

    global x, y, yaw
    x_goal = goal_pose.x
    y_goal = goal_pose.y

    velocity_message = Twist()

    # publisher
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    loop_rate = rospy.Rate(10)
    error = 0.0

    while True:

        kp = 0.5
        ki = 3.0

        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        velocity_message.linear.x = kp * distance
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0

        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = ki * (math.atan2(y_goal-y, x_goal-x)-yaw)

        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

        if distance < distance_tolerance:
            print("end moveGoal")
            break

#############################################################################        

def execute_closed_loop_square():
    
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    
    while not rospy.is_shutdown():

            pose1=Pose()
            pose1.x=5
            pose1.y=5
            moveGoal(phase1,0.1)
    
            loop_rate= rospy.Rate(10)
            loop_rate.sleep()
    

        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        
         
        #loop to re-orient turtlebot
        relative_angle = (0-yaw)
        if relative_angle <0:
           angularspeed=-1
        else:
            angularspeed=1

        t6 = rospy.Time.now().to_sec()
        current_angle = 0
        vel_msg.linear.x= 0
        vel_msg.angular.z = anguarspeed*0.2

        while(current_angle < relative_angle):

              velocity_publisher.publish(vel_msg)
              t16 = rospy.Time.now().to_sec()
              current_angle = angular_speed*(t16-t6)

         pose2=Pose()
         pose2.x=8
         pose2.y=5
         pose2.theta=0
         moveGoal(pose2,0.1)
         
    
    
    
    
    


##################################################################################################

def movetodesiredyaw():

    relative_angle_radians = 0 - yaw

    if relative_angle_radians < 0:
        clockwise = True
    else:
        clockwise = False

    rotate(0.2, abs(relative_angle_radians), clockwise)

#################################################################################################
def move_square_closedloop():

    #global x, y ,yaw

    # go to 5,5 start point


    pose1.theta=0
    loop = rospy.Rate(1)

    #xyz = turtlebot()
    #xyz.move2goal()
    #loop.sleep()
   
    #orient in desired direction
    rotate(0.2,(3.14159/2),False)
    #movetodesiredyaw()

    # move from 5,5 to 5,8
    move(.2, 3)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # move from 5,8 to 8,8

    move(0.2,3)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # move from 8,8 to 5,8
    move(0.2,3)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # 5,5
    move(0.2,3)
    loop.sleep()

#########################################################################
if __name__ == '__main__':

    try:
         # init node
        rospy.init_node('robot_cleaner', anonymous=True)

        # subscriber for turtlesim/Pose
        pose_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(pose_topic, Pose)

        #square_openloop()
        move_square_closedloop()

    except rospy.ROSInterruptException: pass

#########################################################################
