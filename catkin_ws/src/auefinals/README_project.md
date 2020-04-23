
## AuE893 Final Project Gazebo Model

Dependencies that are not included:

* The TB3 packages
* cmvision

To bring up the Gazebo Model:

roslaunch turtlebot3_auefinals turtlebot3_autonomy_finals.launch

The keyboard teleop functionality will be displayed on a new terminal window. Use keyboard to teleop the human.

There are 3 sections to this project:

* Task 1: Wall following/Obstacle avoidance - The Turtlebot starts here. It must successfully follow the wall and avoid the obstacles until it reaches the yellow line.
* Task 2:
- Line following - The Turtlebot must successfully follow the yellow line.
- Stop Sign detection - While navigating the yellow line, the the Turtlebot should stop at the stop sign for 3 seconds before continuing. The stop-sign will be detected by TinyYOLO.
* Task 3: Human tracking - The Turtlebot must use a trained DL network to identify the human in the environment and follow it around. The human in Gazebo can be teleoperated around using the keyboard. This teleoperation is already part of the given Gazebo environment.


This model contains code from the following repositories:

* (Person Simulator) The Construct: https://bitbucket.org/theconstructcore/person_sim/src/master/
* (TB3 model + inpsiration) TB3 Autorace: https://github.com/ROBOTIS-GIT/turtlebot3_autorace_2020.git

Maintainers:

* Adhiti Raman (TA)
