# Team Name: TMNT (Teenage Mutant Ninja Turtles)	

## Team Number: 03  
### Team Members: <img align="right" width="300" height="226" src="https://raw.githubusercontent.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/master/catkin_ws/git_readme_files/ninja_turtles_PNG55.png">   	
		Akshay Mahajan 
		Ashit Mohanty  
		Manu Srivastava  
		Siddesh Bagkar  
		Vipul Kumbhar  
		  
### Assignment #5 
  
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
  
#### Part 2:  April tag follower 
- Script info:  wallfollowing.py script is mainly divided in four parts.      

1) Callback(data) : 
<pre>
 Similar to lane follower script, the image is extracted from raspicam_node and run through april tag 
 detector (explained below) to receive x,y image coordinates of tag. If multiple tags are detected  
 warning is sent.
 
 Image y co-ordinate of detected april tag is used as input for proportional controller for turtlebot3
 to follow april tag. 
 
 Define April tag detector: 
 ar_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
		       
Detection of tags in images is done by running the detect method of the detector:
tags = at_detector.detect(img, estimate_tag_pose=False, camera_params=None, tag_size=None)
</pre>


| **Attribute**   	| **Explanation**                                                                                                                                                                                                                                                                                                                                                                                            	|
|-----------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| tag_family      	| The family of the tag.                                                                                                                                                                                                                                                                                                                                                                                     	|
| tag_id          	| The decoded ID of the tag.                                                                                                                                                                                                                                                                                                                                                                                 	|
| hamming         	| How many error bits were corrected? Note: accepting large numbers of corrected errors leads to greatly increased false positive rates. NOTE: As of this implementation, the detector cannot detect tags with a Hamming distance greater than 2.                                                                                                                                                            	|
| decision_margin 	| A measure of the quality of the binary decoding process: the average difference between the intensity of a data bit versus the decision threshold. Higher numbers roughly indicate better decodes. This is a reasonable measure of detection accuracy only for very small tags-- not effective for larger tags (where we could have sampled anywhere within a bit cell and still gotten a good detection.) 	|
| homography      	| The 3x3 homography matrix describing the projection from an "ideal" tag (with corners at (-1,1), (1,1), (1,-1), and (-1, -1)) to pixels in the image.                                                                                                             	|
| center          	| The center of the detection in image pixel coordinates.                                                                                                                                                                                                                                                                                                                                                    	|
| corners         	| The corners of the tag in image pixel coordinates. These always wrap counter-clock wise around the tag.                                                                                                                                                                                                                                                                                                    	|
| pose_R*         	| Rotation matrix of the pose estimate.                                                                                                                                                                                                                                                                                                                                                                      	|
| pose_t*         	| Translation of the pose estimate.                                                                                                                                                                                                                                                                                                                                                                          	|
| pose_err*       	| Object-space error of the estimation.                                                                                                                                                                                                                                                                                                                                                                      	|


- Launch info:   

Launch file name: turtlebot3_follow_line.launch  
<pre>
This launch file launches 'ar_follow.py' from package 'tb3_line_following'.  
Before launching this, make sure that robot bringup node and camera bring-up node is running.
</pre>

The commands that need to be executed to setup turtlebot environment for run are as follows:

```
1] $ roscore          # in remote-pc terminal to start roscore  
2] $ ssh pi@IP        # in remote-pc terminal to SSH robot
3] $ roslaunch turtlebot3_bringup bringup_robot.launch  # in turtlebot terminal to bring up robot
4] $ roslaunch raspicam_node camerav2_1280x720.launch enable_raw:=true # in turtlebot terminal to 
bring up camera and publish raw images
```
The command that need to be executed in remote-pc to run april tag follower is as follow:
```
$ roslaunch tb3_line_following turtlebot3_follow_ar.launch   
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/April_tag_following_turtlebot.GIF)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/april_tag_real_bot.gif)

#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following/videos/april_tag) - Full length videos of april tag following task

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
