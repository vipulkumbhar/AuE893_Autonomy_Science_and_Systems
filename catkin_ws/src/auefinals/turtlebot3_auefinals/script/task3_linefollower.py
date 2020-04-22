#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Int64
from move_robot import MoveTurtlebot3
import apriltag
#from sensor_msgs.msg import CompressedImage

temp    = 0
kp      = 0.08
kd      = 0
ki      = 0.0001
prev_err= 0
err_sum = 0
first_lane_confirmation = False
n       = 0
lane_find_factor = 0 
cy      = 0 
first_signal = True
t1      = 0
stop_time    = 0
traffic_sign_trigger = False

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
	#self.image_sub = rospy.Subscriber('/raspicam_node/image',Image,self.camera_callback) 
        #self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
			
	# We select bgr8 because its the OpneCV encoding by default
	cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
    
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape

	crop_img = cv_image[(height)/2+160:(height)][1:width]
        
	# input for imshow
	tss  =1 #(width/1280)*2.1 
	itss =1 #int((width/1280)*2.5)
	mll  =1 #int(height/4) #Mask uper limit from bottom
        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV

        # Threshold the HSV image to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)

	global first_lane_confirmation
	global n,t1
	global lane_find_factor
	cv_image2 = cv_image
	
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']

            #print
	    rospy.loginfo("\n \n       Mode - Lane following maneuver") 
	    invoke_lane_finder      = False
	    first_lane_confirmation = True

        except ZeroDivisionError:
            cx, cy = height/2, width/2
		
	    #print
	    rospy.loginfo("")
	    invoke_lane_finder = True
	    lane_detected      = False
        
        # Draw the centroid in the resultut image
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(mask,(int(cx), int(cy)), 10,(0,0,255),-1)

	# initiate control parameters
	global temp,kd,kp,ki,prev_err,err_sum
	err = cx - width/2

	#define nodes/message	
	cmd_vel_pub  = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        #self.moveTurtlebot3_object.move_robot(twist_object)
	twist_object = Twist()

	#avoid steady state oscillation
	if err >-5 and err <5:
		err = 0
	
	#lane following maneuver control 
	twist_object.angular.z = np.clip((-float(err)*kp/100 + kd*(-err+prev_err)/100),-0.2,0.2)
	a_temp                 = np.clip((-float(err)*kp/100 + kd*(-err+prev_err)/100),-0.2,0.2)

	twist_object.linear.x  = np.clip(0.2*(1-abs(a_temp)/0.2),0,0.2)
	b_temp                 = np.clip(0.2*(1-abs(a_temp)/0.2),0,0.2)

	#control end
	prev_err = temp
	err_sum  = err_sum+err

	#control to find lane
	t0 = float(rospy.Time.now().to_sec())
	timestep = (-t1+t0)
	if invoke_lane_finder:

		if first_lane_confirmation==False:

			detector = apriltag.Detector()
			frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
			result = detector.detect(frame)
			tag_detected = False
			cx = 0
			cy = 0
			twist_object.linear.x  = 0.1
			twist_object.angular.z = 0.0

			if len(result)>0:
				tag_detected = True
				tag = result[0].tag_family
				cx  = result[0].center[0]
				cy  = result[0].center[1]
				err = cx - width/2
				if err >-5 and err <5:           #avoid steady state oscillation
					err = 0
				twist_object.angular.z = np.clip((-float(err)*0.08/100),-0.2,0.2)
				twist_object.linear.x  = 0.1
				#print(cx, cy)

			rospy.loginfo("Mode - Lane finding maneuver")
			
		if first_lane_confirmation:

			twist_object.linear.x  = np.clip((lane_find_factor*0.05),0,0.08)
			twist_object.angular.z = 0.21
			n = n + timestep*twist_object.angular.z

			if n > 3.14159*1.5 and invoke_lane_finder:
				n = 0
				lane_find_factor = lane_find_factor+1  

			rospy.loginfo("Mode - Lane finding maneuver-2")
			print("       Angle turned by bot=>"+str(n))      
	
	# Time
	t1 = t0
	if a_temp == twist_object.angular.z and b_temp ==twist_object.linear.x: 
		lane_find_factor        = 0
	    	n                       = 0
		
	# Display	
	# Print
        print("\n       Angular value sent=> "+str(float(int(1000*twist_object.angular.z))/1000))
	print("       Linear  value sent=> "+str(float(int(1000*twist_object.linear.x))/1000))
	print("          Lane error     => "+str(int(err*100/width))+" %")
	print("             cx          => "+str(float(int(100*cx))/100)+"\n             cy          => "+str(float(int(100*cy))/100))
	print("        Timestep (sec)   => "+str(float(int(1000*timestep))/1000))
	#print("         Update rate     => "+str(int(1/timestep)))
	print(" \n")

	global traffic_sign_trigger
	global stop_time 

	sub_tf = rospy.Subscriber("/stop_sign", Int64,callback_traffic_sign_status) 
	while traffic_sign_trigger and stop_time <4:
		t0 = float(rospy.Time.now().to_sec())
		stop_time = stop_time+(t0-t1)
		t1   = t0
		rospy.loginfo('stopping for signal')
		rospy.loginfo('stop_time')
		rospy.loginfo(stop_time)
		twist_object.angular.z = 0
		twist_object.linear.x  = 0
		cmd_vel_pub.publish(twist_object)
		rate = rospy.Rate(10)
		rate.sleep()
		
	cmd_vel_pub.publish(twist_object)

    def clean_up(self):
        #self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()   

traffic_sign_trigger = False # false for stop
def callback_traffic_sign_status(msg):
    global traffic_sign_trigger
    traffic_sign =  msg.data
    if traffic_sign ==1:
	traffic_sign_trigger = True
	    
def main():
    rospy.init_node('line_following_node', anonymous=True)  
    line_follower_object = LineFollower()

    rate = rospy.Rate(10)
    #ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        # line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    #rospy.on_shutdown(shutdownhook)
    #while not ctrl_c:
    while not rospy.is_shutdown():
    	rate.sleep()
     
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass





