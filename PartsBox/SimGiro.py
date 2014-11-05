#=============================================================================================
#
#Robot simulator - Part : Gyro Sensor
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import ActiveObject

class Gyro(ActiveObject):
    def __init__(self):
        super(Compass, self).__init__()
        self.reading=0.
        self.last_rz=None   #last read orientation
        self.rzi=0.         #integral accumulator
        self.vrz=0.         #last speed reading
        
    def UpdateSensors(self,t,dt,world):
        wx,wy,wrz=self.WorldPosition()
        if not self.last_rz :
            self.last_rz=wrz
        self.rzi+=(wrz-self.last_rz)
        self.vrz=(wrz-self.last_rz)/dt

        self.last_rz=wrz

        
    def Reset(self):
        self.rzi=0  

    def GetReading(self):
        return self.vrz, self.rzi
