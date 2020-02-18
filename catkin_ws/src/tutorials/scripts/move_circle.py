#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty

x=0
y=0
yaw=0

def posecallback(pose_message):
    global x
    global y
    global yaw

    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta
   
    #print('Pose callback')
    #print('x = {}'.format(pose_message.x)) 
      
def move_circle():

    global x
    global y
    global yaw

    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #pose_sub = rospy.Subscriber('/turtle1/Pose', Pose, pose_callback)

    rate = rospy.Rate(2)

    #Receiveing the user's input
    print("Let's move robot in circular motion")
 
    circle_radius = 2
    turtlespeed   = 0.5
    #Since we are moving just in x-axis
    vel_msg.linear.x = 0.5
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = turtlespeed/circle_radius
    
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        print(x)
        rate.sleep()

if __name__ == '__main__':
    try:
        #Testing our function
        pose_sub = rospy.Subscriber('/turtle1/pose', Pose, posecallback)   # its '/turtle1/pose' not '/turtle1/Pose'
        move_circle()
    except rospy.ROSInterruptException: pass



