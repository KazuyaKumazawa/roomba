#!/usr/bin/env python
#Keep going forward and stop when bumper activated
import rospy
from geometry_msgs.msg import Twist
from ca_msgs.msg import Bumper

rospy.init_node("GoAndStop") #Give the node a name

pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

def maim():
    sub = rospy.Subscriber("bumper", Bumper, callback)
    while not rospy.is_shutdown():
        vel  = Twist() #initialize
        vel.linear.x  = 0.1
        print vel
        pub.publish(vel)

def callback(bumper):
    print bumper
    stop_vel = Twist()
    stop_vel.linear.x = 0
    rate = rospy.Rate(10.0)
    for i in range(5):
        pub.publish(stop_vel)
        rate.sleep()

if __name__ == "__main__":
    main()
