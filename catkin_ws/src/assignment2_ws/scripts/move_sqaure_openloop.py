#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
PI= 3.1415926535897

x = 0
y = 0
yaw = 0
z = 0
no_of_rotation = 1

def posecallback(pose_msg):
    
    print('callback called')

def move():
    
     print('move function has been initiated')
     pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =10)
     vel_msg = Twist()

     #sub = rospy.Subscriber('/turtle1/pose',Pose, posecallback)
 
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

def rotate():
     print('Rotate function has been initiated')
     pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size =10)
     vel_msg = Twist()
 
     rate     = rospy.Rate(10)
     yaw_rate = 0.5               #in rad/sec
     angle    = 90*(2*PI/360)
 
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
             
if __name__ == '__main__':
    try:
        #move in square loop
        rospy.init_node('open_loop_square', anonymous = True)
        print('open loop square node has been initiated')
        global z
        global no_of_rotation
        while z < 4*no_of_rotation:
             print('this is loop no.',format(z+1))
             move()
             rotate()
             z =z+1
        print('mission success')   
    except rospy.ROSInterruptException: pass


## trash

    #Checking if the movement is forward or backwards
    
