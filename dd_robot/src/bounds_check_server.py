#! usr/bin/env python
import rospy

import os
import time as t
import numpy as np

from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from std_srvs.srv import Trigger, TriggerResponse

name = 'box'
box_i = 0

max_distance = 50
error_dist = 1.5

#robot_proxy = None

# Callback function used by the service server to process
# requests from clients. It returns a TriggerResponse
def trigger_response(request):
    global box_i

    dropBoxBool = False

    a = getRobotLocation()
    x = a[0]
    y = a[1]

    b = getBoxLocation(x,y)

    if (b != None):
        if (not checkBoxLocation(int(b[0]),int(b[1]))):
            dropBox(int(b[0]), int(b[1]))
            dropBoxBool = True
    
    return TriggerResponse(
        success=10.1,
        message= "dt = "
    )

def delbox(bi):
    buff = "rosservice call gazebo/delete_model "+name+str(bi) + " &"
    os.system(buff)

def delBoxAll(bi):
    for i in range(bi):
        delbox(i)
        t.sleep(0.1)

box_x = []
box_y = []
def saveBoxVal(x, y):
    global box_x, box_y
    box_x.append(x)
    box_y.append(y)
    return

def checkBoxLocation(x, y):
    global box_x, box_y
    ret = False

    if (x >= (max_distance - error_dist)):
        x = max_distance
    elif (x <= (error_dist - max_distance)):
        x = -max_distance
    if (x >= (max_distance - error_dist)):
        x = max_distance
    elif (x <= (error_dist - max_distance)):
        x = -max_distance

    print("Box X Locations:", box_x)
    print("Box Y Locations:", box_y)
    print("Robot X Locations:", x)
    print("Robot Y Locations:", y)

    for i in range(box_i):
        xx = box_x[i]
        yy = box_y[i]
        #d = np.sqrt((xx-x)*(xx-x) + (yy-y)*(yy-y))
        #if d < 1.0:
        if (x == box_x[i] and y == box_y[i]):
            return True
    return False

def dropBox(x,y):
    global box_i

    saveBoxVal(x, y)

    b0 = "./drop_box.sh "
    b1 = name + str(box_i) + " "
    box_i += 1
    b2 = str(x) + " "
    b3 = str(y) + " "
    b4 = "&"
    buff = b0 + b1 + b2 + b3 + b4
    os.system(buff)

# Determine if it is inside of the 50mn - 2m circle
def getBoxLocation(x,y):
    x0 = 0.0
    y0 = 0.0

    global max_distance

    dist = np.sqrt( (x-x0) * (x-x0)  + (y-y0)*(y-y0) )

    #rospy.loginfo("Dist = ", str(dist))
    #print("Dist = ", str(dist))
    print("X =", x, "Y =", y, "Max Distance =", max_distance)

    #if (dist < (max_distance-2) ):
    if ((np.abs(x) < (max_distance - error_dist)) and (np.abs(y) < (max_distance - error_dist))):
        print("Inside")
        return None
    else:
        print("Outside")
        xn = x
        yn = y

        if (xn >= (max_distance - error_dist)):
            xn = max_distance
        elif (xn <= (error_dist - max_distance)):
            xn = -max_distance
        if (yn >= (max_distance - error_dist)):
            yn = max_distance
        elif (yn <= (error_dist - max_distance)):
            yn = -max_distance
        
        print('x:', x, 'y:', y, 'xn:', xn, 'yn:', yn)
        
        return (xn, yn)

    return

def getRobotLocation():
    global robot_proxy
    a = GetModelStateRequest(model_name='dd_robot')
    a.model_name = 'dd_robot'
    s = robot_proxy(a)
    
    #print(a)
    #print(s)

    x = s.pose.position.x
    y = s.pose.position.y
    
    return (x,y)

rospy.init_node('bounds_server')
delBoxAll(10)

my_service = rospy.Service('/box', Trigger, trigger_response)
rospy.wait_for_service('/gazebo/get_model_state')
robot_proxy = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

rospy.spin()