#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from ca_msgs.msg import Bumper

rospy.init_node("SBC") #Give the node a name

pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
bumper = rospy.Subscriber("bumper", Bumper, queue_size=10)

#Keep going forward and stop when bumper activated
while not rospy.is_shutdown():
    vel  = Twist() #initialize
    vel.linear.x  = 0.1
    print vel
    pub.publish(vel)
