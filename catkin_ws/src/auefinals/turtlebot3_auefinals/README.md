# Team Name: TMNT (Teenage Mutant Ninja Turtles)	

## Team Number: 03  
### Team Members: <img align="right" width="300" height="226" src="https://raw.githubusercontent.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/master/catkin_ws/git_readme_files/ninja_turtles_PNG55.png">   	
		Akshay Mahajan 
		Ashit Mohanty  
		Manu Srivastava  
		Siddesh Bagkar  
		Vipul Kumbhar  
		  
### Final Project 

Final project is made up of main 5 maneuvers.    
  
1) Wall follower - Turtlebot maintains predefined distance from right-side wall. Proportional controller based on distance from right-side wall is used to control z-angular velocity.  
  
2) Obstacle avoidance - Turtlebot maintains safe front distance from obstacle and maneuvers through course until it finds yellow lanes.  
  
3) lane follower - Turtlebot follows yellow lane using image-processing (to detect lane center) and proportional controller 
to control z-angular velocity.  
  
4) Traffic sign detection - Darknet package is used for traffic sign detection. Traffic sign callback functions stop the turtlebot for 4 seconds.   
  
5) People / leg tracker - People tracker package is used for leg detection. Proportional controller is to control z-angular velocity to guide tutrlebot towards nearest detected leg. If leg is not detected or lost, turtlebot goes into obstacle avoidance mode.   
  
  
### Methodology
Team explored two methodologies for final project
1) Single script file for all tasks.  
[Script](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script/tb3_gazebo_aue20_ms.py)  
[Launch file](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_main_mission2.launch).     
  
The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch turtlebot3_auefinals turtlebot3_autonomy_final_main_mission2.launch       
```

2) Distributed task scripts (Individual nodes for each task controlled from main mission control node)   
[Script](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script)  
[Launch file](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch)  
  
The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch turtlebot3_auefinals turtlebot3_autonomy_final_main_mission.launch       
```
  
### Script and launch files information 
  
#### Part 1: Lane follower - Lane detection by camera and lane following of turtlebot3.

- Script info: 'follow_line_step_hsv.py' and 'follow_line_step_hsv_bot.py' has camera_callback  
function which works as following  

1) camera_callback(self,data) : 
<pre>

__init__ (self) subscribes to topic "/camera/rgb/image_raw" for gazebo simulation and to topic  
"/raspicam_node/image" for turtlebot3 real run. It also calls turtlebot class (defined in   
move_robot.py) and Cvbridge to work with camera images in ROS environment.

</pre>
	  

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/Lane_following_turtlebot.GIF)

#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/videos/lane_following) - Full length videos of lane following task
  
### File locations:
#### - [Launch files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch)     
#### - [Script files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script)  
#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/video)

### Work Distribution

<pre>
Vipul Kumbhar 	: Code integration of methodology 2 + readme file + Traffic sign detection code
Akshay Mahajan	: Lane follower code
Ashit Mohanty 	: Obstacle avoidance code
Manu Srivastava	: Code integration of methodology 1  + people/leg follower code
Siddhesh Bagkar	: April tag detection code + wall follower code
</pre>
