#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.14159

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    #Receiveing the user's input
    print("Let's move robot to make square")
    linearspeed = 0.2
    angularspeed = 0.2
    distance = 2
    isForward = 1

    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    
    while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        current_angle = 0
        x_loop = 2

        #Loop to move the turtle in an specified distance
        while x_loop < 5:
              # while(current_distance < distance)
                      while current_distance < distance:
                            #Publish the velocity
                            vel_msg.linear.x = linearspeed
                            vel_msg.angular.z= 0
                            velocity_publisher.publish(vel_msg)

                            #Takes actual time to velocity calculus
                            t1=float(rospy.Time.now().to_sec())
                            #Calculates distancePoseStamped
                            current_distance= linearspeed*(t1-t0)
                            current_angle = 0

                      t3=float(rospy.Time.now().to_sec())
                      while current_angle < PI/8:
                            vel_msg.linear.x =0
                            vel_msg.angular.z=0.2
                            
                            velocity_publisher.publish(vel_msg)
               
                            #take time to calculate angle turned
                            t2=float(rospy.Time.now().to_sec())
                            current_angle = 0.2*(t2-t3)

                            current_distance = 0

                      x_loop = x_loop +1
                    
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)
        
        rospy.spin()

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
