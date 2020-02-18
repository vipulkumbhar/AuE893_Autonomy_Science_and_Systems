#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI= 3.1415926535897

from turtlesim_circle.srv import *

def move_square_function():
          rospy.wait_for_service('move_sqaure')
          try:
              side_length = 2
              no_of_rotation = 1
              move_square = rospy.ServiceProxy('move_square', MoveSquare)
	      move_square(side_length,rotations)
          
           #except rospy.ServiceException, e:
		  #print "Service call failed: %s"%e


if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass



    
