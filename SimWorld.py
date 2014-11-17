#=============================================================================================
#
#PyRobotSim - Main World Simulation 'Engine'
#                  - Main world simulation methods 
#                  - Definition of world, simulated objects & their common methods
#
#=============================================================================================
# by Santiago Cifuentes

import threading
import time
import math
import sys
from OpenGL.GL import *
import MathAux
import copy
import itertools

class WorldSimulation(threading.Thread) :
    def __init__(self,world):
        threading.Thread.__init__(self)
        self.world=world
        self.T0=time.time()
        self.T=0.
        
    def run(self):
        
        i=0
        fr=20
        while True:
            dT=(time.time()-self.T0)-self.T
            self.T=time.time()-self.T0
            
            self.Sim(self.T,dT)
                
            time.sleep(1./fr)
            if i>10*fr :
                print '.', 
                i=0
            i+=1
                
            
    def Sim(self,T,dT):

        #Update All Positions
        for obj in self.world.simObjects:
            if isinstance(obj,ActiveObject):
                obj.pos0=copy.deepcopy(obj.position)
                obj._UpdateAllPositions(T,dT)
        
        #Handle collisions
        self.HandleCollisions()
            
        #Update All Sensors
        for obj in self.world.simObjects:
            if isinstance(obj,ActiveObject):
                obj._UpdateAllSensors(T,dT,self.world)
        
        #Attend requests
        for obj in self.world.simObjects:
            if isinstance(obj,ActiveObject):
                obj._AttendAllRequests()

            
    def HandleCollisions(self):
        def CheckBoxIntersection(box1,box2):
            [b1_xmin,b1_ymin,b1_xmax,b1_ymax]=box1
            [b2_xmin,b2_ymin,b2_xmax,b2_ymax]=box2
            if b1_xmax<b2_xmin or b1_xmin>b2_xmax or b1_ymax<b2_ymin or b1_ymin> b2_ymax :
                return False
            else:
                return True

        def CollisionCheck_Walls(sobj,wobj):
            sbox=sobj.WorldBox()
            wbox=wobj.WorldBox()
            if sbox :
                if CheckBoxIntersection(sbox,wbox) :
                    wshape=sobj.WorldShape()
                    for wall in wobj.walls:
                        for i in range(0,len(wshape)) :
                            j=(i+1)%len(wshape)
                            ix,iy=MathAux.LinesIntersection(wshape[i]+wshape[j],wall[0:4])
                            if ix != []:
                                return True
            return False
            
        def CollisionCheck_Objects(obj1,obj2):
            if obj1==obj2 :
                return False
            box1=obj1.WorldBox()
            box2=obj2.WorldBox()
            if box1 and box2 :
                if CheckBoxIntersection(box1,box2) :
                    wshape1=obj1.WorldShape()
                    wshape2=obj2.WorldShape()
                    for i1 in range(0,len(wshape1)):
                        j1=(i1+1)%len(wshape1)
                        for i2 in range(0,len(wshape2)):
                            j2=(i2+1)%len(wshape2)
                            
                            ix,iy=MathAux.LinesIntersection(wshape1[i1]+wshape1[j1],wshape2[i2]+wshape2[j2])
                            if ix != []:
                                return True
            return False


        for sobj in self.world.simObjects:
            if isinstance(sobj,ActiveObject) :
                for wobj in self.world.wallsObjects:
                    sobj.coll=CollisionCheck_Walls(sobj,wobj)
                    if sobj.coll :
                        break
        
        obj_combinations = itertools.combinations(self.world.simObjects,2)
        for objs in obj_combinations :
            if objs[0].shape and objs[1].shape:
                if CollisionCheck_Objects(objs[0],objs[1]):
                    objs[0].coll=True
                    objs[1].coll=True

        for sobj in self.world.simObjects:
            if sobj.shape :
                if sobj.coll :
                    sobj.position=copy.deepcopy(sobj.pos0)
                    if sobj.collision==False :
                        print sobj.name+'('+str(id(sobj))+'): Collision!'
                    sobj.collision=True
                else:
                    sobj.collision=False
                del sobj.coll
                del sobj.pos0
        
    


#==========================================    

class WorldDescription(object):
    def __init__(self):
        self.simObjects=[]
        self.wallsObjects=[]
    def AddSimObject(self,simObject):
        self.simObjects.append(simObject)
    def AddWallsObject(self,wallsObject):
        self.wallsObjects.append(wallsObject)
    def GetSimObjectsR(self):    
        objL=self.simObjects[:]
        for obj in self.simObjects:
            objL+=obj.GetChildsR()
        return objL
        
#==========================================    

class WallsObject(object):
    def __init__(self):
        self.walls=[]   #collection of walls, each defined as:[x0,y0,x1,y1]
        self.position=Position()
        
    def Paint(self):
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.position.rz*180./math.pi,0.,0.,1.)        
        glRotatef(self.position.ry*180./math.pi,0.,1.,0.)        
        glRotatef(self.position.rx*180./math.pi,1.,0.,0.)   

        glColor3f(0.0,0.0,0.0)
        
        glBegin(GL_LINES)
        for w in self.walls :
            [x0,y0,x1,y1]=w
            glVertex2f(x0,y0)
            glVertex2f(x1,y1)
        glEnd()


    def WorldBox(self):
        if not hasattr(self,'_box'):
            x_min=sys.float_info.max
            y_min=sys.float_info.max
            x_max=sys.float_info.min
            y_max=sys.float_info.min
            for w in self.walls:
                [x0,y0,x1,y1]=w
                x_min=min([x_min,self.position.x+x0,self.position.x+x1])
                y_min=min([y_min,self.position.y+y0,self.position.y+y1])
                x_max=max([x_max,self.position.x+x0,self.position.x+x1])
                y_max=max([y_max,self.position.y+y0,self.position.y+y1])
           
            self._box=[x_min,y_min,x_max,y_max]
        return self._box

#==========================================

class WorldObject(object):
    def __init__(self):
        self.parentObject=None
        self.childObjects=[]
        self.position=Position()
        self.shape=None
        self.name=''

        
    def AttachChild(self,child):
        self.childObjects.append(child)
        child.parentObject=self
    
    def IsParent(self,parent_candidate):
        if self.parentObject==parent_candidate:
            return True
        elif self.parentObject :
            return self.parentObject.IsParent(parent_candidate)
        else :
            return False
    
    def GetChildsR(self):
        rChildL=[]
        for child in self.childObjects :
            rChildL+=child.GetChildsR()
        rChildL+=self.childObjects
        return rChildL
        
    def GetParentR(self):
        if parentObject==None :
            return self
        else:
            return parentObject.GetParent()
            

    def _Paint(self):   #called from WorldView
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.position.rz*180./math.pi,0.,0.,1.)        
        glRotatef(self.position.ry*180./math.pi,0.,1.,0.)        
        glRotatef(self.position.rx*180./math.pi,1.,0.,0.) 
        self.Paint()
        for child in self.childObjects:
            glPushMatrix()
            child._Paint()
            glPopMatrix()  
            
    def Paint(self):
        if self.shape :
            if self.collision:
                glColor3f(1.0,0.0,0.0)
            else:
                glColor3f(0.0,1.0,0.0)
            
            if len(self.shape)>2:
                glBegin(GL_POLYGON)
            elif len(self.shape)==2:
                glBegin(GL_LINES)
            else :
                return
                
            for v in self.shape :
                glVertex2f(v[0],v[1])
            glEnd()
            
            
    def WorldPosition(self,x=0.,y=0.):
        if not hasattr(self,'_wpos'):
            if self.parentObject != None :
                [xp,yp,rzp]=self.parentObject.WorldPosition()
            else :
                [xp,yp,rzp]=[0,0,0]
            
            xs,ys=MathAux.Rotate([self.position.x,self.position.y],rzp)
            self._wpos=[xs+xp,ys+yp,rzp+self.position.rz]
        
        [swx,swy,swrz]=self._wpos
        
        if(x!=0. or y!=0.) :
            [xl,yl]=MathAux.Rotate([x,y],swrz)
        else:
            [xl,yl]=[0,0]
            
        xw=swx+xl
        yw=swy+yl           
        
        #print 'rp('+str(id(self))+'):'+str([xw,yw,rzw])
        return xw,yw,swrz

    def WorldShape(self):
        if self.shape :
            if not hasattr(self,'_wshape'):
                self._wshape=[]
                for v in self.shape:
                    vwx,vwy,vwrz=self.WorldPosition(v[0],v[1])
                    self._wshape.append([vwx,vwy])
            return self._wshape
            
    def WorldBox(self):
        if self.shape :
            if not hasattr(self,'_box'):
                ws=self.WorldShape()
                x_min=sys.float_info.max
                y_min=sys.float_info.max
                x_max=sys.float_info.min
                y_max=sys.float_info.min
                for v in ws:
                    x_min=min([x_min,v[0]])
                    y_min=min([y_min,v[1]])
                    x_max=max([x_max,v[0]])
                    y_max=max([y_max,v[1]])
                            
                self._box=[x_min,y_min,x_max,y_max]
            return self._box     
        
#==========================================

class ActiveObject(WorldObject):
    def __init__(self):
        super(ActiveObject,self).__init__()
        self.collision=False
        
    def _UpdateAllPositions(self,t,dt) :
        def CleanWorldReferences(obj):
            if hasattr(obj,'_wshape'):
                del obj._wshape
            if hasattr(obj,'_box'):
                del obj._box
            if hasattr(obj,'_wpos'):
                del obj._wpos   
                
        self.UpdatePositions(t,dt)
        for child in self.childObjects:
            if isinstance(child,ActiveObject):
                child._UpdateAllPositions(t,dt)
            else :
                CleanWorldReferences(child)
        CleanWorldReferences(self)
        
    def _UpdateAllSensors(self,t,dt,world) :
        self.UpdateSensors(t,dt,world)
        for child in self.childObjects:
            if isinstance(child,ActiveObject):
                child._UpdateAllSensors(t,dt,world)
        
    def _AttendAllRequests(self) :
        self.AttendRequests()
        for child in self.childObjects:
            if isinstance(child,ActiveObject):
                child._AttendAllRequests()
        

    def UpdatePositions(self,t,dt) :
        pass
        
    def UpdateSensors(self,t,dt,world) :
        pass
        
    def AttendRequests(self) :
        pass

#==========================================
        
class Position:
    def __init__(self):
        self.x=0.
        self.y=0.
        self.z=0.
        self.rx=0.
        self.ry=0.
        self.rz=0.

