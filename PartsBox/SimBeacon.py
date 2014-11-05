#=============================================================================================
#
#Robot simulator - Part : Beacon Transmitter & Receiver
#
#=============================================================================================
#by Santiago Cifuentes

from math import pi, sqrt,atan2
from SimWorld import WorldObject, ActiveObject
from MathAux import AngleDif

class BeaconSource(WorldObject):
    def __init__(self,id=0):
        super(BeaconSource, self).__init__()
        self.id=id

class BeaconReceiver(ActiveObject):
    def __init__(self):
        super(BeaconReceiver, self).__init__()
        self.sensed=[]
        
    def UpdateSensors(self,t,dt,world):
        sL=[]
        for obj in world.GetSimObjectsR(): 
            if isinstance(obj,BeaconSource):
                spx,spy,srz=self.WorldPosition()
                bpx,bpy,brz=obj.WorldPosition()
                dx=bpx-spx
                dy=bpy-spy
                distance=sqrt(dx**2+dy**2)
                angle=AngleDif(0,atan2(dy,dx)-srz)
                sL.append([obj.id, distance, angle])
        self.sensed=sL
       
    
    def GetReading(self,id):
        for s in self.sensed:
            if s[0]==id :
                return s[1],s[2]
        return -1,0
