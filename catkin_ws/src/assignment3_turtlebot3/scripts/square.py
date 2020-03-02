#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg  import Twist, Vector3
PI = 3.14

def talker():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 1hz
    speed = 0.2
    vel_lin = Twist(Vector3(speed,0,0), Vector3(0,0,0)) # somehow the turtle only goes 
    # in the x direction. Probably has something to do with the twist being defined 
    # in the body frame.
    vel_ang = Twist(Vector3(0,0,0), Vector3(0,0,speed))
    side = 2
    angle = PI/2.0
    #side = rospy.get_param('~length')
    #angle = rospy.get_param('~angle')
    #print(type(ang))
    #current_dist = 0
    #current_orientation = 0
    #t0 = float(rospy.Time.now().to_sec())
    i = 0
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        while i < 5:
            t0 = float(rospy.Time.now().to_sec())
            current_dist = 0
            while current_dist < side: 
                rospy.loginfo(vel_lin)
                pub.publish(vel_lin)
                t1 = float(rospy.Time.now().to_sec())
                rate.sleep()
                current_dist = speed*(t1- t0)

            t0 = float(rospy.Time.now().to_sec())
            current_orientation = 0
            while current_orientation < angle:
                rospy.loginfo(vel_ang)
                pub.publish(vel_ang)
                t1 = float(rospy.Time.now().to_sec())
                rate.sleep()
                current_orientation = speed*(t1 - t0)
            #print(current_orientation)
            pub.publish(Twist(Vector3(0,0,0), Vector3(0,0,0))) # This command is necessary for
            #the rotation to stop. I have no idea why!!!!!!!! Maybe, the turtle keeps executing
            # the commanda it  has left in the queue. Knows who!

            i += 1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass