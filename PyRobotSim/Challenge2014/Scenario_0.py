#=============================================================================================
#
#Robot simulator - Basic world definition
#                  - instantiates the world object 
#                  - attaches all the elements present on it
#
#=============================================================================================

from SimWorld import WorldDescription, WallsObject
from SimRobot1 import SimRobot
from RobotLogic import RobotLogic
world=WorldDescription()
controlers=[]


room=WallsObject()
room.walls=[[-60,-100,-60,100],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)

robot1=SimRobot(1005)
world.AddSimObject(robot1)

control1=RobotLogic(1005)
controlers.append(control1)