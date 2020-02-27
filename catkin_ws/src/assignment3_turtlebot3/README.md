# Team Name: TMNT (Teenage Mutant Ninja Turtles)	

## Team Number: 03  
### Team Members: <img align="right" width="300" height="226" src="https://raw.githubusercontent.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/master/catkin_ws/git_readme_files/ninja_turtles_PNG55.png">   	
		Akshay Mahajan 
		Ashit Mohanty  
		Manu Srivastava  
		Siddesh Bagkar  
		Vipul Kumbhar  
		  
### Assignment #3  
  
### Launch Files  
  
#### Part 1:  Launch file name: move.launch  
	
	- This launch file first initializes the type of turtlebot. Here it has a default entry of burger.  
	Next, the initial coordinates of the turtlebot have been defined.    
	After that, set of commands launch the empty.world file in Gazebo and  
	the dynamic parameters of the virtual world are initialized.   
	  
	- An argument has been declared with name 'code' that defaults to 'circle' and can accept  
	'square' and 'circle' as args to run square.py and circle.py, respectively.
	  
	The commands that need to be executed in the terminal are as follows:
  
```
$ roslaunch assignment3_turtlebot3 move.launch code:=square    #for running square.py
	  
$ roslaunch assignment3_turtlebot3 move.launch code:=circle    #for running circle.py
```
  
#### Part 2:  Launch file name: emergency_braking.launch
	   
	- This launch file first initializes the type of turtlebot. Here it has a default entry of burger.  
	Next, the initial coordinates of the turtlebot have been defined.  
	  
	- A world in Gazebo has been created with a single wall facing the turtlebot and   
	the dynamic parameters of the virtual world have been initialized.  
	  
	- Next the roslaunch command is executed to run the file emergency_brake.py and   
	execute the "emergency brake" maneuver. THe implementation involved creating of 2 threads  
	- once for publishing the velocity commands and once for sensing the LIDAR data.  
	Upon imminent impact, a global flag is set, which in turn signals to the publisher to send the   
	brake command to the bot.
  
	The command that need to be executed in the terminal are as follows:
``` 
$ roslaunch assignment3_turtlebot3 emergency_braking.launch    #for running emergency_brake.py
```
  
### Work Distribution

<pre>
Vipul Kumbhar 	: LiDAR data processing, Recording Videos and writing README.md   
Akshay Mahajan	: Creating move.launch file  
Ashit Mohanty 	: Emergency Braking Maneuver python code  
Manu Srivastava	: Creating Gazebo environment, modifying circle.py and square.py and pushing into repo  
Siddhesh Bagkar	: Creating turtlebot3_wall.launch file  
</pre>
