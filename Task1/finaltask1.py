#!/usr/bin/env python3
#chmod u+x ~/catkin_ws/src/beginner_tutorials/src/finaltask1.py

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
from tf.transformations import euler_from_quaternion,quaternion_from_euler
import sys
import time
from std_srvs.srv import Empty

#Barkin Koroglu - 18070001047
robot0x = 0.0 #p1->x
robot0y = 0.0 #p1->y
robot1x = 0.0 #p2->x
robot1y = 0.0 #p2->y
robot2x = 0.0 #p3->x
robot2y = 0.0 #p3->y
	
class Stagerobot:

	def __init__(self,nodename):
		self.vel_publisher = rospy.Publisher(nodename+'/cmd_vel', Twist, queue_size=10)
		self.pose_subscriber = rospy.Subscriber(nodename+'/odom', Odometry, self.update_pose)

		self.odom = Odometry()
		self.pose = self.odom.pose.pose
		self.rate = rospy.Rate(10)
		self.temp = 0
		self.roll = self.pitch = self.yaw = 0.0

	def update_pose(self, data):
		self.pose = data.pose.pose
		#print(self.pose)
		orientation_q = self.pose.orientation
		#bu local variable 
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		
		(self.roll, self.pitch, self.yaw) = euler_from_quaternion (orientation_list)
		#print self.yaw
		#rospy.loginfo(str(self.pose.position.x), str (self.pose.position.y))


	def euclidean_distance(self, goal_pose):
		return sqrt(pow((goal_pose.position.x-self.pose.position.x),2)+pow((goal_pose.position.y-self.pose.position.y),2))


	def linear_vel(self, goal_pose, constant=1.5):
		return constant * self.euclidean_distance(goal_pose)

	def steering_angle(self, goal_pose):
		return atan2(goal_pose.position.y-self.pose.position.y, goal_pose.position.x-self.pose.position.x)

	def angular_vel(self, goal_pose, constant=2.0):
		return constant * (self.steering_angle(goal_pose)-self.yaw)

	def move2goal(self,goalx,goaly):
		newodom = Odometry()
		goal_pose = newodom.pose.pose
		goal_pose.position.x = goalx  
		goal_pose.position.y = goaly 
		dist_tolerance = 0.1 
		vel_msg = Twist()
		while self.euclidean_distance(goal_pose) >= dist_tolerance:

			vel_msg.linear.x = self.linear_vel(goal_pose)
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = self.angular_vel(goal_pose)
			self.vel_publisher.publish(vel_msg)
			self.rate.sleep()
		vel_msg.linear.x = 0
		vel_msg.angular.z = 0
		self.vel_publisher.publish(vel_msg)
		#rospy.spin()
		
def update_pose1(msg):
		global robot0x
		global robot0y
		robot0x = msg.pose.pose.position.x
		robot0y = msg.pose.pose.position.y
		
def update_pose2(msg):
		global robot1x
		global robot1y
		robot1x = msg.pose.pose.position.x
		robot1y = msg.pose.pose.position.y
def update_pose3(msg):
		global robot2x
		global robot2y
		robot2x = msg.pose.pose.position.x
		robot2y = msg.pose.pose.position.y
		
		    	
if __name__ == "__main__":
	try:
		
		rospy.init_node('stagetogoal', anonymous=True)
		r = rospy.Rate(40)
		#We listen to each other's odom topic.
		#We learn where the robots are now.
		odomsubscriber = rospy.Subscriber("robot_0/odom",Odometry, update_pose1) #robot1
		odomsubscriber2 = rospy.Subscriber("robot_1/odom",Odometry, update_pose2) #robot2
		odomsubscriber3 = rospy.Subscriber("robot_2/odom",Odometry, update_pose3) #robot3
		r.sleep()
		#Printing initial positions.
		print("Robot1 initial position", robot0x,robot0y)
		print("Robot2 initial position", robot1x,robot1y)
		print("Robot3 initial position", robot2x,robot2y)
		#Since robot1 will go to the first initial position of robot2, robot3 needs to save the initial position of robot1.
		#We get the robot1 initial position from subscribing robot_0/odom -> robot0x, robot0y
		#Now we can be unregister from the odom topic of Robot1 because we have already learned the initial position.
		odomsubscriber.unregister()
		r.sleep()
		
		x = Stagerobot("robot_0")
		#I adjusted the position to go so that the robots do not collide with each other.
		robot1x = robot1x - 1
		robot1y = robot1y + 1
		#robot1 goes to the initial position of robot2
		x.move2goal(robot1x,robot1y)
		
		y = Stagerobot("robot_1")
		#I adjusted the position to go so that the robots do not collide with each other.
		robot2x = robot2x + 2
		#robot2 goes to the initial position of robot3
		y.move2goal(robot2x,robot2y)
		
		z = Stagerobot("robot_2")
		#robot3 goes to the initial position of robot1
		z.move2goal(robot0x,robot0y)
		
		#Return the robots back to their initial position when robot3 reaches p1.
		#set_state = rospy.ServiceProxy('/reset_positions',Empty)
		#set_state()
		
	except rospy.ROSInterruptException:
		pass
