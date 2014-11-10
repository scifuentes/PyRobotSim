#=============================================================================================
#
#PyRobotSim  - Simulated Robot HW definition and low level commands simulated actions
#                  Receives the control commands through a UDP link
#
#============================================================================================
# by Santiago Cifuentes

import math
import SimpleUDP

from SimOmnidirectionalChassis import OmnidirectionalChassisRobot
from SimRangeSensor import DistanceSensor
from SimServoMotor import ServoMotor
from SimBeacon import BeaconReceiver
from SimBeacon import BeaconSource

class SimOmniRobot(OmnidirectionalChassisRobot):
    def __init__(self,port=1005,beaconId=0):
        OmnidirectionalChassisRobot.__init__(self)
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
        
        elif msgIn[0]=='Set_moveXY' :
            self.motors.speedX=float(msgIn[1])
            self.motors.speedY=float(msgIn[2])
        
        elif msgIn[0]=='Set_motorRz' :
            self.motors.speedRZ=float(msgIn[1])
            
        elif msgIn[0]=='Set_SensorServo.target' :
            self.sensorServo.target=float(msgIn[1])
        
        elif msgIn[0]=='Get_DistanceSensor.reading' :
            msgOut=str(self.distanceSensor.reading) 

        elif msgIn[0]=='Get_BeaconRead' :
            d,a=self.beaconReceiver.GetReading(int(msgIn[1]))
            msgOut=' '.join([str(d),str(a)])
            
        else :
            print 'Unknown message:',msgIn
            msgOut='NACK'
            
        return msgOut

#==============================================================================
