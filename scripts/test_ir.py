#!/usr/bin/env python

import rospy
import csv
import re  #seikihyougennsousa
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ca_msgs.msg import Bumper
from std_msgs.msg import UInt16

class LCS():
    def __init__(self):
        self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.dock = rospy.Publisher("dock", Empty, queue_size=10)
        self.bumper = Bumper()
        rospy.Subscriber("bumper", Bumper, self.callback)
        self.ir_omni = UInt16()
        rospy.Subscriber("ir_omni", UInt16, self.callback)
            
    def callback(self,messages):
        self.bumper = messages
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
        ir = self.ir_omni
        while not rospy.is_shutdown():
            for i in range(256):
                vel.linear.x  = 0
                vel.angular.z = 0.5
                num = re.sub(r'\D', '', "self.ir_omni") #tyuusyutu
                print num
                with open('ir.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, self.ir_omni, ir])
                self.cmd_vel.publish(vel)
                rate.sleep()    
            
#            if self.ir_omni is 'data:0':
#                vel.linear.x  = 0
#                vel.angular.z = 0.5
#                print self.ir_omni
#                with open('ir.csv', 'a') as r:
#                    writer = csv.writer(r)
#                    writer.writerow([vel.linear.x, vel.angular.z, self.ir_omni, ir])
#                self.cmd_vel.publish(vel)
#                rate.sleep()
#            else:
#                for i in range(20):
#                    vel.linear.x  = 0
#                    vel.angular.z = 0
#                    print self.ir_omni
#                    print ("3rd layer activated")
#                    with open('ir.csv', 'a') as r:
#                        writer = csv.writer(r)
#                        writer.writerow([vel.linear.x, vel.angular.z, self.ir_omni, ir, "3rd layer activated"])
#                    self.cmd_vel.publish(vel)
#                    rate.sleep()
                    
            

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
