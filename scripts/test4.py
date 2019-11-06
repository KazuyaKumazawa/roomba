#!/usr/bin/env python
#Keep going forward and stop when bumper activated
import rospy
from geometry_msgs.msg import Twist
from ca_msgs.msg import Bumper

class GoAndStop():
    def __init__(self):
        self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.bumper = Bumper()
        rospy.Subscriber("bumper", Bumper, self.callback)
            
    def callback(self,messages):
        self.bumper = messages
        
    def run(self):
        vel  = Twist() #initialize
        while not rospy.is_shutdown():
            if self.bumper.is_left_pressed == False:
                vel.linear.x  = 0.1
                print vel
                self.cmd_vel.publish(vel)
            else:
                vel.linear.x  = 0
                print vel
                self.cmd_vel.publish(vel)
                break

if __name__ == '__main__':
    rospy.init_node("GoAndStop")
    GoAndStop().run()

'''
rospy.init_node("GoAndStop") #Give the node a name

pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

def main():
    #sub = rospy.Subscriber("bumper", Bumper, callback)
    sub = rospy.Subscriber("bumper", Bumper)
    while not rospy.is_shutdown():
        vel  = Twist() #initialize
        vel.linear.x  = 0.1
        print vel
        rightbumper = Bumper()
        rightbumper = sub
        print rightbumper
        pub.publish(vel)


def callback(bumper):
    print rightbumper.is_right_pressed
    stop_vel = Twist()
    stop_vel.linear.x = 0
    rate = rospy.Rate(10.0)
    for i in range(5):
        pub.publish(stop_vel)
        rate.sleep()

if __name__ == "__main__":
    main()
'''
