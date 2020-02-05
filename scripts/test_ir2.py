#!/usr/bin/env python

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
            
#    def callback(self,messages):
#        self.bumper = messages
#        self.ir_omni = messages
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
        ir = self.ir_omni
        while not rospy.is_shutdown():
            light_l = self.bumper.light_signal_left
            light_fl = self.bumper.light_signal_front_left
            light_cl = self.bumper.light_signal_center_left
            light_cr = self.bumper.light_signal_center_right
            light_fr = self.bumper.light_signal_front_right
            light_r = self.bumper.light_signal_right
            ir = self.ir_omni
            if (164 in ir):
            # or (ir == 165) or (ir == 168) or (ir == 169) or (ir == 172) or (ir == 173):
                vel.linear.x  = 0
                vel.angular.z = 0
                print ir
                print '3rd layer is activated!!!!!!!!!!'
                with open('ir.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, ir])
                self.cmd_vel.publish(vel)
                rate.sleep()
            else:
                vel.linear.x  = 0
                vel.angular.z = 0.5
                print ir
                print '3rd layer is not activated'
                with open('ir.csv', 'a') as r:
                    writer = csv.writer(r)
                    writer.writerow([vel.linear.x, vel.angular.z, ir])
                self.cmd_vel.publish(vel)
                rate.sleep()    
            

                    
            

if __name__ == '__main__':
    rospy.init_node("LCS")
    LCS().run()
