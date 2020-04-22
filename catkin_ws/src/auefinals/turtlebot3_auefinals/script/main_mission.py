#!/usr/bin/env python

import roslaunch
import rospy
from std_msgs.msg import Int64
from geometry_msgs.msg  import Twist, Vector3
import numpy as np
from numpy import inf
from sensor_msgs.msg import LaserScan

# initiate main node
rospy.init_node('aue_final_team3', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

# wait for 'launch world'
rospy.sleep(5)

# launch SLAM mapping
launch_slam = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/turtlebot3/turtlebot3_slam/launch/turtlebot3_slam.launch"])
launch_slam.start()
rospy.loginfo("slam initiated")
rospy.sleep(2)

# mission status callback
mission_stage = 1
current_tag   = 0
def callback_mission_stage(msg):
    global mission_stage
    mission_stage =  msg.data
   
def callback_current_tag(msg):
    global current_tag
    current_tag =  msg.data 

sub_status = rospy.Subscriber("/mission_stage", Int64, callback_mission_stage)
sub_tag    = rospy.Subscriber("/current_tag", Int64, callback_current_tag)
pub_vel    = rospy.Publisher('/cmd_vel', Twist, queue_size=3)

# wall follower
launch_wf = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_wall_follower.launch"])

if mission_stage ==1:
	launch_wf.start()
	rospy.loginfo("wall following initiated")

while mission_stage==1:
	rospy.loginfo('mode - wall following')
	rospy.sleep(0.3)

launch_wf.shutdown()

# obstacle avoidance
launch_oa = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_obstacle_aviodance.launch"])

if mission_stage ==2:
	launch_oa.start()
	print(' starting obstacle avoidance mode')
while mission_stage==2:
	rospy.loginfo('obstacle avoidance mode')
	rospy.sleep(0.3)

pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
launch_oa.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))

## lane follower

#1 traffic sign - stop
launch_sd = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/darknet_ros/darknet_ros/launch/darknet_ros.launch"])
if mission_stage ==3:
	launch_sd.start()
	rospy.loginfo('Traffic sign recognition node started')

rospy.sleep(3)

#2 traffic sign callback publisher node
launch_pn = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_traffic_sign.launch"])
if mission_stage ==3:
	launch_pn.start()
	rospy.loginfo('Traffic sign recognition node started')

#3 follow lane
launch_lf = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_lane_follower.launch"])
if mission_stage == 3:
	launch_lf.start()
	print('starting lane follower mode')

while mission_stage ==3:
	rospy.loginfo('lane follower mode')
	rospy.sleep(0.3)

# shutdown lane follower
launch_lf.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	
## leg follower

#1 start leg detector node
launch_ld = roslaunch.parent.ROSLaunchParent(uuid,["/home/vipulkumbhar/catkin_ws/src/People_Detection/people/leg_detector/launch/pi_leg_detector.launch"])
launch_ld.start()

rospy.sleep(2)

#2 start leg follower ndoe
rospy.loginfo('Starting leg follower')
launch_legf = roslaunch.parent.ROSLaunchParent(uuid,["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_leg_follower.launch"])
launch_legf.start()

while mission_stage ==4 and not rospy.is_shutdown():
	rospy.loginfo('mode - leg follower')
	rospy.sleep(0.3)

# shutdown all nodes
launch_ld.shutdown()
launch_legf.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))

rospy.loginfo('closing all nodes')
rospy.sleep(5)

#to delete temp log files 
#rosclean purge

	


