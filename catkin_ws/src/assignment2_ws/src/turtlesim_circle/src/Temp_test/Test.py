#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

X_min = 0.0
Y_min = 0.0
X_max = 11.0
Y_max = 11.0

x=0
y=0
yaw=0


def move(speed, distance, isForward):
    velocity_message = Twist()
    if (isForward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    t0 = rospy.Time.now().to_sec()
    current_distance = 0
    loop_rate = rospy.Rate(10)

    # velocity publisher
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1-t0)
        loop_rate.sleep()

        if not (current_distance < distance):
            rospy.loginfo("reached")
            break

    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


def rotate(angular_speed, relative_angle, clockwise):

    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0

    if (clockwise):
        velocity_message.angular.z = -abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed)

    current_angle = 0.0
    t0 = rospy.Time.now().to_sec()
    loop_rate = rospy.Rate(10)
    # velocity publisher
    velocity_publisher = rospy.Publisher(
        "/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1-t0)
        loop_rate.sleep()
        if current_angle > relative_angle:
            rospy.loginfo("reached")
            break

    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)


def degrees2radians(angle_in_degrees):
    return angle_in_degrees*(math.pi/180.0)


def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    if relative_angle_radians < 0:
        clockwise = True
    else:
        clockwise = False
    rotate(degrees2radians(30), abs(relative_angle_radians), clockwise)


def poseCallback(pose_message):
    global x
    global y
    global yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


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

def circle():
    global x, y
    velocity_message = Twist()

    constant_speed = 4
    rk = 3.5
    loop_rate = rospy.Rate(1)

    # publisher
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:

        rk = rk
        velocity_message.linear.x = rk
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0

        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = constant_speed
        print("velocity_message.x = %s" %velocity_message.linear.x)
        print("velocity_message.x = %s" %velocity_message.angular.z)

        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        if not ((x<10.5) and (y<10.5)):
            print("end spiral")
            break

    # stop robot 
    velocity_message.linear.x = 0
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

def square_openloop():
    global x, y, yaw
    loop = rospy.Rate(0.5)

    move(0.2, 2.0, True)
    rotate(degrees2radians(11.5), degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

    rotate(degrees2radians(11.5), degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)
    rotate(degrees2radians(11.5), degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

    rotate(degrees2radians(11.5), degrees2radians(90), False)

def square_closedloop():
    global x,y,yaw

    pose1 = Pose()
    pose2 = Pose()
    pose3 = Pose()
    pose4 = Pose()
    loop = rospy.Rate(1)

    # (5,5)
    pose1.x = 5
    pose1.y = 5
    pose1.theta = 0
    moveGoal(pose1,0.01)
    loop.sleep()
    setDesiredOrientation(degrees2radians(0))

    # (8,5)
    pose2.x = 8
    pose2.y = 5
    pose2.theta = 0
    moveGoal(pose2,0.01)
    loop.sleep()
    rotate(degrees2radians(40),degrees2radians(90),False)

    # (8,8)
    pose3.x = 8
    pose3.y = 8
    pose3.theta = 0
    moveGoal(pose3,0.01)
    loop.sleep()

    # (8,5)
    pose4.x = 5
    pose4.y = 8
    pose4.theta = 0
    move(2,3, False)
    loop.sleep()
    setDesiredOrientation(degrees2radians(0))

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
        square_closedloop()

    except rospy.ROSInterruptException:
        pass
