#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3
from sensor_msgs.msg import CompressedImage

temp    = 0
kp      = 0.08
kd      = 0
ki      = 0.0001
prev_err= 0
err_sum = 0
first_lane_confirmation = False
n       = 0
lane_find_factor = 0 
t1      = 0

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
	#self.bridge_object = CvBridge.compressed_imgmsg_to_cv2() 

        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
	#self.image_sub = rospy.Subscriber('/raspicam_node/image',Image,self.camera_callback) 
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
        
	# We select bgr8 because its the OpneCV encoding by default
	cv_image  = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
	#cv_image  = self.bridge_object.compressed_imgmsg_to_cv2(data, desired_encoding="bgr8")

	cv_image2 = cv_image.copy()
	
	#check if white lane works
	#cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
	#filter too bright light
	#ret,cv_image = cv2.threshold(cv_image,200,255,cv2.THRESH_TOZERO_INV)
	#cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)		

        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape

	tss  = (width/1280)*2.1 
	itss = int((width/1280)*2.5)
	mll  = int(height/4) #Mask uper limit from bottom

        #crop_img = cv_image[(height)/2+100:(height)/2+120][1:width]
	crop_img = cv_image[(height)/2+mll:(height)][1:(width)]
        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV
        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
        """
        # Threshold the HSV image to get only yellow colors
        #lower_yellow = np.array([20,100,100])
        #upper_yellow = np.array([50,255,255])

	# Threshold the HSV image to get only white colors
	lower_yellow = np.array([0,0,90])
        upper_yellow = np.array([172,70,150])


        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)

	global first_lane_confirmation
	global n,t1
	global lane_find_factor
	
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']

            #print
	    rospy.loginfo("\n \n       Mode - Lane following maneuver") 
	    cv_image2 = cv2.putText(cv_image2,'Mode: Lane following maneuver',(int(20*tss),int(23*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.5*tss,(0,0,255),1*itss, cv2.LINE_AA)
	    invoke_lane_finder      = False
	    first_lane_confirmation = True

        except ZeroDivisionError:
            cx, cy = height/2, width/2
		
	    #print
	    rospy.loginfo("")
	    invoke_lane_finder = True
        
        # Draw the centroid in the resultut image
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(mask,(int(cx), int(cy)), 10,(0,0,255),-1)

	# initiate control parameters
	global temp,kd,kp,ki,prev_err,err_sum
	err = cx - width/2

	# lane finding rotation direction

	#define nodes/message	
	cmd_vel_pub  = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	twist_object = Twist()

	#avoid steady state oscillation
	if err >-5 and err <5:
		err = 0
	
	#lane following maneuver control 
	twist_object.angular.z = np.clip((-float(err)*kp/100 + kd*(-err+prev_err)/100),-0.2,0.2)
	a_temp                 = np.clip((-float(err)*kp/100 + kd*(-err+prev_err)/100),-0.2,0.2)

	twist_object.linear.x  = np.clip(0.2*(1-abs(a_temp)/0.2),0,0.08)
	b_temp                 = np.clip(0.2*(1-abs(a_temp)/0.2),0,0.08)

	#control end
	prev_err = temp
	err_sum  = err_sum+err

	#control to find lane
	t0 = float(rospy.Time.now().to_sec())
	timestep = (-t1+t0)
	if invoke_lane_finder:

		if first_lane_confirmation==False:

			print("       Mode - Lane finding maneuver")
			cv_image2 = cv2.putText(cv_image2,'Mode: Lane finding maneuver-1',(int(20*tss),int(23*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.5*tss,(0,0,255),1*itss, cv2.LINE_AA)
		twist_object.linear.x  = 0.1
		twist_object.angular.z = 0.02


		if first_lane_confirmation:

			twist_object.linear.x  = np.clip((lane_find_factor*0.05),0,0.08)
			twist_object.angular.z = 0.21
			n = n + timestep*twist_object.angular.z

			if n > 3.14159*1.5 and invoke_lane_finder:
				n = 0
				lane_find_factor = lane_find_factor+1  

			print("       Mode - Lane finding maneuver-2")
			cv_image2 = cv2.putText(cv_image2,'Mode: Lane finding maneuver-2',(int(20*tss),int(23*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.5*tss,(0,0,255),1*itss, cv2.LINE_AA)
			print("       Angle turned by bot=>"+str(n))      
	
	# Time
	t1 = t0
	if a_temp == twist_object.angular.z and b_temp ==twist_object.linear.x: 
		lane_find_factor        = 0
	    	n                       = 0
	
	# Debugging camera and lane finder
	#twist_object.angular.z = 0
	#twist_object.linear.x  = 0
		
	cmd_vel_pub.publish(twist_object)

	# Display
	cv_image2 = cv2.rectangle(cv_image2,(int(10*tss),int(5*tss)),(int(290*tss),int(100*tss)),(0,250, 0),2*int(tss))
        #cv_image= cv2.putText(cv_image,str(mode),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1, cv2.LINE_AA)
	msg1     = str("Lane  error            " + str(int(err*100/width))+" %")
	cv_image2 = cv2.putText(cv_image2,msg1,(int(20*tss),int(45*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.4*tss,(0,255,0),1*itss, cv2.LINE_AA)

	msg2     = str("Linear  velocity        " + str(float(int(1000*twist_object.linear.x))/1000))
	cv_image2 = cv2.putText(cv_image2,msg2,(int(20*tss),int(60*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.4*tss,(0,255,0),1*itss, cv2.LINE_AA)

	msg3     = str("Angular velocity        " + str(float(int(1000*twist_object.angular.z))/1000))
	cv_image2 = cv2.putText(cv_image2,msg3,(int(20*tss),int(75*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.4*tss,(0,255,0),1*itss, cv2.LINE_AA)

	msg4     = str("Update time (ms)     " + str((int(1000*timestep))))
        cv_image2 = cv2.putText(cv_image2,msg4,(int(20*tss),int(90*tss)),cv2.FONT_HERSHEY_SIMPLEX,0.4*tss,(0,255,0),1*itss, cv2.LINE_AA)

	cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
	mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	image_vertical_concat = np.concatenate((mask2,cv_image2), axis=0)
	cv2.imshow('Original', image_vertical_concat)

	# uncomment below to see two diffent image windows
	#cv2.imshow("Original", cv_image)
	cv2.resizeWindow('Original', (800,800))
	#cv2.moveWindow("Original", 40,40)
        #cv2.imshow("MASK", mask)
        cv2.waitKey(1)

	# Print
        print("\n       Angular value sent=> "+str(float(int(1000*twist_object.angular.z))/1000))
	print("       Linear  value sent=> "+str(float(int(1000*twist_object.linear.x))/1000))
	print("          Lane error     => "+str(int(err*100/width))+" %")
	print("             cx          => "+str(float(int(100*cx))/100)+"\n             cy          => "+str(float(int(100*cy))/100))
	print("        Timestep (sec)   => "+str(float(int(1000*timestep))/1000))
	print("         Update rate     => "+str(int(1/timestep)))
	print(" \n")
	
        # Make it start turning
        self.moveTurtlebot3_object.move_robot(twist_object)
        
    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()       

def main():
    rospy.init_node('line_following_node', anonymous=True)
    #rospy.wait_for_message("/camera/rgb/image_raw", Image)
       
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
