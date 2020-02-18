#!/usr/bin/env python

import rospy
from rospy_tutorials.srv import AddTwoInts


if __name__=='__main__':
    
     rospy.init_node("add_two_ints_client",anonymous=True)
     rospy.wait_for_service("/add_two_int")

     try:
         add_two_int = rospy.ServiceProxy("/add_two_int",AddTwoInts)
         response= add_two_int(2,6)
         rospy.loginfo("sum is: " + str(response.sum))

     except rospy.ServiceException as e:
            rospy.logwarn("service failed:"+str(e))

