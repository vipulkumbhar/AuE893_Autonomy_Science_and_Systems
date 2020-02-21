# AuE893: Autonomy Science and System

This repository contains the code and assets for Clemson Univeristy course AuE893: Autonomy Science and System for Spring 2020 semester. 

## Information for use of this repository:
1) Clone or download the repository from link: https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar.git
2) Workspace: Ubuntu 16.04, ROS Kinetic Kame

### HW2
link: https://github.com/vipulkumbhar/AuE893Spring20_VipulKumbhar/tree/master/catkin_ws/src/assignment2_ws 

Script      : /AuE893Spring20_VipulKumbhar/catkin_ws/src/assignment2_ws/scripts       
Video       : /AuE893Spring20_VipulKumbhar/catkin_ws/src/assignment2_ws/video  
Launch files: /AuE893Spring20_VipulKumbhar/catkin_ws/src/assignment2_ws/launch  


```python
from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b
```
