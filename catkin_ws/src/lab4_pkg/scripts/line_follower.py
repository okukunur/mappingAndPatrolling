#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


#Pull in parameters
maxSpeed = rospy.get_param("/maxSpeed") #Max speed
delayT   = rospy.get_param("/delayT")   # Time delay in seconds
distanceD= rospy.get_param("/distanceD")# Distance from wall in meters
g_ranges = []
wallFound = False

class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    self.image_sub = rospy.Subscriber('/front/image_raw', 
                                      Image, self.image_callback)

    self.laser = rospy.Subscriber('/front/scan', LaserScan, self.laser_callback)
    self.cmd_vel_pub = rospy.Publisher('/rawTwist',Twist, queue_size=1)
    self.twist = Twist()

  def laser_callback(self,msg):
    global g_ranges
    g_ranges = msg.ranges

  def image_callback(self, msg):
    global g_ranges
    global wallFound
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = numpy.array([ 25,  25,  50])
    upper_yellow = numpy.array([80, 255, 240])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("window", res)
    cv2.waitKey(3)
    cv2.imshow("hsv", hsv)
    # BEGIN CROP
    h, w, d = image.shape
    search_top = 3*h/5
    search_bot = search_top + 30
    image[0:search_top, 0:w] = 0
    image[search_bot:h, 0:w] = 0
    #cv2.imshow("cropped", image)
    #cv2.waitKey(3)
    # END CROP
    # BEGIN FINDER
    M = cv2.moments(mask)
    #check the sign of last error
    errorSign = 1

    #if we are to the left of the line, turn right
    if M['m00'] > 0:
      wallFound = True
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
    # END FINDER
    # BEGIN CIRCLE
      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
    # END CIRCLE
    # BEGIN CONTROL
      err = cx - w/2

      if(err != 0):
          errorSign = -err/abs(err) 

      #if we came to the end of the line rotate only
      if(cy < h/1.5):
          self.twist.linear.x = maxSpeed
          self.twist.angular.z = float(abs(err))*errorSign / 70
      else:
          self.twist.linear.x = 0.0
          #this makes sure we turn only to the direction in which the line was lost.
          self.twist.angular.z = 3*errorSign
    # END CONTROL
    #if we lost the line find it....
    else:
        if not wallFound:
            if  min(g_ranges) < distanceD:
                #print("Completely lost!!!")
                self.twist.linear.x = 0.0
                #division by + 1 so we never have division by 0
                direction = (359.0 - g_ranges.index(min(g_ranges)))/abs((359.0 - g_ranges.index(min(g_ranges)) + 1.0))
                print g_ranges.index(min(g_ranges))
                self.twist.angular.z = direction*2
            else:
                self.twist.linear.x = maxSpeed
                self.twist.angular.z = 0
        else:
            self.twist.linear.x = 0.0
            self.twist.angular.z = errorSign*2
    self.cmd_vel_pub.publish(self.twist)
    cv2.imshow("window", image)
    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
