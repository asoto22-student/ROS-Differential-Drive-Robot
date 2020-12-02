#! usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import GetModelState

rospy.init_node('bounds_check', anonymous=True)
pub = rospy.Publisher('/box', Twist, queue_size=10)

# robot moves max 10m/sec
V_max     = 0.5   # Max movement speed (m/s)
L_buff    = 2     # Buffer room
h_box     = 5     # Box height (m)
t_ground  = 1.01  # sec (based on a height of 5m)
T         = 0.02  # Sampling rate (sec)
t_loading = 1.5   # Loading time

t_for_bugger            = L_buff/V_max
d_from_v_max_to_ground  = V_max * t_ground  # m - 10.1m
d_from_sampling         = V_max * T         # m - 1m
d_from_loading          = V_max * t_loading
d_total                 = d_from_sampling + d_from_v_max_to_ground + d_from_loading

print("dist from T", d_from_sampling)
print("dist from Box", d_from_v_max_to_ground)
print("dist from t_loading", d_from_loading)
print(d_total)