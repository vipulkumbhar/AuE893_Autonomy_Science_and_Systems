#!/usr/bin/env python
import rospy                                                      # initiate ros library


from geometry_msgs.msg import Twist

def move():                                                       # define new function with options to input parameters from global workspace

                                                                  # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)              # initiate new node, anonymous - if required

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #publish to topic '/turtle1/cmd_vel' with message type 'Twist' it can be gloabl also. 

    # after starting turtlesim_node, check for available topic list "$ rostopic list" -> 1- /turtle1/cmd_vel , 2-/turtle1/color_sensor 3-/turtle1/pose

    # "$ rostopic info /turtle1/cmd_vel"
    # Type: geometry_msgs/Twist
    # check twist message info "$ rosmsg show geometry_msgs/Twist"
  # geometry_msgs/Vector3 linear
  #   float64 x
  #   float64 y
  #   float64 z
  #   geometry_msgs/Vector3 angular
  #   float64 x
  #   float64 y
  #   float64 z

    # similarly for 'turtlesim/Pose'
  #   float32 x
  #   float32 y
  #   float32 theta
  #   float32 linear_velocity
  #   float32 angular_velocity

    vel_msg = Twist()                                             # define vel_msg to be of 'Twist()' type
    
    #Receiveing the user's input
    print("Let's move your robot")

    # promt input command in terminal (can also be given as input parameter while initiating function) 
    speed = input("Input your speed:")
    distance = input("Type your distance:")
    isForward = input("Foward?: ")
    
    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
    # since Twist() has linear and angular message types with both having further 3 inputs as x, y, z translational and x, y, z rotational
    vel_msg.linear.y = 0                                           #messagename(fromline35).twistmessagetype.messagecomponent
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

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
