#=============================================================================================
#
#PyRobotSim - Part : Omnidirectional Chassis
#
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import ActiveObject
from math import sqrt
import MathAux
from OpenGL.GL import *

class DummyMotor:
    pass

class DiferentialChassisRobot(ActiveObject):
    
    
    def __init__(self):
        super(DiferentialChassisRobot, self).__init__()
        #lets build the chassis
        self.wheel_diameter=5.
        self.wheel_separation=10.
        
        self.motors=DummyMotor()
        self.motors.speedX=0
        self.motors.speedY=0
        self.motors.speerRZ=0
        

    def UpdatePositions(self,t,dt):
            
        rob_dx=self.motors.speedX*dt
        rob_dy=self.motors.speedY*dt
        rob_drz=self.motors.speedRZ*dt

        [wrl_dx,wrl_dy]=MathAux.Rotate([rob_dx,rob_dy],self.position.rz)    
        self.position.x+=wrl_dx
        self.position.y+=wrl_dy
        self.position.rz+=drz  
        

    def Paint(self):
        super(DiferentialChassisRobot,self).Paint()


