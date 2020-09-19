# AuE893: Autonomy Science and System

This repository contains the code and assets for Clemson Univeristy course AuE893: Autonomy Science and System for Spring 2020 semester. 

## Information for use of this repository:
1) Clone or download the repository from [link](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar.git)
2) Workspace: Ubuntu 16.04, ROS Kinetic Kame


# Team Name: TMNT (Teenage Mutant Ninja Turtles)	

## Team Number: 03  
### Team Members: <img align="right" width="300" height="226" src="https://raw.githubusercontent.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/master/catkin_ws/git_readme_files/ninja_turtles_PNG55.png">   	
		Akshay Mahajan 
		Ashit Mohanty  
		Manu Srivastava  
		Siddesh Bagkar  
		Vipul Kumbhar  


### [HW2](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment2_ws) TurtleSim basic maneuvers

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment2_ws/video/closedloop_gif.gif)

### [HW3](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment3) TurtleBot3 basic maneuvers and emergency braking

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/git_readme_files/move.gif)

### [HW4](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment4) TurtleBot3 wall follower and obstacle avoidance, simulation and physical implementation 
   
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/gazebo/wall_following.gif)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/turtlebot3burger/wallfollowing_real.gif)


### [HW5](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following) Part 1: Lane detection by camera and lane following by turtlebot3

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/lane_following_gazebo.GIF)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/lane_following.GIF)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/Lane_following_turtlebot.GIF)


### [HW5](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/tb3_line_following) Part 2: April tag detection and follower
   
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/April_tag_following_turtlebot.GIF)

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/tb3_line_following/videos/gifs_for_readme/april_tag_real_bot.gif)
  
### [Final Project](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals)   
   
Final project is made up of main 5 maneuvers.

Wall follower - Turtlebot maintains predefined distance from right-side wall. Proportional controller based on distance from right-side wall is used to control z-angular velocity.

Obstacle avoidance - Turtlebot maintains safe front distance from obstacle and maneuvers through course until it finds yellow lanes.

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/video/final_project_1.gif)

lane follower - Turtlebot follows yellow lane using image-processing (to detect lane center) and proportional controller to control z-angular velocity.

Traffic sign detection - Darknet package is used for traffic sign detection. Traffic sign callback functions stop the turtlebot for 4 seconds.

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/video/final_project_2.gif)

People / leg tracker - People tracker package is used for leg detection. Proportional controller is to control z-angular velocity to guide tutrlebot towards nearest detected leg. If leg is not detected or lost, turtlebot goes into obstacle avoidance mode.

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/video/final_project_3.gif)

