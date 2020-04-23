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
1) Wall follower
2) Obstacle avoidance
3) lane follower
4) Traffic sign detection
5) People / leg tracker
  
### Methodology
Team explored two methodologies for final project
1) Single script file for all tasks
2) Distributed task scripts (Individual nodes for each task controlled from main mission control node)

### Script and launch files information 
  
#### Part 1: Lane follower - Lane detection by camera and lane following of turtlebot3.

- Script info: 'follow_line_step_hsv.py' and 'follow_line_step_hsv_bot.py' has camera_callback  
function which works as following  

1) camera_callback(self,data) : 
<pre>

__init__ (self) subscribes to topic "/camera/rgb/image_raw" for gazebo simulation and to topic  
"/raspicam_node/image" for turtlebot3 real run. It also calls turtlebot class (defined in   
move_robot.py) and Cvbridge to work with camera images in ROS environment.

camera_callback functions gets images from topic subscribed and converts opencv image format for   
next steps
1] crop image to form mask which will be used for lane centroid
2] convert from RGB image format to gray
3] if lane color present in mask, find x,y co-ordinates of color mask centroid.
4] if lane not found, invoke lane finding maneuver (twist_object.linear.x  = 0.1,  
twist_object.angular.z = 0.02)
5] if lane found, invoke lane following maneuver (proportional controller based on cx distance)
6] if was detected earlier and lane finding maneuver invokes, sprial motion of turtlebot will be  
implemented. 
</pre>
	  
- Launch info: 

Launch file name: turtlebot3_follow_line.launch (launches gazebo world and follow_lane_step_hsv.py)
 
<pre>
This launch file first initializes the type of turtlebot. Here it has a default entry of burger. 
Next, the initial coordinates of the turtlebot have been defined. After that, set of commands 
launch the follow_line.world file in Gazebo and the dynamic parameters of the virtual world are 
initialized. After setting up environment and turtlebot, follow_line_step_hsv.py is run with   
'tb3_line_following' package. 
</pre>

The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch tb3_line_following turtlebot3_follow_line.launch       
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/lane_following_gazebo.GIF)

#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/videos/lane_following) - Full length videos of lane following task

Launch file name: turtlebot3_follow_line_bot.launch (launches follow_lane_step_hsv_bot.py)
<pre>
This launch file launches 'follow_lane_step_hsv_bot.py' from package 'tb3_line_following'.  
Before launching this, make sure that robot bringup node and camera bring-up node is running.   
</pre>

The commands that need to be executed to setup turtlebot for run are as follows:

```
1] $ roscore          # in remote-pc terminal to start roscore  
2] $ ssh pi@IP        # in remote-pc terminal to SSH robot
3] $ roslaunch turtlebot3_bringup bringup_robot.launch  # in turtlebot terminal to bring up robot
4] $ roslaunch raspicam_node camerav2_1280x720.launch enable_raw:=true # in turtlebot terminal to 
bring up camera and publish raw images
```

The commands that need to be executed in the remote -pc terminal for real turtlebotbot3 run are as follows:

```
$ roslaunch tb3_line_following turtlebot3_follow_line_bot.launch       
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/lane_following.GIF)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/Lane_following_turtlebot.GIF)

#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/videos/lane_following) - Full length videos of lane following task
  


### File locations:
#### - [Launch files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/launch)     
#### - [Script files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/scripts)  
#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/videos)

### Work Distribution

<pre>
Vipul Kumbhar 	: Code and h/w transition + readme file  
Akshay Mahajan	: camera data debugging
Ashit Mohanty 	: Environment setup and h/w transition
Manu Srivastava	: lane follower simulations + environment setup
Siddhesh Bagkar	: April tag simulations + environment setup
</pre>
