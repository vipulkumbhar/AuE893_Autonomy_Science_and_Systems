
def callback(data):
	if under_camera_control==0: #Not under cam control
		global delta
		#Higher values of the the parameters below allow for higher speeds in the death arena
		#Lower value of head on threshold indicates more confidence in driving ability
		Head_on_threshold        = 0.4
		side_obstacle_confidence = 0.7
		#rospy.loginfo(rospy.get_caller_id(), data.ranges)
		x = list(data.ranges)

		f_l      = numpy.array(x[0:30])
		f_l[f_l  == inf] = 3.5
		f_l_dist = sum(f_l)/len(f_l)

		
		f_r      = numpy.array(x[330:360])
		f_r[f_r  == inf] = 3.5
		f_r_dist = sum(f_r)/len(f_r)

		l      = numpy.array(x[30:90])
		l[l    == inf] = 3.5
		l_dist = sum(l)/len(l)

		r = numpy.array(x[270:330])
		r[r == inf] = 3.5
		r_dist = sum(r)/len(r)

		
		delta = l_dist - r_dist

		if min(f_l_dist, f_r_dist) < 3.5: # obstacle ahread
			print "f_l_dist: %.2f f_r_dist: %.2f delta: %.2f" %(f_l_dist,f_r_dist,delta),
			approach  = f_l_dist - f_r_dist
			
			if approach > 1: # Obstacle on the right
				delta = min(3.5,delta + 1/f_r_dist)
			elif approach < -1: #Obstacle on the left
				delta = max(-3.5, delta - 1/f_l_dist)
			else: #Head-on
				
				# delta = random.choice([min(3.5, fwd_wt/f_l_dist), max(-3.5,-1 * fwd_wt/f_l_dist)]) #f_l_dist is the same as f_r_dist
				#Don't over react if the head on collision is not imminent

				if min(f_l_dist,f_r_dist)<Head_on_threshold: #imminent collision
					print "Alert!!!!",	
					if -1*side_obstacle_confidence<delta<side_obstacle_confidence: #No danger of side collision
						print "Delta ignored" ,
						if f_l_dist < f_r_dist:
							delta = -3.5
						elif f_l_dist > f_r_dist:
							delta = +3.5
						else:
							delta = random.choice([-3.5,3.5]) 
					else:
						delta = numpy.sign(delta) * 3.5 #side collision danger
