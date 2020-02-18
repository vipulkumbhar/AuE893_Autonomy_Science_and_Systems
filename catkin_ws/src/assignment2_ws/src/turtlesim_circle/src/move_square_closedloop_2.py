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

#########################################################


###############################################################################################
# go to goal

class turtlebot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        #rospy.init_node('robot_cleaner', anonymous=True)

        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.callback)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def callback(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        #yaw = round(self.pose.theta,4)

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance

    def move2goal(self):
        goal_pose = Pose()
        goal_pose.x = 5
        goal_pose.y = 5
        distance_tolerance = 0.1
        vel_msg = Twist()


        while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:

            #Porportional Controller

            distance_g = sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
 
            #linear velocity in the x-axis:
            vel_msg.linear.x = 1.5 * sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 4 * (atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x) - self.pose.theta)

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
          
            if distance_g < distance_tolerance:
               print("end move2gola")
               break
        

   # define move function

    def move(distance):
    # Starts a new node
    # rospy.init_node('robot_cleaner', anonymous=True)

        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()
    
    #Checking if the movement is forward or backwards
        isForward = 1

    #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
    
        while not rospy.is_shutdown():

        #Setting the current time for distance calculus
            t0 = float(rospy.Time.now().to_sec())
            current_distance = 0

        #Loop to move the turtle in an specified distance
            while(current_distance < 3):
            #Publish the velocity
                velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
                t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
                current_distance= 2*(t1-t0)
        #After the loop, stops the robot
            vel_msg.linear.x = 0
        #Force the robot to stop
            velocity_publisher.publish(vel_msg)
##################################################################################################

    def movetodesiredyaw():

        relative_angle_radians = 0 - yaw

        if relative_angle_radians < 0:
            clockwise = True
        else:
            clockwise = False

        rotate(0.2, abs(relative_angle_radians), clockwise)

# define rotate function

    def rotate(speed, angle, clockwise):
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        vel_msg = Twist()

    #Converting from angles to radians
        angular_speed = speed
        relative_angle = angle

    #We wont use linear components
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
        if clockwise:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)

    # Setting the current time for distance calculus
        t6 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle < relative_angle):
            velocity_publisher.publish(vel_msg)
            t16 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t16-t6)

    #Forcing our robot to stop
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)

#################################################################################################
def move_square_closedloop():

    global x, y ,yaw

    # go to 5,5 start point

    pose1=Pose()
    pose1.x=5
    pose1.y=5
    pose1.theta=0
    loop = rospy.Rate(10)

    xyz = turtlebot()
    xyz.move2goal()

    loop.sleep()
   
    #orient in desired direction
    y1 = turtlebot()
    y1.rotate(0.2,(3.14159/2),False)
    #movetodesiredyaw()

    # move from 5,5 to 5,8
    yz = turtlebot()
    yz.move()

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
