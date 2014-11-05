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
import math
import random
from math import radians, degrees, pi

currDir=os.path.dirname(os.path.realpath(__file__))
parentDir=os.path.dirname(currDir)
sys.path.insert(1,parentDir+r'\PartsBox')
    
from MathAux import AngleDif
import SimpleUDP

class SheepLogic(threading.Thread):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        self.com=SimpleUDP.Client('127.0.0.1',port)
    
    def run(self):
        self.main()
    
    def main(self):
    
        while True:
            dist=self.GetDistanceSensor()
            fieldBeacon_dist,fieldBeacon_angle=self.GetBeaconRead(4)
            dog1_dist,dog1_angle=self.GetBeaconRead(1)
            dog2_dist,dog2_angle=self.GetBeaconRead(2)

            self.SetSpeed(random.gauss(10,4),random.gauss(10,4))
            
            
    def GetDistanceSensor(self):    
        return float(self.com.Request('Get_DistanceSensor.reading')[0])

    def GetBeaconRead(self,id):
        [dstr,astr]=self.com.Request(' '.join(['Get_BeaconRead',str(id)]))
        distance=float(dstr)
        angle=float(astr)
        return distance,angle
        

    def SetSpeed(self,vl,vr):
        if (vr!=None):
            self.com.Send((' ').join(['Set_motorR.speed',str(vr)]))
        if (vl!=None):
            self.com.Send((' ').join(['Set_motorL.speed',str(vl)]))    
        time.sleep(0.05)
    
if __name__ == "__main__":
    r=RobotLogic()
    r.main()
