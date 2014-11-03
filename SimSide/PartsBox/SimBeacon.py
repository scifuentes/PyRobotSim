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
        self.id=0

class BeaconReceiver(ActiveObject):
    def __init__(self,id=0):
        super(BeaconReceiver, self).__init__()
        self.id=0
        self.distance=-1
        self.angle=-0
        
    def UpdateSensors(self,t,dt,world):
        self.distance=-1
        for obj in world.simObjects: 
            if isinstance(obj,BeaconSource):
                if obj.id==self.id :
                    spx,spy,srz=self.WorldPosition()
                    bpx,bpy,brz=obj.WorldPosition()
                    self.distance=sqrt((spx-bpx)**2+(spy-bpy)**2)
                    self.angle=atan2(bpy-spy,bpx-spx)
