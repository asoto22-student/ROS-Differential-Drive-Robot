#! usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerRequest
from nav_msgs.srv import GetMap, GetMapRequest
import time as t

# Init a node as usual
rospy.init_node('bounds_client')

# Wait for this service to be running
rospy.wait_for_service('/box')

# Create the connection to the service. Remember it's a Trigger service
sos_service = rospy.ServiceProxy('/box', Trigger)

# Create an object of the type TriggerRequest. We need a TriggerRequest for a Trigger service
sos = TriggerRequest()

# Now send the request through the connection
while(True):
    tick = t.time()
    result = sos_service(sos)
    tock = t.time()
    print(tock-tick)
    t.sleep(0.2)

# Done
print(result)

