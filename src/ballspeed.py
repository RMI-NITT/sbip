#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import time
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Pose

ball = Pose()

def bp(msg):
    global ball
    ball  = msg

def run():
    global ball
    rospy.init_node('ballspeed', anonymous=True)
    rospy.Subscriber('ballpose',Pose,bp)
    bpub = rospy.Publisher('balltwist',Twist,queue_size = 10)
    rate = rospy.Rate(20)
    xo = 0
    yo = 0
    tw = Twist()
    while(True):
        x = ball.position.x
        y = ball.position.y
        difx = x -xo
        dify = y -yo
        vx = 20*(x-xo)
        vy = 20*(y-yo)
        tw.linear.x = vx
        tw.linear.y = vy
        bpub.publish(tw)
        xo = x
        yo = y 
        rate.sleep()

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass