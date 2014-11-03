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

world=WorldDescription()

robot1=SimRobot(1006)
robot1.position.x=0 
robot1.position.y=15
robot1.motorR.speed=10
robot1.motorL.speed=9
robot1.servoBC.speed=1
world.AddSimObject(robot1)

robot2=SimRobot(1007)
robot2.position.x=-10
robot2.position.y=-14 
#robot2.motorR.speed=9
#robot2.motorL.speed=10
#robot2.servoBC.speed=1
world.AddSimObject(robot2)

beacon=BeaconSource(0)
beacon.position.x=100
world.AddSimObject(beacon)


room=WallsObject()
room.walls=[[-60,-100,-60,100],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)