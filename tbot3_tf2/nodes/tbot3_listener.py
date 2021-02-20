#!/usr/bin/env python2.7

import rospy
import tf2_ros
import math
import geometry_msgs.msg

object_name = 'unit_box'

MAX_LIN_VEL = 0.2

if __name__ == '__main__':
    rospy.init_node('tbot3_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    tbot3_vel = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('base_footprint', object_name, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        msg = geometry_msgs.msg.Twist()
        msg.angular.z = math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        msg.linear.x = min(math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2), MAX_LIN_VEL)

        tbot3_vel.publish(msg)

        rate.sleep()