#=============================================================================================
#
#Robot simulator - Basic world definition
#                  - instantiates the world object 
#                  - attaches all the elements present on it
#
#=============================================================================================

from SimWorld import WorldDescription, WallsObject
from SimRobot1 import SimRobot

world=WorldDescription()

robot1=SimRobot(1005)
world.AddSimObject(robot1)

room=WallsObject()
room.walls=[[-60,-100,-60,100],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)