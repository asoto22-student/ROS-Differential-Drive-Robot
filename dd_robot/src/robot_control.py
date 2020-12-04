#!/usr/bin/env python3

import os
import rospy
import numpy as np

from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
from geometry_msgs.msg import Twist
from std_msgs.msg import Header

# Constants
move_speed = 5
angular_speed = 5
pub_freq = 10

# Global Variables
l_wheel_speed = 0
r_wheel_speed = 0

target_vels = 0.0
target_angvels = 0.0

def get_values(msg):
    global l_wheel_speed, r_wheel_speed
    dd = ros2diffDrive(msg.linear.x, msg.linear.y)

    l_wheel_speed = dd[0]
    r_wheel_speed = dd[1]

    print(l_wheel_speed, r_wheel_speed)

def getPos(pub):
    buff = GetJointProperties()

    buff.joint_name = 'dd_robot::left_wheel_hinge'
    val = pub(buff.joint_name)
    leftw = val.rate[0]
    
    buff.joint_name = 'dd_robot::right_wheel_hinge'
    val = pub(buff.joint_name)
    rightw = val.rate[0]

    v = (leftw, rightw)
    return v

def ros2diffDrive(x, y):
    global target_vels, target_angvels

    if (x > 1.0):
        x = 1.0
    if (x < -1.0):
        x = -1.0
    if (y > 1.0):
        y = 1.0
    if (y < -1.0):
        y = -1.0

    x *= angular_speed
    y *= move_speed

    target_vels = y
    target_angvels = x

    v = (1.0 - np.abs(x)) * y + y
    w = (1.0 - np.abs(y)) * x + x
    r = (v + w) / 2.0
    l = (v - w) / 2.0
    
    wheel_l = l
    wheel_r = r
    return [wheel_l, wheel_r]

def vel2ros(pub, v, start_time, end_time):
    if (np.abs(target_vels) > 0.1):
        if (v[0] < l_wheel_speed):
            pub("dd_robot::left_wheel_hinge", l_wheel_speed, start_time, end_time)
        else:
            pub("dd_robot::left_wheel_hinge", -l_wheel_speed, start_time, end_time)
        if (v[1] < r_wheel_speed):
            pub("dd_robot::right_wheel_hinge", r_wheel_speed, start_time, end_time)
        else:
            pub("dd_robot::right_wheel_hinge", -r_wheel_speed, start_time, end_time)
    elif (np.abs(target_angvels) > 0.1):
            pub("dd_robot::left_wheel_hinge", l_wheel_speed, start_time, end_time)
            pub("dd_robot::right_wheel_hinge", r_wheel_speed, start_time, end_time)
    else:
        pub("dd_robot::left_wheel_hinge", -v[0], start_time, end_time)
        pub("dd_robot::right_wheel_hinge", -v[1], start_time, end_time)

def main():
    rospy.init_node('dd_ctrl', anonymous=True)
    pub = rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
    pubget = rospy.ServiceProxy('/gazebo/get_joint_properties',GetJointProperties)
    sub = rospy.Subscriber('/cmd_vel', Twist, get_values)

    os.system('./loadModel.sh')

    rate = rospy.Rate(pub_freq)

    start_time = rospy.Time(0, 0)
    end_time = rospy.Time(0.1/pub_freq, 0)

    while not rospy.is_shutdown():
        v = getPos(pubget)
        print v
        print ('target_vels:', target_vels, 'target_angvels:', target_angvels)

        vel2ros(pub, v, start_time, end_time)

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
