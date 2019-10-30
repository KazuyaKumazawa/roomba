#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

rospy.init_node("sample")

pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

while not rospy.is_shutdown():
    vel  = Twist()

    direction = raw_input("f: forward, b: backward, l: left, r: right, s: stop,  q: quit > ")

    if "f" in direction:
        vel.linear.x = +0.1

    if "b" in direction:
        vel.linear.x = -0.1

    if "l" in direction:
        vel.angular.z = +1.0

    if "r" in direction:
        vel.angular.z = -1.0

    if "s" in direction:
        vel.linear.x = 0.0
        vel.angular.z = 0.0

    if "q" in direction:
        break

    print vel

    pub.publish(vel)
