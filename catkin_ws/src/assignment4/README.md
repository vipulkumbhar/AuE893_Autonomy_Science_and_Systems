# Team Name: TMNT (Teenage Mutant Ninja Turtles)	

## Team Number: 03  
### Team Members: <img align="right" width="300" height="226" src="https://raw.githubusercontent.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/master/catkin_ws/git_readme_files/ninja_turtles_PNG55.png">   	
		Akshay Mahajan 
		Ashit Mohanty  
		Manu Srivastava  
		Siddesh Bagkar  
		Vipul Kumbhar  
		  
### Assignment #4  
  
### Script and launch files information 
  
#### Part 1:  Launch file name: turtlebot3_wallfollowing.launch 

- Script info: wallfollowing.py script is mainly divided in two parts    
1) Callback(data) : 
<pre>
This callback fuctions reads data from subscribed topic '/scan'. It replaces 'inf' and false '0's 
and gives front wall distance(s_d), left wall distance (y_l), right wall distance (y_r) from pre-
-defined scan range. 
</pre>

2) tmnt_controller(): 
<pre>
tnmt controller subscribes to 'scan' data and gets desired values from callback function. it also
publishes twist msg on topic '/cmd_vel'. For angular velocity in z direction, a PD (proportional 
derivative) controller is used which uses error term defined as ( distance to be maintained from 
wall - distance from wall). This error term and PD controller helps keep turtlebot path parallel 
to right side wall at predefined distance. Linear velocity is inversely proportional distance from
front obstacle and is capped from -0.1 to 0.4. This helps keep turtlebot speed lower during corner
rotate maneuver and high during straight line path.
</pre>
	  
- Launch info: 
<pre>
This launch file first initializes the type of turtlebot. Here it has a default entry of burger. 
Next, the initial coordinates of the turtlebot have been defined. After that, set of commands 
launch the empty.world file in Gazebo and the dynamic parameters of the virtual world are 
initialized. After setting up environment and turtlebot, wallfollowing.py is run with 'assignment4'
package. 
</pre>

The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch assignment4 turtlebot3_wallfollowing.launch       
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/gazebo/wall_following.gif)

The commands that need to be executed in the terminal for turtlebot3 burger run are as follows:

```
$ rosrun assignment4 turtlebot3_wallfollowing.py       
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/turtlebot3burger/wallfollowing_real.gif)

  
#### Part 2:  Launch file name: turtlebot3_obstacleavoidance.launch  
- Script info:  wallfollowing.py script is mainly divided in four parts.      

1) Callback(data) : 
<pre>
This callback fuctions reads data from subscribed topic '/scan'. It replaces 'inf' and false '0's 
and gives front obstacle distance(y_l), left obstacle distance (l_l), right obstacle distance 
(r_l) and back side obstacle distance (y_b) from predefined scan range.  
</pre>
2) wander_controller_move(): 
<pre>
This function is mainly used for straight line maneuvers. Linear velocity is proportional to 
difference between front obstacle(y_l) and front safe distance (front_limit). It is controlled by 
prportional gain of 1/5 and is capped between -0.2 to 0.5. it also added angular velocity opposite 
object detected in right or left side provided that front obstacle distance is greater than front 
safe limit. If front obstacle distance is lower than front safe limit, this function breaks and 
call wander_controller_rotate() function.  
</pre>
3) wander_controller_rotate(): 
<pre>
This functions rotates the turtlebot until front obstacle distance is greater than safe limit and 
also if there are not any obstacle in immediate front-left or front-right vicinity. If these 
conditions are satisfied then the function breaks and calls wander_controller_move() function.
</pre>
4) stuck(): 
<pre>
If turtlebots front obstacle distance or back side obstacle distance is lower than safe limit and 
there is not place to rotate then these situations calls stuck() function. Which publishes 
negative or positive linear velocity until there is enough space for turtlebot to rotate.
</pre>
	  
- Launch info: 
<pre>
This launch file first initializes the type of turtlebot. Here it has a default entry of burger. 
Next, the initial coordinates of the turtlebot have been defined. After that, set of commands 
launch the empty.world file in Gazebo and the dynamic parameters of the virtual world are 
initialized. After setting up environment and turtlebot, wanderfast.py is run with 'assignment4'
package. 
</pre>

The commands that need to be executed in the terminal for gazebo simulation are as follows:

```
$ roslaunch assignment4 turtlebot3_obstacleavoidance.launch    
```
![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/gazebo/obstacle_avoidance.gif)

The commands that need to be executed in the terminal for turtlebot3 burger run are as follows:

```
$ rosrun assignment4 turtlebot3_wander.py       
```

![Watch the video](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/blob/master/catkin_ws/src/assignment4/video/turtlebot3burger/obstacleavoidance_real.gif)

### File locations:
#### - [Launch files](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment4/launch)     
#### - Script files    
[1) Gazebo](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment4/script)     
[2) Turtlebot3 burger](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment4/src)      
#### - [Videos](https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment4/video)

### Work Distribution

<pre>
Vipul Kumbhar 	: Wallfollowing, obstacle avoidance scripts and launch files  
Akshay Mahajan	:  
Ashit Mohanty 	:  
Manu Srivastava	:   
Siddhesh Bagkar	:  
</pre>
