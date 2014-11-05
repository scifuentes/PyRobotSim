#=============================================================================================
#
#Robot simulator - Piece : Distance Sensor
#
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import ActiveObject

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
        self.pos+=self.speed*dt;
        
        if self.target != None :
            if ( (pos0>=self.target and self.pos<=self.target) 
                 or (pos0<=self.target and self.pos>=self.target) ):
                self.pos=target
                self.speed=0.
                self.target=None
        
        self.position.rx=self.zero[0]+self.axis[0]*self.pos
        self.position.ry=self.zero[1]+self.axis[1]*self.pos
        self.position.rz=self.zero[2]+self.axis[2]*self.pos
        
