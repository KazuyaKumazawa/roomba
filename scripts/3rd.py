#!/usr/bin/env python
# coding: UTF-8

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
3rd layer
Based on IR sensor,
go to dock (original algorithm)
'''

import rospy
import csv
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ca_msgs.msg import Bumper
from std_msgs.msg import UInt16

class LCS():
    def __init__(self):
        self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.dock = rospy.Publisher("dock", Empty, queue_size=10)
        self.bumper = Bumper()
        rospy.Subscriber("bumper", Bumper, self.callback_bumper)
        self.ir_omni = UInt16()
        rospy.Subscriber("ir_omni", UInt16, self.callback_ir)
            
    def callback_bumper(self,messages):
        self.bumper = messages
    def callback_ir(self,messages):
        self.ir_omni = messages
        
    def run(self):
        rate = rospy.Rate(10)
        vel  = Twist()
        light_l = self.bumper.light_signal_left
        light_fl = self.bumper.light_signal_front_left
        light_cl = self.bumper.light_signal_center_left
        light_cr = self.bumper.light_signal_center_right
        light_fr = self.bumper.light_signal_front_right
        light_r = self.bumper.light_signal_right
        THRESHOLD_2 = 10
        THRESHOLD_3 = 20
        ir = self.ir_omni.data
        while not rospy.is_shutdown():
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
            ir = self.ir_omni.data
            #3rd layer (ir_omni is derived from dock, so 3ed layer has priority)
            if (ir == 172): #go for dock
                vel.linear.x  = 0.15
                vel.angular.z = 0
                self.cmd_vel.publish(vel)
                print '3rd layer'
                with open('record.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                rate.sleep()
            elif (ir == 164): #Green Buoy
                vel.linear.x  = 0.15
                vel.angular.z = -0.5
                self.cmd_vel.publish(vel)
                print '3rd layer'
                with open('record.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                rate.sleep()
            elif (ir == 168): #Red Buoy
                vel.linear.x  = 0.15
                vel.angular.z = 0.5
                self.cmd_vel.publish(vel)
                print '3rd layer'
                with open('record.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                rate.sleep()
            elif (ir == 161) or (ir == 173) or (ir == 165) or (ir == 169): #near dock
                vel.linear.x  = 0
                vel.angular.z = 0
                self.cmd_vel.publish(vel)
                print '3rd layer'
                print 'gooooooooal!'
                with open('record.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                rate.sleep()
                break
            #1st layer
            elif (self.bumper.is_right_pressed == True) and (self.bumper.is_left_pressed == False):
                for i in range(16):
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    with open('record.csv', 'a') as r:
                        writer = csv.writer(r)
                        writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                    self.cmd_vel.publish(vel)
                    print '1st layer'
                    rate.sleep()
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == False):
                for i in range(16):
                    vel.linear.x  = 0
                    vel.angular.z = -0.5
                    with open('record.csv', 'a') as r:
                        writer = csv.writer(r)
                        writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                    self.cmd_vel.publish(vel)
                    print '1st layer'
                    rate.sleep()
            elif (self.bumper.is_left_pressed == True) and (self.bumper.is_right_pressed == True):
                for i in range(62): #6.2sec*0.5rad/sec~Pi
                    vel.linear.x  = 0
                    vel.angular.z = 0.5
                    with open('record.csv', 'a') as r:
                        writer = csv.writer(r)
                        writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                    self.cmd_vel.publish(vel)
                    print '1st layer'
                    rate.sleep()
            #2nd layer
            elif (ave_c>THRESHOLD_2) or (ave_r>THRESHOLD_2) or (ave_l>THRESHOLD_2): #detect obstacle
                if (ave_l < ave_c) and (ave_r < ave_c): #obstacle is in front
                    if ave_l > ave_r: #direction of right is more safety
                        vel.linear.x  = 0.05
                        vel.angular.z = -1
                        with open('record.csv', 'a') as r:
                            writer = csv.writer(r)
                            writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r])
                        self.cmd_vel.publish(vel)
                        print '2nd layer'
                        rate.sleep()
                    else: #direction of left is more safety
                        vel.linear.x  = 0.05
                        vel.angular.z = 1
                        with open('record.csv', 'a') as r:
                            writer = csv.writer(r)
                            writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                        self.cmd_vel.publish(vel)
                        print '2nd layer'
                        rate.sleep()
                elif (ave_l > ave_c) and (ave_r < ave_l): #obstacle is in left
                    vel.linear.x  = 0.05
                    vel.angular.z = -0.5
                    with open('record.csv', 'a') as r:
                        writer = csv.writer(r)
                        writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                    self.cmd_vel.publish(vel)
                    print '2nd layer'
                    rate.sleep()
                elif (ave_r > ave_c) and (ave_r > ave_l): #obstacle is in right
                    vel.linear.x  = 0.05
                    vel.angular.z = 0.5
                    with open('record.csv', 'a') as r:
                        writer = csv.writer(r)
                        writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                    self.cmd_vel.publish(vel)
                    print '2nd layer'
                    rate.sleep()
            else:
                vel.linear.x  = 0.1
                vel.angular.z = 0
                with open('record.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.bumper.is_left_pressed, self.bumper.is_right_pressed, light_l, light_fl, light_cl, light_cr, light_fr, light_r, ir])
                self.cmd_vel.publish(vel)
                print '2nd layer'
                rate.sleep()
            
            
            

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
