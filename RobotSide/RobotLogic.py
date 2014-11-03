import SimpleUDP
import time
from math import radians, degrees, pi
from MathAux import AngleDif

com=SimpleUDP.Client('127.0.0.1',1005)
def main():
    
    while True:
    
        d_fr,d_fl,d_bc=GetDistanceSensors()
        o_z= GetOrientation()
        print 'Status = ',d_fr,d_fl,o_z
        
        if d_fr >=80 and d_fl >=80 :
            SetSpeed(20,20)        
        elif d_fr >20 and d_fl >20 :
            SetSpeed(5,5)
        else :
            print 'Collision Risk, turning'
            SetSpeed(0,0)
            r0=GetOrientation()
            r1=AngleDif(0,r0+radians(180))
            da=AngleDif(r0,r1)
                
            print 'Orientation = ',r0,r1

                
            while abs(da)>radians(0.1):
                if abs(da)>radians(10):
                    ts=5
                else:
                    ts=degrees(abs(da))/2.0
                if (da>0):
                    SetSpeed(-ts,ts)
                else:
                    SetSpeed(ts,-ts)                
                r0=GetOrientation()
                da=AngleDif(r0,r1)
                print 'Orientation = ',r0,r1,da

            print 'Turn Done',r0
            SetSpeed(0,0)
    
def GetDistanceSensors():    
    d_fr=float(com.Request('Get_DistanceSensorFR.reading')[0])
    d_fl=float(com.Request('Get_DistanceSensorFL.reading')[0])
    d_bc=float(com.Request('Get_DistanceSensorBC.reading')[0])
    return d_fr,d_fl,d_bc
    
def GetOrientation():
    return float(com.Request('Get_Compass.reading')[0])

def SetSpeed(vr,vl):
    if (vr!=None):
        com.Send((' ').join(['Set_motorR.speed',str(vr)]))
    if (vl!=None):
        com.Send((' ').join(['Set_motorL.speed',str(vl)]))    
    time.sleep(0.05)
    
if __name__ == "__main__":
    main()