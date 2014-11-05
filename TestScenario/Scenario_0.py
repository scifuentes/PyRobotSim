#=============================================================================================
#
#Robot simulator - Basic Scenario definition
#                  - instantiates the world object and attaches all the simulated elements to the world object
#                  - instantiate all the controllers and add them to the controllers list
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import WorldDescription, WallsObject
from SimRobot1 import SimRobot
from RobotLogic import RobotLogic
world=WorldDescription()
controllers=[]


room=WallsObject()
room.walls=[[-60,-150,-60,150],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)

robot1=SimRobot(1005)
world.AddSimObject(robot1)

control1=RobotLogic(1005)
controllers.append(control1)