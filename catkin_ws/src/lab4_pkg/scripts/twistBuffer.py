#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

linear  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
angular = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def raw_callback(msg,twist_pub):
    #referencing global variables
    global g_last_twist
    global linear
    global angular
    linear.pop(0)
    angular.pop(0)
    linear.append(msg.linear.x)
    angular.append(msg.angular.z)
    g_last_twist.angular.z = sum(angular)/len(angular)
    g_last_twist.linear.x  = sum(linear)/len(linear)

if __name__ == "__main__":

    try:
        rospy.init_node("rawTwist", anonymous=True)
        #We also want to subscribe to the Twist topics so if teleop is running we freeze
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)    
        #We want to subscribe to the velocity command so that we can command it 
        rospy.Subscriber('rawTwist', Twist, raw_callback, pub)
        rate = rospy.Rate(10)#publish data to twist at 10 Hz
        g_last_twist = Twist()
        while not rospy.is_shutdown():
            pub.publish(g_last_twist)
            rate.sleep()
            # print(max(LaserScan.ranges))
    except rospy.ROSInterruptException:
        pass
