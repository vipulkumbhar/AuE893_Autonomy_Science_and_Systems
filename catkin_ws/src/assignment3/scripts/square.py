#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist, Vector3
PI = 3.14

def talker():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 1hz
    speed = 0.2
    vel_lin = Twist(Vector3(speed,0,0), Vector3(0,0,0))

    vel_ang = Twist(Vector3(0,0,0), Vector3(0,0,speed))
    side = 2
    angle = PI/2.0

    i = 0
    while not rospy.is_shutdown():

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

            pub.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))

            i += 1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
