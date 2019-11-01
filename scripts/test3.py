#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

rospy.init_node("forward") #Give the node a name


pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

while not rospy.is_shutdown():
    vel  = Twist() #initialize
    vel  = 0.2
    print vel
    pub.publish(vel)
