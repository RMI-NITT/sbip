#!/usr/bin/env python
from __future__ import print_function

import roslib
import numpy as np
roslib.load_manifest('sbip')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

points_1 = np.float32([(102,1),(614,14),(87,465),(626,470)]) 
points_2 = np.float32([(0,0),(640,0),(0,566),(640,566)])

lower_red = np.array([0,220,180])
upper_red = np.array([25,255,200])

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("fieldroi",Image, queue_size = 10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("usb_cam/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    frame = cv2.medianBlur(cv_image,3)
    perspective_transform = cv2.getPerspectiveTransform(points_1,points_2)
    dst = cv2.warpPerspective(frame,perspective_transform,(640,566))

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(dst, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('roigen', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)