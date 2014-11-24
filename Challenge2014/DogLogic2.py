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

currDir=os.path.dirname(os.path.realpath(__file__))
parentDir=os.path.dirname(currDir)
sys.path.insert(1,parentDir+r'\PartsBox')
    
from MathAux import AngleDif
import SimpleUDP

class DogLogic(threading.Thread):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        self.com=SimpleUDP.Client('127.0.0.1',port)
    
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
    def SetForwardSpeed(self,v):
        self.com.Send((' ').join(['Set_Forward_Speed',str(v)]))
        time.sleep(0)
        
    def SetTurnSpeed(self,v):
        self.com.Send((' ').join(['Set_Turn_Speed',str(v)]))
        time.sleep(0)
        
    def SetForwardMove(self,ad,v=10):
        if ad<0 and v>0:
            v*=-1
        self.com.Send((' ').join(['Move_Forward',str(ad),str(v)]))
        time.sleep(0)
        
    def SetTurnMove(self,ad,v=10):
        if ad<0 and v>0:
            v*=-1
        self.com.Send((' ').join(['Move_Turn',str(ad),str(v)]))
        time.sleep(0) 
        
    def StopMove(self):
        self.com.Send('Stop_Move')
        time.sleep(0)

        
    def CheckMoveCompleted(self):
        return (self.com.Request('Check_Move_Done')[0]=='True')
        
    def GetDistanceSensor(self):    
        return float(self.com.Request('Get_DistanceSensor.reading')[0])
        
    def GetBeaconRead(self,id):
        [dstr,astr]=self.com.Request(' '.join(['Get_BeaconRead',str(id)]))
        distance=float(dstr)
        angle=float(astr)
        return distance,angle

    def GetGiroSensor(self):    
        [vrz_str,irz_str]=self.com.Request('Get_GiroRead')
        return float(vrz_str),float(irz_str)
    
    def ResetGiroSenor(self):
        self.com.Send('Reset_GiroRead')
        
    def SetSensorServoSpeed(self,v):
        self.com.Send((' ').join(['Set_SensorServo_Speed',str(v)]))        
        time.sleep(0)
    
    def MoveSensorServo(self,ad,v):
        self.com.Send((' ').join(['Move_SensorServo',str(ad),str(v)]))  
        time.sleep(0)
        
    def GetSensorServoPos(self):    
        return float(self.com.Request('Get_SensorServo_Pos'        
if __name__ == "__main__":
    r=RobotLogic()
    r.main()
