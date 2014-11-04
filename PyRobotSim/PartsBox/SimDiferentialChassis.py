#=============================================================================================
#
#Robot simulator - Main Piece : Diferential Chassis
#
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import ActiveObject
from math import *
import MathAux
from OpenGL.GL import *

class SimpleMotor:
    pass

class DiferentialChassisRobot(ActiveObject):
    
    
    def __init__(self):
        super(DiferentialChassisRobot, self).__init__()
        #lets build the chassis
        self.wheel_diameter=5.
        self.wheel_separation=10.
        
        self.motorR=SimpleMotor()
        self.motorL=SimpleMotor()
        self.motorR.speed=0.
        self.motorR.pos=0.
        self.motorL.speed=0.
        self.motorL.pos=0.
        
        
    def UpdatePositions(self,t,dt):
            
        self.motorR.pos+=self.motorR.speed*dt
        self.motorL.pos+=self.motorL.speed*dt
        
        l0=self.motorL.speed*self.wheel_diameter/2.*dt
        l1=self.motorR.speed*self.wheel_diameter/2.*dt
        
        if l0==l1:    
            #-- straight movement
            drz=0.
            rob_dx=(l0+l1)/2.
            rob_dy=0.
        else:
            #-- arc movement    
            r=self.wheel_separation/2.*(l0+l1)/(l0-l1)
            if r!=0 :
                drz=(l0+l1)/2./r
                rob_dx=sin(drz)*r
                rob_dy=(1-cos(drz))*r
            else:
                drz=l0/(self.wheel_separation/2.)
                rob_dx=0.
                rob_dy=0.
        
        [wrl_dx,wrl_dy]=MathAux.Rotate([rob_dx,rob_dy],self.position.rz)    
        self.position.x+=wrl_dx
        self.position.y+=wrl_dy
        self.position.rz+=drz  
        

    def Paint(self):
        #wheels
        super(DiferentialChassisRobot,self).Paint()
        wd=self.wheel_diameter
        wt=2.
        ws=self.wheel_separation
        
        glColor3f(0.0,0.0,0.0)
        glBegin(GL_POLYGON)
        glVertex3f(wd/2.,ws/2.,0.0)
        glVertex3f(wd/2.,ws/2.-wt,0.0)
        glVertex3f(-wd/2.,ws/2.-wt,0.0)
        glVertex3f(-wd/2.,ws/2.,0.0)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex3f(wd/2.,-ws/2.+wt,0.0)
        glVertex3f(wd/2.,-ws/2.,0.0)
        glVertex3f(-wd/2.,-ws/2.,0.0)
        glVertex3f(-wd/2.,-ws/2.+wt,0.0)
        glEnd()
        

