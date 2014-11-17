#=============================================================================================
#
#PyRobotSim  - Basic world definition
#                  - instantiates the world object and controllers list
#                  - attaches all simulated elements to the world object
#                  - adds the control logic elements to the controller lists
#
#=============================================================================================

from SimWorld import WorldDescription
from SimWorld import WallsObject
from SimBeacon import BeaconSource, BeaconReceiver
from math import pi

world=WorldDescription()
controllers=[]

room=WallsObject()
room.walls=[[-60,-150,-60,150],
            [100,-100,100,100],
            [-100,100,100,100],
            [-100,-100,100,-100]]
world.AddWallsObject(room)

beacon=BeaconSource(0)
beacon.position.x=0
beacon.position.y=0
beacon.position.rz=pi
world.AddSimObject(beacon)

beaconS=BeaconReceiver()
beaconS.position.x=-100
beaconS.position.y=-1
beaconS.position.rz=-pi/4
world.AddSimObject(beaconS)


