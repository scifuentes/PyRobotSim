#=============================================================================================
#
#Robot simulator - Basic world definition
#                  - instantiates the world object 
#                  - attaches all the elements present on it
#
#=============================================================================================

from SimWorld import WorldDescription
from SimWorld import WallsObject
from SimRobot1 import SimRobot
from SimBeacon import BeaconSource
from RobotLogic import RobotLogic

world=WorldDescription()
controlers=[]

room=WallsObject()
room.walls=[[-60,-150,-60,150],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)

beacon=BeaconSource(0)
beacon.position.x=100
world.AddSimObject(beacon)

robot1=SimRobot(1006)
robot1.position.x=0 
robot1.position.y=15
robot1.motorR.speed=10
robot1.motorL.speed=9
robot1.servoBC.speed=6
world.AddSimObject(robot1)

control1=RobotLogic(1006)
controlers.append(control1)

robot2=SimRobot(1007)
robot2.position.x=-10
robot2.position.y=-14 
robot2.servoBC.speed=4
world.AddSimObject(robot2)

control2=RobotLogic(1007)
controlers.append(control2)



