#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3
import apriltag

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/raspicam_node/image",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):

	#define nodes/message	
	cmd_vel_pub  = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	twist_object = Twist()

	# initial cmd_vel
	twist_object.linear.x   = 0
	twist_object.angular.z  = 0

	rospy.loginfo("")

	# We select bgr8 because its the OpneCV encoding by default
	cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
	height, width, channels = cv_image.shape
	tss  = (width/1280)*2.1 
	itss = int((width/1280)*2.5)
	mll  = int(height/4) #Mask uper limit from bottom

	## AR TAG DETECTION AND CONTROL

	height, width, channels = cv_image.shape
	frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

	# April tag detector	
	detector = apriltag.Detector()
	result = detector.detect(frame)
	tag_detected = False

	if len(result)==1:
		tag_detected = True
		tag = result[0].tag_family
		cx  = result[0].center[0]
		cy  = result[0].center[1]
		corner_points = result[0].corners
		print(cx, cy,)

	if len(result) > 1:
		print("multiple tags detected")

	if tag_detected:
		print("tag detected")	

	# Control
	err = 0
	if tag_detected:
		print("Mode: Tag following")
		err = cx - width/2
		if err >-5 and err <5:           #avoid steady state oscillation
			err = 0
		twist_object.angular.z = np.clip((-float(err)*0.08/100),-0.2,0.2) 
		twist_object.linear.x  = 0.1

	if tag_detected == False:
		print("Mode: Tag finding")
		twist_object.linear.x   = 0
		twist_object.angular.z  = 0.2

	# Show image

	cv2.imshow("Image window", cv_image)
	cv2.waitKey(1)

	

        # Make it start turning  
        self.moveTurtlebot3_object.move_robot(twist_object)
	print("\n")
        
    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()
        
def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()

    
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()
  
if __name__ == '__main__':
    main()
