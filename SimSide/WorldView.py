# -*- coding: utf-8 -*-
"""
Created on Wed Nov 06 07:34:00 2013

@author: Tagore
"""

#=============================================================================================
#
#Robot simulator - World Visualization
#
#Rendering of the Robot hardware and the world
#  Build as a client of the HW simulation
#
#=============================================================================================

import math
import time
import socket
import threading

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#from SimWorld import WorldObject

class WorldPainter(threading.Thread):
    def __init__(self,world):
        threading.Thread.__init__(self)
        self.world=world
        
    def run(self):
        self.GL_Init()

        glutMainLoop()
            
    def GL_Init(self):
        
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutCreateWindow("Sim World")
        
        glClearColor(1.0,1.0,1.0,0.0)
        glMatrixMode(GL_PROJECTION)
        
        xMax,xMin,yMax,yMin=self.GetWorldLimits()
        xc=(xMin+xMax)/2
        yc=(yMin+yMax)/2
        xs=xMax-xMin
        ys=yMax-yMin
        ez=max([xs+20,ys+20])/math.sin(30./180.*math.pi)*math.cos(30./180.*math.pi)
        
        glLoadIdentity()
        gluPerspective(40.,-4.0/3.0,1.,ez)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(xc,yc,ez,
                  xc,yc,0,
                  1,0,0)
        
        
        glutDisplayFunc(self.Display_cb)
        
    def Display_cb(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.PaintWorld()
        
        self.PaintSimObjects()
        
        self.OnScreenText()
        
        glutSwapBuffers()

        glutTimerFunc(33,self.Timer_cb,0)
        
    def Timer_cb(self,id):
        glutPostRedisplay() 
    
    
    #====================================
    
    def PaintSimObjects(self):
        for obj in self.world.simObjects:
            glPushMatrix()
            obj._Paint()
            glPopMatrix() 
            
    def PaintWorld(self):
        glPushMatrix()
        for obj in self.world.wallsObjects:
            obj.Paint()
        glPopMatrix()    
            
    def OnScreenText(self):
        glColor3f(0.0, 0.0, 0.0);
        
        text=''
        text+='boo: ({0:.2f},{1:.2f})@{2:.2f}\n'.format(1.,2.,3.)
        
        glRasterPos2f(300.0, -300);
        glutBitmapString(GLUT_BITMAP_HELVETICA_12,text )
        
    def GetWorldLimits(self):
        
        return [200,-200,200,-200]    
