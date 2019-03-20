#!/usr/bin/env python
############
#INCOMPLETE#
############
from __future__ import print_function

import roslib
import numpy as np
roslib.load_manifest('sbip')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose
from cv_bridge import CvBridge, CvBridgeError

lower_white = np.array([(230,230,230)])
higher_white = np.array([(255,255,255)])
lower_yellow = np.array([(0,230,220)])
higher_yellow = np.array([(10,255,255)])

def ftransform(x,y):
  x = (x-640/2)
  y = (566/2-y)
  return x,y

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("ballmask",Image, queue_size = 10)
    self.ballpub = rospy.Publisher("ballpose",Pose, queue_size = 10)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/fieldroi",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    
    mask_white = cv2.inRange(cv_image,lower_yellow,higher_yellow)
    _,cnts,_ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      cX,cY = ftransform(cX,cY)
      bp = Pose()
      bp.position.x = cX
      bp.position.y = cY
      

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(mask_white, "mono8"))
      self.ballpub.publish(bp)
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('balldatapub', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)