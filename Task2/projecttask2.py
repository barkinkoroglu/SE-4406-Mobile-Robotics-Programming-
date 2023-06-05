#! /usr/bin/env python3
#chmod u+x ~/catkin_ws/src/beginner_tutorials/src/projecttask2.py

import sys
import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

nodeid=str(sys.argv[1])
nodename = 'robot_'+nodeid  
#Barkın Köroğlu - 18070001047

vel_msg = Twist()
vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0
obstacle = False
hitground = 0

def go_toPosition2(godistance):
	vel_msg=Twist()
	speed = 0.3
	distance = godistance
	vel_msg.linear.x=abs(speed)
	vel_msg.angular.z=0.0
	rate = rospy.Rate(1000)
	t0=rospy.Time.now().to_sec()
	current_dist = 0
	while current_dist < distance:
		pub.publish(vel_msg)
		t1=rospy.Time.now().to_sec()
		current_dist=speed*(t1-t0)
		rate.sleep()
	vel_msg.linear.x = 0
	vel_msg.angular.z = 0
	pub.publish(vel_msg)

def rotatetask(speed, angle, clockwise, lspeed=0.0):
	vel_msg=Twist()
	#vel_msg.linear.x=0
	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	
	angularspeed = speed * float((math.pi)/180)
	vel_msg.angular.z= float(clockwise*abs(angularspeed))
	rate2 = rospy.Rate(10)
	t0=rospy.Time.now().to_sec()
	current_angle = 0
	relativeangle = float(angle*(math.pi)/180)
	while current_angle < relativeangle:
		pub.publish(vel_msg)
		t1= rospy.Time.now().to_sec()
		current_angle= float(angularspeed*(t1-t0))
		#rate2.sleep()
	vel_msg.linear.x=0
	vel_msg.angular.z=0
	pub.publish(vel_msg)
	
# 0 -270 stage
# 0 -360 gazebo 
def callback(msg): #default value without obstacles is 5.
	global obstacle 
	obstacle = False
	for i in range(len(msg.ranges)):
		#We look at the values of the robot's sensors
		#between 120 and 150 degrees
		if (i>= 120 and i<=150):
			if nodename == 'robot_1':
				#The range value that Robot2 will look at is 1.0
				rangeobs = 1.0
			else:
				#The range value that Robot1 will look at is 0.5
				rangeobs = 0.5
			#if the value taken by the robot's sensor(between 120 and 150 degrees) is smaller than the range value the robot looks at(0.5 or 1.0)
			#It indicates that the robot has come so close to the obstacle.(0.5 or 1.0)
			if(msg.ranges[i] < rangeobs):
				#To avoid hitting the obstacle.
				obstacle = True
			#pub.publish(vel_msg)
	if(obstacle):
		vel_msg.linear.x = 0.0
		vel_msg.angular.z = 0.0
		#Set the hitground value to 1.
		global hitground
		hitground = 1
		
	else:
		#If the sensor does not detect an obstacle at any desired range for now,
		#the robot goes straight ahead
		if(hitground == 0):
			vel_msg.linear.x = 0.3
			vel_msg.angular.z = 0.0
	
	pub.publish(vel_msg)

rospy.init_node("robotmotion", anonymous=True)
pub = rospy.Publisher(nodename+'/cmd_vel', Twist, queue_size=10)

sub = rospy.Subscriber(nodename+'/base_scan', LaserScan, callback)

flag = 0
#For Robot2
if nodename == "robot_1":
	#Total number of turns and moves(for R2) 
	rotateturn = 4
	#1 means rotate left
	movetemp = 1
	#For robot2-> R = 2
	robotgodistance = rospy.get_param('R2')

#For Robot1
else:
	#Total number of turns and moves(for R1) 
	rotateturn = 5
	#-1 means rotate right
	movetemp = -1
	#For robot1-> R = 3
	robotgodistance = rospy.get_param('R1')	

while (flag<rotateturn):
	#Do nothing until robot reach the desired range of the obstacle.
	while(hitground == 0):
		pass
	#When robot detect the obstacle  
	#Rotate 90 degree, if movetemp=1 -> rotate left, movemtemp = -1 > rotate right
	rotatetask(10.0, 90, movetemp)
	#Robot goes as far as R value -> robotgodistance.
	go_toPosition2(robotgodistance)
	#Rotate 90 degree with same movetemp
	rotatetask(10.0, 90, movetemp)
	
	#The robot will make its next turn in reverse.
	#For example, if it turned left before, it will now turn right.
	if movetemp == -1:
		movetemp = 1
	else:
		movetemp = -1
	
	hitground = 0
	flag = flag +1
#When the total number of turns and moves is over.
#Wait until the robot detects the obstacle.	
while (hitground == 0):
	pass
#Stop because robot reaches the end point (Figure 2 in final task2)
sub.unregister()
#rospy.spin()
