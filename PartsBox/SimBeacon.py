#=============================================================================================
#
#PyRobotSim - Part : Beacon Transmitter & Receiver
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
        self.apperture=pi/2.

class BeaconReceiver(ActiveObject):
    def __init__(self):
        super(BeaconReceiver, self).__init__()
        self.sensed=[]
        self.max_range=300
        self.apperture=pi/2.
        
    def UpdateSensors(self,t,dt,world):
        sL=[]
        for obj in world.GetSimObjectsR(): 
            if isinstance(obj,BeaconSource):
                spx,spy,srz=self.WorldPosition()    #sensor world position
                bpx,bpy,brz=obj.WorldPosition()     #beacon world position
                dx=bpx-spx
                dy=bpy-spy
                distance=sqrt(dx**2+dy**2)
                angle=AngleDif(0,atan2(dy,dx)-srz)
                if (distance<=self.max_range and abs(angle)<=self.apperture/2.    #within sensor distance and aperture
                   and abs(AngleDif(angle+pi,brz)) <= obj.apperture/2. ):         #within beacon aperture
                        sL.append([obj.id, distance, angle])
                else:
                    sL.append([obj.id, self.max_range, 0])
                print sL[-1],obj.id,',',dx,dy,distance,',',srz,brz,angle,',',abs(AngleDif(angle+pi,brz))

        self.sensed=sL
    
    def GetReading(self,id):
        for s in self.sensed:
            if s[0]==id :
                return s[1],s[2]
        return -1,0
