#=============================================================================================
#
#PyRobotSim - Common math functions
#
#=============================================================================================
#by Santiago Cifuentes

import math

def Rotate(pos,angle):
    pos_x,pos_y=pos
    out_x=  pos_x*math.cos(angle) -pos_y*math.sin(angle)
    out_y=  pos_x*math.sin(angle) +pos_y*math.cos(angle)    
    return [out_x,out_y]
    
def LinesIntersection(l0,l1):
    #in the same region
    [l0x0,l0y0,l0x1,l0y1]=l0
    [l1x0,l1y0,l1x1,l1y1]=l1

    xi=[]
    yi=[]    
    
    if l0x0!=l0x1 and l1x0!=l1x1 :
        m0=(l0y0-l0y1)/(l0x0-l0x1)
        b0=l0y0-m0*l0x0
        m1=(l1y0-l1y1)/(l1x0-l1x1)
        b1=l1y0-m1*l1x0
        if m0!=m1 :
            xi=(b1-b0)/(m0-m1)
            yi=m0*xi+b0
    elif l1x0!=l1x1 :
        m1=(l1y0-l1y1)/(l1x0-l1x1)
        b1=l1y0-m1*l1x0
        xi=l0x0
        yi=m1*xi+b1
    elif l0x0!=l0x1 :
        m0=(l0y0-l0y1)/(l0x0-l0x1)
        b0=l0y0-m0*l0x0
        xi=l1x0
        yi=m0*xi+b0
    
    e=0.01
    if ( xi!=[] and xi>=min([l0x0,l0x1])-e and xi<=max([l0x0,l0x1])+e and 
        xi>=min([l1x0,l1x1])-e and xi<=max([l1x0,l1x1])+e and
        yi>=min([l0y0,l0y1])-e and yi<=max([l0y0,l0y1])+e and
        yi>=min([l1y0,l1y1])-e and yi<=max([l1y0,l1y1])+e ) :        
        return xi,yi
    else:
        return [],[]


def AngleDif(a0,a1):
    d=a1-a0
    while d>math.pi :
        d-=2*math.pi
    while d<-math.pi :
        d+=2*math.pi
    return d

