#=============================================================================================
#
#PyRobotSim  - Simulated Robot HW definition and low level commands simulated actions
#                  Receives the control commands through a UDP link
#
#============================================================================================
# by Santiago Cifuentes

import math

import SimpleUDP

from SimDiferentialChassis import DiferentialChassisRobot
from SimRangeSensor import DistanceSensor
from SimServoMotor import ServoMotor
from SimCompass import Compass
from SimBeacon import BeaconReceiver

class SimRobot(DiferentialChassisRobot):
    def __init__(self,port=1005):
        DiferentialChassisRobot.__init__(self)
        self.comm=SimpleUDP.Server(self.AttendMessage,'127.0.0.1',port)
        
        #lets build the robot#
        
        self.shape=[[10.,6.],[10.,-6.],[-10.,-6.],[-10.,6.]]
        
        self.wheel_diameter=5.
        self.wheel_separation=12.
        
        self.servoFR=ServoMotor(zero=[0.,0.,math.pi/4.],axis=[0.,0.,1.])
        self.distanceSensorFR=DistanceSensor()
        self.AttachChild(self.servoFR)
        self.servoFR.AttachChild(self.distanceSensorFR)
        self.servoFR.position.x=9.
        self.servoFR.position.y=4.
        self.distanceSensorFR.range=80.
        
        self.servoFL=ServoMotor(zero=[0.,0.,-math.pi/4.],axis=[0.,0.,1.])
        self.distanceSensorFL=DistanceSensor()
        self.AttachChild(self.servoFL)
        self.servoFL.AttachChild(self.distanceSensorFL)
        self.servoFL.position.x=9.
        self.servoFL.position.y=-4.
        self.distanceSensorFL.range=80.
        
        self.servoBC=ServoMotor(zero=[0.,0.,math.pi],axis=[0.,0.,1.])
        self.distanceSensorBC=DistanceSensor()
        self.AttachChild(self.servoBC)
        self.servoBC.AttachChild(self.distanceSensorBC)
        self.servoBC.position.x=-9.
        self.servoBC.position.y=0.
        self.distanceSensorBC.range=80.
        
        self.compass=Compass()
        self.AttachChild(self.compass)
        
        self.beaconReceiver=BeaconReceiver()
        self.AttachChild(self.beaconReceiver)
        
    def AttendRequests(self):   #implements ActiveObject::AttendRequests
        self.comm.CheckRequests()
        
    #=================================================
        
    def AttendMessage(self,msgIn,addr):
        #transforms remote commands into simHW actions
        
        msgOut=''
        msgIn=msgIn.split()
        
        if msgIn[0]=='Tic' :
            msgOut='Toc'
        
        elif msgIn[0]=='Set_motorR.speed' :
            self.motorR.speed=float(msgIn[1])
        
        elif msgIn[0]=='Set_motorL.speed' :
            self.motorL.speed=float(msgIn[1])
        
        elif msgIn[0]=='Get_DistanceSensorFR.reading' :
            msgOut=str(self.distanceSensorFR.reading) 
            
        elif msgIn[0]=='Get_DistanceSensorFL.reading' :
            msgOut=str(self.distanceSensorFL.reading) 
            
        elif msgIn[0]=='Get_DistanceSensorBC.reading' :
            msgOut=str(self.distanceSensorBC.reading) 
        
        elif msgIn[0]=='Get_Compass.reading' :
            msgOut=str(self.compass.reading) 
            
        else :
            print msgIn
            msgOut='NACK'
            
        return msgOut

#==============================================================================
