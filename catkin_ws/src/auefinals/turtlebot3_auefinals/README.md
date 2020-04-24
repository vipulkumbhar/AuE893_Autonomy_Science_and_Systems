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
  
  
### Final project - problem solving approaches   
  
Team explored two methodologies for final project
#### Methodology 1: Single script file for all tasks.  
[Script](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script/tb3_gazebo_aue20_ms.py)  
[Launch file](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_main_mission2.launch).     
  
The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch turtlebot3_auefinals turtlebot3_autonomy_final_main_mission2.launch       
```

#### Methodology 2: Distributed task scripts (Individual nodes for each task controlled from main mission control node)   
[Script](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script)  
[Launch file](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch)  
  
The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch turtlebot3_auefinals turtlebot3_autonomy_final_main_mission.launch       
```
  
### Script and launch files information 
  
#### Methodology 1

- Script info: ['tb3_gazebo_aue20_ms.py'](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script/tb3_gazebo_aue20_ms.py) has all mode transitions and all 5 maneuvers which control delta (z-angular velocity) of turtlebot. After initiating node, it waits for 10 seconds for all other launch processes to finish.   
  
- Launch file info: ['turtlebot3_autonomy_final_main_mission2.launch'](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_main_mission2.launch) launches   
1) Gazebo world  
2) People   
3) gmapping slam  
4) darknet_ros (traffic sign detecter)    
5) pi_leg_detector (people/leg detector)   
6) tb3_gazebo_aue20_ms.py script   

#### Methodology 2
- Script info:['main_mission.py'](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script/main_mission.py) launches gmapping slam, april-tag detector callback and mission stage callback. April tag detector node launched from 'turtlebot3_autonomy_final_main_mission.launch' publishes the tagID of april tag detected and mission stage from previous mission stage and currently detected april tag. As per mission stage, it initiates the necessary nodes for task execution.  
For ex. for lane following mission stage, it first launches darknet_ros (traffic sign detecter) and then lane follower node. After finishing each task, the nodes for that task are killed and next nodes are initiated.  

- Launch file info: ['turtlebot3_autonomy_final_main_mission.launch'](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch/turtlebot3_autonomy_final_main_mission.launch) launches  
1) Gazebo world  
2) People 
3) April tag detector
4) main_mission.py script   
  
First 3 launch nodes are essential ones, and main_mission.py controls the launch and shutdown of essential nodes for particular tasks. 
	  
### File locations:
#### - [Launch files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/launch)     
#### - [Script files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/script)  
#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/auefinals/turtlebot3_auefinals/video)

### Work Distribution

<pre>
Vipul Kumbhar 	: Code integration of methodology 2 + readme file + Traffic sign detection code
Akshay Mahajan	: Lane follower code + mode/mission transition code
Ashit Mohanty 	: Gazebo environment setup + Obstacle avoidance code
Manu Srivastava	: Code integration of methodology 1  + people/leg follower code
Siddhesh Bagkar	: April tag detection code + wall follower code
</pre>
