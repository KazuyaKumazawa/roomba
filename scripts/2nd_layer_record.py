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
'''

import rospy
import csv
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
        light_l = self.bumper.light_signal_left
        light_fl = self.bumper.light_signal_front_left
        light_cl = self.bumper.light_signal_center_left
        light_cr = self.bumper.light_signal_center_right
        light_fr = self.bumper.light_signal_front_right
        light_r = self.bumper.light_signal_right
        ave_c = (light_cl + light_cr)/2
        ave_l = (light_l + light_fl)/2
        ave_r = (light_r + light_fr)/2
        THRESHOLD = 10
        while not rospy.is_shutdown():
            with open('record.csv', 'a') as r:
                writer = csv.writer(r)
                writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r])
            #1st layer
            if (self.bumper.is_right_pressed == True) and (self.bumper.is_left_pressed == False):
                for i in range(16):
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    print vel
                    self.cmd_vel.publish(vel)
                    rate.sleep()
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == False):
                for i in range(16):
                    vel.linear.x  = 0
                    vel.angular.z = -0.5
                    print vel
                    self.cmd_vel.publish(vel)
                    rate.sleep()
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == True):
                for i in range(62): #6.2sec*0.5rad/sec~Pi
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    print vel
                    self.cmd_vel.publish(vel)
                    rate.sleep()
            else:
                #2nd layer
                if ave_c>THRESHOLD or ave_r>THRESHOLD or ave_l>THRESHOLD: #detect obstacle
                    if (ave_l < ave_c) and (ave_r < ave_c): #obstacle is in front
                        if ave_l > ave_r: #direction of right is more safety
                            vel.linear.x  = 0.05
                            vel.angular.z = -1
                            print vel
                            self.cmd_vel.publish(vel)
                            rate.sleep()
                        else: #direction of left is more safety
                            vel.linear.x  = 0.05
                            vel.angular.z = 1
                            print vel
                            self.cmd_vel.publish(vel)
                            rate.sleep()
                    elif (ave_l > ave_c) and (ave_r < ave_l): #obstacle is in left
                        vel.linear.x  = 0.05
                        vel.angular.z = -0.5
                        print vel
                        self.cmd_vel.publish(vel)
                        rate.sleep()
                    elif (ave_r > ave_c) and (ave_r > ave_l): #obstacle is in right
                        vel.linear.x  = 0.05
                        vel.angular.z = 0.5
                        print vel
                        self.cmd_vel.publish(vel)
                        rate.sleep()
                else:
                    vel.linear.x  = 0.1
                    vel.angular.z = 0
                    print vel
                    self.cmd_vel.publish(vel)
                    rate.sleep()

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
