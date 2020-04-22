#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import apriltag
from std_msgs.msg import Int64
mission_stage_msg = 0

class arFollower(object):

    def __init__(self):
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)

    def camera_callback(self,data):
	rospy.loginfo("April tag detector loginfo")
	# We select bgr8 because its the OpneCV encoding by default
	cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
	frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

	# April tag detector	
	tag_detected = False
	detector = apriltag.Detector()
	result = detector.detect(frame)

	tagID = 0
	global mission_stage_msg

	if len(result)==1:
		tag_detected = True
		tag = result[0].tag_family
		tagID = result[0].tag_id
		cx  = result[0].center[0]
		cy  = result[0].center[1]
		corner_points = result[0].corners

	if len(result) > 1:
		print("Multiple tags detected")

	pub2      = rospy.Publisher("/current_tag", Int64, queue_size=1)
	msg2      = Int64()
	msg2.data = 0

	if tag_detected:
		print("Tag detected")
		print('tag ID = ', tagID)
		#print(result)
		# publish current detected tag if any
		msg2.data = tagID
	if tag_detected == False:
		print('No tag detected')
	print('\n')

	# publish mission stage
	if mission_stage_msg == 0 and tagID == 8:
		mission_stage_msg = 1
	if mission_stage_msg == 1 and tagID == 9:
		mission_stage_msg = 2
	if mission_stage_msg == 2 and tagID == 6:
		mission_stage_msg = 3
	if mission_stage_msg == 3 and tagID == 4:
		mission_stage_msg = 4
        
	pub  = rospy.Publisher("/mission_stage", Int64, queue_size=1)
	msg  = Int64()
	msg.data = mission_stage_msg
	pub.publish(msg)
	pub2.publish(msg2)
	    
def main():
    rospy.init_node('april_tag_detector', anonymous=True)
    line_follower_object = arFollower()
    rate = rospy.Rate(10)
    
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        # line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    #while not ctrl_c:
    while not rospy.is_shutdown():
    	rate.sleep()
    
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass
	




