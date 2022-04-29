#!/usr/bin/env python
import rospy

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()
last_pose = PoseStamped()
last_pose.pose.position.x = 0
last_pose.pose.position.y = 0
last_pose.pose.position.z = 0
def dist(ps1, ps2):
    return ((ps1.pose.position.x - ps2.pose.position.x)**2 + (ps1.pose.position.y - ps2.pose.position.y)**2 + (ps1.pose.position.z - ps2.pose.position.z)**2)**0.5

def odom_cb(data):
    global path, last_pose
    path.header = data.header
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose.pose
    if (dist(pose, last_pose) >= 0.05):
        path.poses.append(pose)
        last_pose = pose
    path_pub.publish(path)

rospy.init_node('path_node')

odom_sub = rospy.Subscriber('/mavros/local_position/odom', Odometry, odom_cb)
path_pub = rospy.Publisher('/path_px4', Path, queue_size=1000)

if __name__ == '__main__':
    rospy.spin()