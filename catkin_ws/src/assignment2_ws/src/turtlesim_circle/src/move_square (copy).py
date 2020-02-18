#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.14159

def move():
    rospy.init_node('square_move')
    publish_velocity = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    velocity_message = Twist()

    print('node has been initiated')

    # inputs for move_sqaure
    linear_speed  = 0.2
    angular_speed = PI/16
    square_side_length = 2
    no_of_repeatations = 1

    while not rospy.is_shutdown():
        current_distance = 0
        current_angle    = 0
        no_of_turns      = 0

        print('check1')
        t0 = float(rospy.Time.now().to_sec())
        while no_of_turns < 4:
            print('check2')
            while current_distance < square_side_length:
                print('check3')
                velocity_message.linear.y = 0
                velocity_message.linear.z = 0
                velocity_message.linear.x = linear_speed
                velocity_message.angular.x = 0
                velocity_message.angular.y = 0
                velocity_message.angular.z = 0
                publish_velocity.publish(velocity_message)
                print('check4')
                t1 = float(rospy.Time.now().to_sec())

                current_distance = current_distance + (t1-t0)*linear_speed

            t2 = float(rospy.Time.now().to_sec())
            while current_angle < PI/2:
                print('check_a5')
                velocity_message.linear.y = 0
                velocity_message.linear.z = 0
                velocity_message.linear.x = 0
                velocity_message.angular.x = 0
                velocity_message.angular.y = 0
                velocity_message.angular.z = angular_speed
                publish_velocity.publish(velocity_message)
                print('check_a6')
                t3 = float(rospy.Time.now().to_sec())

                current_angle = current_angle + (t3-t2)*angular_speed

            no_of_turns = no_of_turns +1
            print('out of while loop1')

        print('set all velocities to zero')
        # stop the bot    
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0
        velocity_message.linear.x = 0
        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = angular_speed
        publish_velocity.publish(velocity_message)

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
