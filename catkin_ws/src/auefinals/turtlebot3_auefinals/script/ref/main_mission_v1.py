#!/usr/bin/env python

# work to do: automate the path arg for all launch files , to replace '/home/vipulkumbhar/catkin_ws/src'

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

# launch world (working)
rospy.sleep(10)

# launch SLAM mapping
launch_slam = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/turtlebot3/turtlebot3_slam/launch/turtlebot3_slam.launch"])
launch_slam.start()
rospy.loginfo("slam initiated")
rospy.sleep(5)

# check mission status
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
	rospy.sleep(0.5)

launch_wf.shutdown()

# obstacle avoidance
launch_oa = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_obstacle_aviodance.launch"])

if mission_stage ==2:
	launch_oa.start()
	print(' starting obstacle avoidance mode')
while mission_stage==2:
	rospy.loginfo('obstacle avoidance mode')
	#rospy.sleep(0.5)

rospy.sleep(1)
launch_oa.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))

## lane follower

# start 3 nodes
launch_lf = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_lane_follower.launch"])
if mission_stage == 3:
	launch_lf.start()
	print('starting lane follower mode')

#1 traffic sign - stop
launch_sd = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/darknet_ros/darknet_ros/launch/darknet_ros.launch"])
if mission_stage ==3:
	launch_sd.start()
	rospy.loginfo('Traffic sign recognition node started')

#2 traffic sign callback publisher node
launch_pn = roslaunch.parent.ROSLaunchParent(uuid, ["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_traffic_sign.launch"])
if mission_stage ==3:
	launch_pn.start()
	rospy.loginfo('Traffic sign recognition node started')

#3 traffic sign node subscribe
traffic_sign_trigger = False # false for stop
def callback_traffic_sign_status(msg):
    global traffic_sign_trigger
    traffic_sign =  msg.data
    if traffic_sign ==1:
	traffic_sign_trigger = True
	 
sub_tf = rospy.Subscriber("/stop_sign", Int64,callback_traffic_sign_status)

# follow lane
while mission_stage ==3 and traffic_sign_trigger==False:
	rospy.loginfo('lane follower mode')
	#rospy.sleep(0.1)

# shutdown all 3 nodes
launch_lf.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
#launch_pn.shutdown()
#launch_sd.shutdown()

#4 traffic sign wait for 4 seconds
rospy.loginfo('Traffic sign stop for 4 sec started')
rospy.sleep(4)
rospy.loginfo('traffic sign stop ended')

#5 start lane follower again
while mission_stage ==3:
	launch_lf.start()
	rospy.loginfo('Lane following node after stop sign')
launch_lf.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	
## leg follower
# start leg detector node
launch_ld = roslaunch.parent.ROSLaunchParent(uuid,["/home/vipulkumbhar/catkin_ws/src/People_Detection/people/leg_detector/launch/pi_leg_detector.launch"])
launch_ld.start()

rospy.sleep(4)
rospy.loginfo('Starting leg follower')
launch_legf = roslaunch.parent.ROSLaunchParent(uuid,["/home/vipulkumbhar/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_leg_follower.launch"])
launch_legf.start()

# save SLAM map 
# rosrun map_server map_saver -f <map_name>

while mission_stage ==4:
	rospy.loginfo('mode - leg follower')

# close all
launch_ld.shutdown()
launch_legf.shutdown()
pub_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
	


