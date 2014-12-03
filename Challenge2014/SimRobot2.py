#=============================================================================================
#
#PyRobotSim  - Simulated Robot HW definition and low level commands simulated actions
#                  Receives the control commands through a UDP link
#
#============================================================================================
# by Santiago Cifuentes


import math
import SimpleUDP
import time

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
        
        self.distanceSensorF=DistanceSensor()
        self.distanceSensorF.range=250.
        self.AttachChild(self.distanceSensorF)

        self.beaconReceiver=BeaconReceiver()
        self.beaconReceiver.aperture=240./180.*math.pi
        self.beaconReceiver.max_range=400
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
        #print '@'+self.name,'Received:',msgIn
        
        msgOut=''
        msgIn=msgIn.split()
        
        if msgIn[0]=='Tic' :
            msgOut='Toc'
        
        elif msgIn[0]=='Set_Forward_Speed' :        #used alone will set the speed for a continuous forward movement
            self.motorR.speed=float(msgIn[1])
            self.motorL.speed=float(msgIn[1])
        
        elif msgIn[0]=='Set_Turn_Speed' :
            self.motorR.speed=-float(msgIn[1])
            self.motorL.speed=float(msgIn[1])
            
        elif msgIn[0]=='Move_Forward' :             #sets a controlled movement: after the requested amount(angle) is completed the movement stops
            self.motorR.target=self.motorR.pos+float(msgIn[1])
            self.motorL.target=self.motorL.pos+float(msgIn[1])
            self.motorR.speed=float(msgIn[2])
            self.motorL.speed=float(msgIn[2])
            
        elif msgIn[0]=='Move_Turn' :
            self.motorR.target=self.motorR.pos-float(msgIn[1])
            self.motorL.target=self.motorL.pos+float(msgIn[1])            
            self.motorR.speed=-float(msgIn[2])
            self.motorL.speed=float(msgIn[2])
            
        elif msgIn[0]=='Check_Move_Done' :
            msgOut=str(self.motorR.target==None and self.motorL.target==None) 
            
        elif msgIn[0]=='Stop_Move' :
            self.motorR.speed=0
            self.motorL.speed=0
            self.motorR.target==None
            self.motorL.target==None            
        
        elif msgIn[0]=='Set_SensorServo_Speed' :
        
            self.sensorServo.speed=float(msgIn[1])  

        elif msgIn[0]=='Move_SensorServo' :
            self.sensorServo.target=float(msgIn[1])
            self.sensorServo.speed=float(msgIn[2])    
            
        elif msgIn[0]=='Get_SensorServo_Pos' :
            msgOut=str(self.sensorServo.pos)      
            
        elif msgIn[0]=='Get_DistanceSensor.reading' :
            msgOut=str(self.distanceSensor.reading) 
            
        elif msgIn[0]=='Get_DistanceSensorF.reading' :
            msgOut=str(self.distanceSensorF.reading) 

        elif msgIn[0]=='Get_BeaconRead' :
            d,a=self.beaconReceiver.GetReading(int(msgIn[1]))
            if d==self.distanceSensor.range: d=-1
            msgOut=' '.join([str(d),str(a)])
            print 'Beacon',msgIn[1],d,a*180/math.pi
            
        elif msgIn[0]=='Get_GiroRead' :
            vrz,rzi=self.giroSensor.GetReading()
            msgOut=' '.join([str(vrz),str(rzi)])
            
        elif msgIn[0]=='Reset_GiroRead' :
            self.giroSensor.Reset()
           
        else :
            print 'Unknown message: ',msgIn
            msgOut='NACK'
            
        return msgOut

#==============================================================================

class SimRobotClient:
    def __init__(self,ip,port):
        self.com=SimpleUDP.Client(ip,port)

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
        
    def GetDistanceSensorF(self):    
        return float(self.com.Request('Get_DistanceSensorF.reading')[0])
        
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
        return float(self.com.Request('Get_SensorServo_Pos')[0])        
