#=============================================================================================
#
#PyRobotSim  - Basic Scenario definition
#                  - instantiates the world object and attaches all the simulated elements to the world object
#                  - instantiate all the controllers and add them to the controllers list
#
#=============================================================================================
#by Santiago Cifuentes

from SimWorld import WorldDescription
import Field
import SimRobot2
import SheepLogic2
import DogLogic2
import math


world=WorldDescription()        #needed by SimMain
controllers=[]                  #needed by SimMain


world.AddWallsObject(Field.field)
world.AddSimObject(Field.fieldBeacon)


sheep=SimRobot2.SimRobot(1005,3)
sheep.name='sheep'
sheep.position.x=Field.l-40
sheep.position.y=40 #Field.w/2-30
sheep.position.rz=math.pi+1
sheepControl=SheepLogic2.SheepLogic(1005)
world.AddSimObject(sheep)



dog1=SimRobot2.SimRobot(1006,1)
dog1.name='dog1'
dog1.position.x=50
dog1.position.y=Field.w/2-30
dog1.position.rz=0
dog1.beaconReceiver.name='dog1_beacon'
dog1Control=DogLogic2.DogLogic(1006)
world.AddSimObject(dog1)



dog2=SimRobot2.SimRobot(1007,2)
dog2.name='dog2'
dog2.position.x=50
dog2.position.y=-Field.w/2+30
dog1.position.rz=-.6
dog2Control=DogLogic2.DogLogic(1007)
world.AddSimObject(dog2)

