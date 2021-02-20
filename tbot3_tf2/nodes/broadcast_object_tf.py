#!/usr/bin/env python2.7

import rospy
import tf2_ros
import geometry_msgs.msg
from gazebo_msgs.msg import ModelStates

object_name = 'unit_box'

def handle_object_pose(msg):
    ind = msg.name.index(object_name)
    box_position_x = msg.pose[ind].position.x
    box_position_y = msg.pose[ind].position.y
    box_or_x = msg.pose[ind].orientation.x
    box_or_y = msg.pose[ind].orientation.y
    box_or_z = msg.pose[ind].orientation.z
    box_or_w = msg.pose[ind].orientation.w

    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "odom"
    t.child_frame_id = object_name
    t.transform.translation.x = box_position_x
    t.transform.translation.y = box_position_y
    t.transform.translation.z = 0.0
    t.transform.rotation.x = box_or_x
    t.transform.rotation.y = box_or_y
    t.transform.rotation.z = box_or_z
    t.transform.rotation.w = box_or_w

    br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('tf2_object_broadcaster')

    rospy.Subscriber('/gazebo/model_states', ModelStates, handle_object_pose)

    rospy.spin()