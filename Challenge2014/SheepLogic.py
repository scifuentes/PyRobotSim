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

class SheepLogic(threading.Thread):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        self.com=SimpleUDP.Client('127.0.0.1',port)
    
    def run(self):
        self.main()
    
    def main(self):
        vmax=10
        
        while True:
            dist=self.GetDistanceSensor()
            barn_dist,barn_angle=self.GetBeaconRead(4)
            dog1_dist,dog1_angle=self.GetBeaconRead(1)
            dog2_dist,dog2_angle=self.GetBeaconRead(2)
               
            #Demo: random move
            #self.SetSpeed(random.gauss(10,4),random.gauss(10,4))
            
            dog0_dist=min(dog1_dist,dog2_dist)
            dog2dog_angle=AngleDif(dog1_angle,dog2_angle)
            dog2dog_distance=dog1_dist**2+dog2_dist-2*dog1_dist*dog2_dist*cos(dog2dog_angle)
            w1=1-dog1_dist/(dog1_dist+dog2_dist)
            w2=1-dog2_dist/(dog1_dist+dog2_dist)
            
            dog0_angle=AngleNorm(dog1_angle*w1+dog2_angle*w2)
            scape_angle=AngleNorm(dog0_angle+pi)
            mid_angle=AngleNorm((dog1_angle+dog2_angle)/2.)
            skirt_angle=AngleNorm(dog0_angle+pi/2.)
            barn2dog_angle=AngleDif(dog0_angle,barn_angle)
            
            if dog0_dist<100:
                print dog1_angle,dog2_angle,barn_angle,dog0_angle,skirt_angle,barn2dog_angle,dog0_dist
                err_dist=(100-dog0_dist)/100.
                self.Move(vmax,skirt_angle+err_dist*pi/2.,err_dist*5.+5.)
                print 
            else:
                self.Move(vmax,mid_angle)
            
            
    def Move(self,speed,dir=0,k=5):
        self.SetSpeed(speed+AngleNorm(dir)*k,speed-AngleNorm(dir)*k)
                

    # ====== HW commands =======
    def SetSpeed(self,vl,vr):
        if (vr!=None):
            self.com.Send((' ').join(['Set_motorR.speed',str(vr)]))
        if (vl!=None):
            self.com.Send((' ').join(['Set_motorL.speed',str(vl)]))    
        time.sleep(0.05)

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
