#!/usr/bin/env python

'''
1st layer
keep forward
rotate with positive acceleration when the right bumper is activated
rotate with negative acceleration when the left bumper is activated
'''

import rospy
from geometry_msgs.msg import Twist
from ca_msgs.msg import Bumper

class LCS():
    def __init__(self):
        self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.bumper = Bumper()
        rospy.Subscriber("bumper", Bumper, self.callback)
            
    def callback(self,messages):
        self.bumper = messages
        
    def run(self):
        rate = rospy.Rate(10)
        vel  = Twist() #initialize
        while not rospy.is_shutdown():
            if (self.bumper.is_left_pressed == False) and (self.bumper.is_right_pressed == False):
                vel.linear.x  = 0.1
                vel.angular.z = 0
                print vel
                self.cmd_vel.publish(vel)
            elif self.bumper.is_right_pressed == True:
                for i in range(500):
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    print vel
                    self.cmd_vel.publish(vel)
            elif self.bumper.is_left_pressed == True:
                for i in range(500):
                    vel.linear.x  = 0
                    vel.angular.z = -0.5
                    print vel
                    self.cmd_vel.publish(vel)
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == True):
                for i in range(500): #6.2sec*0.5rad/sec~Pi
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    self.cmd_vel.publish(vel)
            rate.sleep()
                

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
