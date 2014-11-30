#=============================================================================================
#
#Robot Logic - Defines the high level logic of the robot, 
#              Controls the robot through commands send to a communication link
#
#============================================================================================
# by Santiago Cifuentes

import os
import sys
import time
import threading
from math import radians, degrees, pi
import SimRobot2

currDir=os.path.dirname(os.path.realpath(__file__))
parentDir=os.path.dirname(currDir)
sys.path.insert(1,parentDir+r'\PartsBox')
    
from MathAux import AngleDif
import SimpleUDP

class DogLogic(threading.Thread,SimRobot2.SimRobotClient):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        SimRobot2.SimRobotClient.__init__(self,"127.0.0.1",port);
    
    def run(self):
        self.main()
    
    def main(self):
    
        while True:
            dist=self.GetDistanceSensor()
            fieldBeacon_dist,fieldBeacon_angle=self.GetBeaconRead(4)
            sheep_dist,sheep_angle=self.GetBeaconRead(3)
            
            self.LookToBeacon(4)

    
    def LookToBeacon(self,beacon_id):
        beacon_dist,beacon_angle=self.GetBeaconRead(beacon_id)
        if beacon_dist<300:
            ang_err=beacon_angle
            if ang_err>1:
                ang_err=1
            if ang_err<-1:
                ang_err=-1
            self.SetSensorServoSpeed(ang_err*3)
        else :
            self.SetSensorServoSpeed(0.1)
    
    # ====== HW commands =======
    # These are now contained in the SimRobotClient class, 
    #  provided together with the SimRobot class that simulated the HW
    
if __name__ == "__main__":
    r=RobotLogic()
    r.main()
