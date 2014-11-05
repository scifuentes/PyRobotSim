#=============================================================================================
#
#Robot simulator - Part : Distance Sensor
#
#=============================================================================================
#by Santiago Cifuentes

import math
from SimWorld import ActiveObject
from OpenGL.GL import *
import MathAux

class DistanceSensor(ActiveObject):
    def __init__(self):
        super(DistanceSensor, self).__init__()
        
        self.range=80.
        self.reading=80.
        self.contact=[]
        
    def UpdateSensors(self,t,dt,world):
        wx0,wy0,wrz0=self.WorldPosition()
        wx1,wy1,wrz1=self.WorldPosition(self.range,0.)
        #print '---'
        self.contact=None
        r2=self.range*self.range
        
        for wobj in world.wallsObjects:
            for w in wobj.walls:
                xi,yi=MathAux.LinesIntersection([wx0,wy0,wx1,wy1],[w[0],w[1],w[2],w[3]])
                if xi!=[]:
                    d2=(wx0-xi)*(wx0-xi)+(wy0-yi)*(wy0-yi)
                    if d2<r2:
                        r2=d2
                        self.contact=w
                        
        for aobj in world.simObjects:
            if not self.IsParent(aobj) :
                wshape=aobj.WorldShape()
                if wshape :
                    for v0,v1 in zip(wshape,wshape[1:]+[wshape[0]]) :
                        xi,yi=MathAux.LinesIntersection([wx0,wy0,wx1,wy1],[v0[0],v0[1],v1[0],v1[1]])
                        if xi!=[]:
                            d2=(wx0-xi)*(wx0-xi)+(wy0-yi)*(wy0-yi)
                            if d2<r2:
                                r2=d2
                                self.contact=w
                        
        self.reading=math.sqrt(r2)        
        
    def Paint(self):
        if self.contact==None:
            glColor3f(.5,.5,0.5)
            glBegin(GL_LINES)
            glVertex2f(0.,0.)
            glVertex2f(self.range,0.)
            glEnd()
        else:
            glColor3f(1.0,0.0,0.0)
            glBegin(GL_LINES)
            glVertex2f(0.,0.)
            glVertex2f(self.reading,0.)
            glEnd()
        
        
