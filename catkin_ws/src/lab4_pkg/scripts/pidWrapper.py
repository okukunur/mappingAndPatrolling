#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

odom_x = 0.0
odom_z = 0.0

class pidWrapper:
  def __init__(self):
    self.lin_stpt = rospy.Publisher('/linear_pid/setpoint',Float64,queue_size=1)
    self.lin_state = rospy.Publisher('/linear_pid/state',Float64,queue_size=1)
    self.lin_effort = rospy.Subscriber('/linear_pid/control_effort', Float64, self.xeffort_callback)

    self.ang_stpt = rospy.Publisher('/angular_pid/setpoint',Float64,queue_size=1)
    self.ang_state = rospy.Publisher('/angular_pid/state',Float64,queue_size=1)
    self.ang_effort = rospy.Subscriber('/angular_pid/control_effort', Float64, self.zeffort_callback)

    self.cmd_vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size=1)
    self.odom = rospy.Subscriber('/jackal_velocity_controller/odom', Odometry, self.odom_callback)
    self.rawTwist = rospy.Subscriber('/rawTwist', Twist, self.twist_callback)
    self.twist = Twist()

  def xeffort_callback(self,msg):
    self.twist.linear.x = msg.data

  def zeffort_callback(self,msg):
    self.twist.angular.z = msg.data

  def odom_callback(self,msg):
    global odom_x
    global odom_z
    odom_x = msg.twist.twist.linear.x
    odom_z = msg.twist.twist.angular.z

  def twist_callback(self,msg):
    global odom_z
    global odom_x
    z = msg.angular.z
    x = msg.linear.x
    self.ang_stpt.publish(z) 
    self.ang_state.publish(odom_z)
    self.lin_stpt.publish(x) 
    self.lin_state.publish(odom_x)
    self.cmd_vel_pub.publish(self.twist)

rospy.init_node('pid_wrapper')
wrapper = pidWrapper()
rospy.spin()
# END ALL
