#!/usr/bin/env python

'''
1st layer
Keep forward
Rotate with positive acceleration when the right bumper is activated
Rotate with negative acceleration when the left bumper is activated
Change direction to the opposite when the right and left bumper is activated
2nd layer
Based on the sum of light_signal_left and light_signal_front_left, 
light_signal_center_left and light_signal_center_right, 
and light_signal_front_right and light_signal_right, 
change the direction to avoid obstacles
Velocity, angular velocity are constant
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
        vel  = Twist()
        while not rospy.is_shutdown():
            #1st layer
            if (self.bumper.is_left_pressed == False) and (self.bumper.is_right_pressed == False):
                vel.linear.x  = 0.1
                vel.angular.z = 0
                print vel
            elif self.bumper.is_right_pressed == True:
                vel.linear.x  = 0
                vel.angular.z = 0.5
                print vel
            elif self.bumper.is_left_pressed == True:
                vel.linear.x  = 0
                vel.angular.z = -0.5
                print vel
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == True):
                for i in range(62): #6.2sec*0.5rad/sec~Pi
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    self.cmd_vel.publish(vel)
            #2nd layer
            light_l = self.bumper.light_signal_left
            light_fl = self.bumper.light_signal_front_left
            light_cl = self.bumper.light_signal_center_left
            light_cr = self.bumper.light_signal_center_right
            light_fr = self.bumper.light_signal_front_right
            light_r = self.bumper.light_signal_right
            THRESHOLD = 500
            if light_l>THRESHOLD or light_fl>THRESHOLD or light_cl or light_cr>THRESHOLD or light_fr>THRESHOLD or light_r>THRESHOLD: #detect obstacle
                if (light_l + light_fl < light_cl + light_cr) and (light_r + light_fr < light_cl + light_cr): #obstacle is in front
                    if light_l + light_fl > light_r + light_fr: #direction of right is more safety
                        vel.linear.x  = 0.1
                        vel.angular.z = -1
                        print vel
                    else: #direction of left is more safety
                        vel.linear.x  = 0.1
                        vel.angular.z = 1
                        print vel
                elif (light_l + light_fl > light_cl + light_cr) and (light_r + light_fr < light_l + light_fl): #obstacle is in left
                    vel.linear.x  = 0.1
                    vel.angular.z = -1
                    print vel
                elif (light_r + light_fr > light_cl + light_cr) and (light_r + light_fr > light_l + light_fl): #obstacle is in right
                    vel.linear.x  = 0.1
                    vel.angular.z = 1
                    print vel
            self.cmd_vel.publish(vel)
            rate.sleep()
                

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
