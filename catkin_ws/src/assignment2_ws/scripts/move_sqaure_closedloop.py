#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math 
from math import pow,atan2,sqrt

PI= 3.1415926535897

x = 0
y = 0
yaw = 0

z = 0
no_of_rotation = 1

pos_x   = 0
pos_y   = 0
pos_yaw = 0

def move():
    
     print('move function has been initiated')
     pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =10)
     vel_msg = Twist() 
     rate = rospy.Rate(10)
     
     square_side    = 20
     turtle_speed   = 0.5
     turtle_yawrate = 0.5  
     rotation_time  = 4*PI/2/turtle_yawrate   
 
     # fixed vel commands, no need to change further
     vel_msg.linear.y  = 0
     vel_msg.linear.z  = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0

     while not rospy.is_shutdown():

               t0 = float(rospy.Time.now().to_sec())
               #print('time count started')
               current_distance = 0
               while current_distance < square_side:
                     vel_msg.linear.x  = turtle_speed
                     vel_msg.angular.z = 0
                     pub.publish(vel_msg)
                     #print('moving in straigth line')
                     t1 = float(rospy.Time.now().to_sec())

                     current_distance = current_distance + (t1-t0)*turtle_speed
                     print('moving in straight line, current distance= ',format(current_distance))
                     rate.sleep()

               #stop turtlebot
               vel_msg.linear.x  = 0
               vel_msg.angular.z = turtle_yawrate
               pub.publish(vel_msg)
               print('turtlebot has been stopped')          # stop turtlebot by using rospy.spin()
               #rospy.spin()
               break

def rotate(yaw_input):
     print('Rotate function has been initiated')
     pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =10)
     vel_msg = Twist()
 
     rate     = rospy.Rate(20)
     yaw_rate = 0.5               #in rad/sec
     angle    = yaw_input         #90*(2*PI/360)
 
     # fixed vel commands, no need to change further
     vel_msg.linear.x  = 0
     vel_msg.linear.y  = 0
     vel_msg.linear.z  = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     vel_msg.angular.z = yaw_rate

     while not rospy.is_shutdown():
           t0 = float(rospy.Time.now().to_sec())
           current_angle = 0
           while (current_angle < angle):
                 pub.publish(vel_msg)
                 t1 = float(rospy.Time.now().to_sec())
                 current_angle = yaw_rate*(t1-t0)
      
           vel_msg.angular.z = 0
           pub.publish(vel_msg)
           #rospy.spin()
           print('rotation complete')
           break
   
def poseCallback(pose_msg):
    #print('callback called')
    global pos_x
    global pos_y
    global pos_yaw

    pos_x   = pose_msg.x
    pos_y   = pose_msg.y
    pos_yaw = pose_msg.theta
        
def gotogoal(goal_x,goal_y, speed):
     print('gotogoal function has been initiated')
     pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =10)
     vel_msg = Twist()

     pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, poseCallback)
     pose = Pose()
     rate = rospy.Rate(10)
 
     vel_msg.linear.y  = 0
     vel_msg.linear.z  = 0
     vel_msg.angular.x = 0
     vel_msg.angular.y = 0
     
     global pos_x, pos_y, pos_yaw

     distance_tolerance = 0.1
     
     while not rospy.is_shutdown():
           #t0 = float(rospy.Time.now().to_sec())
           while (sqrt(pow((goal_x - pos_x), 2) + pow((goal_y - pos_y), 2))) > distance_tolerance:

                  distance = abs(math.sqrt(((goal_x-pos_x) ** 2) + ((goal_y-pos_y) ** 2)))
                  vel_msg.linear.x = speed*0.5 * distance
                  vel_msg.angular.z = 3.0 * (atan2(goal_y - pos_y, goal_x - pos_x) - pos_yaw) #(math.atan2(goal_y-pos_y, goal_x-pos_x)-pos_yaw)
           
                  pub.publish(vel_msg)
                  rate.sleep()

           vel_msg.linear.x  =0
           vel_msg.angular.z =0
           pub.publish(vel_msg)
           print('goal achieved')
           break 
   

def desiredyaw(desired_yaw):

     rotate_angle = desired_yaw - pos_yaw
     rotate(rotate_angle)  
     print('current yaw in degree', format(pos_yaw*360/2/PI))   
        
if __name__ == '__main__':
    try:
        #move in square loop
        rospy.init_node('open_loop_square', anonymous = True)
        print('closed loop square node has been initiated')
        rate = rospy.Rate(10)

        gotogoal(5,5,1)
        rate.sleep()
        desiredyaw(0)
        gotogoal(8,5,1)
        rate.sleep()
        desiredyaw(PI/2)
        gotogoal(8,8,1)
        rate.sleep()
        desiredyaw(PI)
        gotogoal(5,8,1)
        rate.sleep()
        desiredyaw(3*PI/2)
        gotogoal(5,5,0.2)
        rate.sleep()
 
        #print('mission success')   
    except rospy.ROSInterruptException: pass


## trash

    #Checking if the movement is forward or backwards
    
