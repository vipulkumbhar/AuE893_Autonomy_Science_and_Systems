#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.14159
import time
from turtlesim.msg import Pose
import math

x_pos =0
y_pos =0
yaw_pos =0

#########################################################
# define move function

def move(speed, distance):
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
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
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)

############################################################################
# define rotate function

def rotate(speed, angle, clockwise):

    #Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Converting from angles to radians
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

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
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)


    #Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    rospy.spin()

###################################################################
# go to goal

def posecallback(pose_message):
        global x
        x = pose_message.x
        global y
        y = pose_message.y
        global yaw
        yaw = pose_messgae.theta
         
def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance
####################################################################

def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    if relative_angle_radians < 0:
        clockwise = True
    else:
        clockwise = False
    rotate(0.2, abs(relative_angle_radians), clockwise)

####################################################################
def move2goal(x,y,t):
        goal_pose = Pose()
        goal_pose.x = x
        goal_pose.y = y
        distance_tolerance = t
        vel_msg = Twist()

        while sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2)) >= distance_tolerance:

            #Porportional Controller
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
        #Stopping our robot after the movement is over
        vel_msg.linear.x = 0
        vel_msg.angular.z =0
        self.velocity_publisher.publish(vel_msg)

        rospy.spin()

######################################################################
def closedloop():

    global x, y ,yaw

    pose1=pose()
    pose1.x=5
    pose1.y=5
    pose1.theta=0

    # go to start point 5,5
    loop = rospy.Rate(1)
    moveGoal(pose1.x,pose1.y,0.01)
    loop.(sleep)

    #orient in desired direction
    setDesiredOrientation(0)

    # start square motion to 5,8
    pose2=pose()
    pose2.x = 8
    pose2.y = 5
    pose2.theta = 0
    move(0.2,3)
    #moveGoal(pose2.x,pose2.y,0.01)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # 8,8
    pose3=pose()
    pose3.x = 8
    pose3.y = 8
    pose3.theta = 0
    move(0.2,3)
    #moveGoal(pose3.x,pose3.y,0.01)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # 5,8
    pose4=pose()
    pose4.x = 5
    pose4.y = 8
    pose4.theta = 0
    move(0.2,3)
    #moveGoal(pose4.x,pose4.y,0.01)
    loop.sleep()
    rotate(0.2,(3.14159/2),False)

    # 5,5
    move(0.2,3)
    loop.sleep()

#########################################################################
if __name__ == '__main__':

    try:
         # init node
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        # cmd_vel publisher

        # subscriber for turtlesim/Pose
        pose_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(pose_topic, Pose, poseCallback)

        #circle()
        #square_openloop()
        closedloop()

    except rospy.ROSInterruptException: pass
