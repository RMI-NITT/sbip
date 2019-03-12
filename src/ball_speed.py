import rospy
import cv2
import numpy as np
import time
import rospy
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Pose



class ball_speed():
    def __init__(self):
        self.pos_old_x = 0 
        self.pos_old_y = 0
        rospy.Subscriber("ballpose",Pose,self.callback)
        self.pub_s = rospy.Publisher("balltwist",Twist, queue_size = 10)

    def callback(self,msg):
        self.pos_x  = msg.position.x
        self.pos_y  = msg.position.y
        self.dif_x = -((self.pos_old_x - self.pos_x))
        self.dif_y = -((self.pos_old_y - self.pos_y))
        self.pos_old_x = self.pos_x
        self.pos_old_y = self.pos_y
        #publish speed_x and speed._y
    
if __name__ == '__main__':
    try:
        rospy.init_node('balltwistfind')
        rate = rospy.Rate(60)
        bs = ball_speed()
        tw = Twist()
        while(True):
            tw.linear.x = bs.difx*60
            tw.linear.y = bs.dify*60
            rate.sleep()

    except rospy.ROSInterruptException: pass
