#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg  import Twist, Vector3
from sensor_msgs.msg import LaserScan
flag = 0

def callback(data):
	global flag
	#rospy.loginfo(rospy.get_caller_id(), data.ranges)
	x = y = []
	z = float('inf')
	x = list(data.ranges)
	#print(type(data.ranges))
	# 10 deg flank on either side of the center
	y = x[9:0:-1] + [x[0]] + x[-1:-11:-1]
	z = (y[len(y)/2] + y[(len(y)/2) - 1])/2
	print(z)

	if z < 0.3:
		flag = 1
	#print(len(y))




def tmnt_controller():
	#Setup
	rospy.init_node('tmnt_control', anonymous=True)
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	scan_subscriber = rospy.Subscriber('/scan', LaserScan, callback)
	rate = rospy.Rate(10) # 1hz

	vel_msg = Twist(Vector3(0.5,0,0), Vector3(0,0,0))

	while not rospy.is_shutdown() and flag==0:
		#rospy.loginfo(vel_msg)
		velocity_publisher.publish(vel_msg)
		rate.sleep()
	velocity_publisher.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	print('EMERGENCY BRAKES ACTIVATED!!')

if __name__ == '__main__':
	try:
		#Testing our function
		tmnt_controller()
	except rospy.ROSInterruptException: pass
