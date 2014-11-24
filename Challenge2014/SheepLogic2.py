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
from math import radians, degrees, pi, cos, sin
from MathAux import AngleNorm, AngleDif

currDir=os.path.dirname(os.path.realpath(__file__))
parentDir=os.path.dirname(currDir)
sys.path.insert(1,parentDir+r'\PartsBox')
    
from MathAux import AngleDif
import SimpleUDP

#To be used with SimRobot2 or compatible 

class SheepLogic(threading.Thread):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        self.com=SimpleUDP.Client('127.0.0.1',port)
    
    def run(self):
        self.main()
    
    def main(self):
        vmax=10
        
        self.SetForwardMove(5*pi)
        while not self.CheckMoveCompleted():
            print 'moving...'
            time.sleep(0.01)

        while True:
            dist=self.GetDistanceSensor()
            barn_dist,barn_angle=self.GetBeaconRead(4)
            dog1_dist,dog1_angle=self.GetBeaconRead(1)
            dog2_dist,dog2_angle=self.GetBeaconRead(2)
               

            self.SetTurnMove(-pi)
            while not self.CheckMoveCompleted():
                print 'turning...'
                time.sleep(0.01)
                
            self.SetForwardMove(2*pi)
            while not self.CheckMoveCompleted():
                print 'moving...'
                time.sleep(0.01)
            
    def Move(self,speed,dir=0,k=5):
        self.SetSpeed(speed+AngleNorm(dir)*k,speed-AngleNorm(dir)*k)
                

    # ====== HW commands =======
    def SetForwardSpeed(self,v):
        self.com.Send((' ').join(['Set_Forward_Speed',str(v)]))
        time.sleep(0.01)
        
    def SetTurnSpeed(self,v):
        self.com.Send((' ').join(['Set_Turn_Speed',str(v)]))
        time.sleep(0.01)
        
    def SetForwardMove(self,ad,v=10):
        if ad<0 and v>0:
            v*=-1
        self.com.Send((' ').join(['Move_Forward',str(ad),str(v)]))
        time.sleep(0.01)
        
    def SetTurnMove(self,ad,v=10):
        if ad<0 and v>0:
            v*=-1
        self.com.Send((' ').join(['Move_Turn',str(ad),str(v)]))
        time.sleep(0.01) 
        
    def StopMove(self):
        self.com.Send('Stop_Move')
        time.sleep(0.01)

        
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
    

    
if __name__ == "__main__":
    r=RobotLogic()
    r.main()
