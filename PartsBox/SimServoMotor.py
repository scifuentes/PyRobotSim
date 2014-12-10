#=============================================================================================
#
#PyRobotSim - Part : Distance Sensor
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import ActiveObject
from math import copysign

class ServoMotor(ActiveObject):
    def __init__(self,axis=[1.,0.,0.],zero=[0.,0.,0.]):
        super(ServoMotor, self).__init__()
        
        self.pos=0.
        self.speed=0.
        self.target=None    #target angle, for non-continuous rotation control
        self.zero=zero
        self.axis=axis
        
    def UpdatePositions(self,t,dt):
        pos0=self.pos

        if self.target == None :
            self.pos+=self.speed*dt;
            
        else :
            self.pos+=copysign(self.speed,pos0-self.target)*dt;
            if ( (pos0>=self.target and self.pos<=self.target) 
                 or (pos0<=self.target and self.pos>=self.target) ):
                self.pos=self.target
                self.speed=0.
                self.target=None
        
        self.position.rx=self.zero[0]+self.axis[0]*self.pos
        self.position.ry=self.zero[1]+self.axis[1]*self.pos
        self.position.rz=self.zero[2]+self.axis[2]*self.pos
        
