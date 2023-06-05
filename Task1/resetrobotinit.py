#!/usr/bin/env python3
#chmod u+x ~/catkin_ws/src/beginner_tutorials/src/resetrobotinit.py

import rospy
import sys
from std_srvs.srv import Empty
   	
if __name__ == "__main__":
	try:
		#Return the robots back to their initial position when robot3 reaches p1.
		rospy.init_node('resetinitrobots', anonymous=True)
		set_state = rospy.ServiceProxy('/reset_positions',Empty)
		set_state()
		
	except rospy.ROSInterruptException:
		pass
