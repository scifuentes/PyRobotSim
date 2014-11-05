#=============================================================================================
#
#PyRobotSim - Part : Compass
#
#=============================================================================================
#by Santiago Cifuentes

from math import pi
from SimWorld import ActiveObject

class Compass(ActiveObject):
    def __init__(self):
        super(Compass, self).__init__()
        self.reading=0
        
    def UpdateSensors(self,t,dt,world):
        wx,wy,wrz=self.WorldPosition()
        self.reading=wrz
        while self.reading>pi :
            self.reading-=2*pi
        while self.reading<-pi :
            self.reading+=2*pi    