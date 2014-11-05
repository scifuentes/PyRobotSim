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

class RobotLogic(threading.Thread):
    def __init__(self,port=1005):
        threading.Thread.__init__(self)
        self.com=SimpleUDP.Client('127.0.0.1',port)
    
    def run(self):
        self.main()
    
    def main(self):
    
        while True:
        
            d_fr,d_fl,d_bc=self.GetDistanceSensors()
            o_z= self.GetOrientation()
            print 'Status = ',d_fr,d_fl,o_z
            
            if d_fr >=80 and d_fl >=80 :
                self.SetSpeed(20,20)        
            elif d_fr >20 and d_fl >20 :
                self.SetSpeed(5,5)
            else :
                print 'Collision Risk, turning'
                self.SetSpeed(0,0)
                r0=self.GetOrientation()
                r1=AngleDif(0,r0+radians(120))
                da=AngleDif(r0,r1)
                    
                print 'Orientation = ',r0,r1

                    
                while abs(da)>radians(0.1):
                    if abs(da)>radians(10):
                        ts=5
                    else:
                        ts=degrees(abs(da))/2.0
                    if (da>0):
                        self.SetSpeed(-ts,ts)
                    else:
                        self.SetSpeed(ts,-ts)                
                    r0=self.GetOrientation()
                    da=AngleDif(r0,r1)
                    print 'Orientation = ',r0,r1,da

                print 'Turn Done',r0
                self.SetSpeed(0,0)
    
    def GetDistanceSensors(self):    
        d_fr=float(self.com.Request('Get_DistanceSensorFR.reading')[0])
        d_fl=float(self.com.Request('Get_DistanceSensorFL.reading')[0])
        d_bc=float(self.com.Request('Get_DistanceSensorBC.reading')[0])
        return d_fr,d_fl,d_bc
    
    def GetOrientation(self):
        return float(self.com.Request('Get_Compass.reading')[0])

    def SetSpeed(self,vr,vl):
        if (vr!=None):
            self.com.Send((' ').join(['Set_motorR.speed',str(vr)]))
        if (vl!=None):
            self.com.Send((' ').join(['Set_motorL.speed',str(vl)]))    
        time.sleep(0.05)
    
if __name__ == "__main__":
    r=RobotLogic()
    r.main()
