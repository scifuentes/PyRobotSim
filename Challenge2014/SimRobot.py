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
from SimBeacon import BeaconReceiver, BeaconSource
from SimGiro import GiroSensor

class SimRobot(DiferentialChassisRobot):
    def __init__(self,port=1005,beaconId=0):
        DiferentialChassisRobot.__init__(self)
        self.comm=SimpleUDP.Server(self.AttendMessage,'127.0.0.1',port)
        
        #lets build the robot#
        
        #this defines the robot body, it will be used for collision detection and interaction with sensors
        l=25.
        w=20.
        self.shape=[[l/2,-w/2],[l/2,w/2],[-l/2,w/2],[-l/2,-w/2]]    
        
        self.wheel_diameter=5.
        self.wheel_separation=20.
        
        self.sensorServo=ServoMotor(zero=[0.,0.,0],axis=[0.,0.,1.])
        self.sensorServo.position.x=l/2-5.
        self.sensorServo.position.y=0.
        self.AttachChild(self.sensorServo)

        self.distanceSensor=DistanceSensor()
        self.distanceSensor.range=80.
        self.sensorServo.AttachChild(self.distanceSensor)

        self.beaconReceiver=BeaconReceiver()
        self.sensorServo.AttachChild(self.beaconReceiver)
        
        self.giroSensor=GiroSensor()
        self.AttachChild(self.giroSensor)
        
        self.beaconSender=BeaconSource(beaconId)
        self.AttachChild(self.beaconSender)
        
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
            
        elif msgIn[0]=='Set_SensorServo.target' :
            self.sensorServo.target=float(msgIn[1])
        
        elif msgIn[0]=='Get_DistanceSensor.reading' :
            msgOut=str(self.distanceSensor.reading) 

        elif msgIn[0]=='Get_BeaconRead' :
            d,a=self.beaconReceiver.GetReading(int(msgIn[1]))
            msgOut=' '.join([str(d),str(a)])
            
        elif msgIn[0]=='Get_GiroRead' :
            vrz,rzi=self.giroSensor.GetReading()
            msgOut=' '.join([str(vrz),str(rzi)])
            
        else :
            print 'Unknown message:',msgIn
            msgOut='NACK'
            
        return msgOut

#==============================================================================
