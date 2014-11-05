# WallsObject for the techno-challenge defining the play field

from SimWorld import WallsObject
from SimBeacon import BeaconSource

field=WallsObject()
field.walls=[]
l=350.
w=200.
field.walls.append([ l,-w/2, l, w/2])
field.walls.append([ 0,-w/2, 0, w/2])
field.walls.append([ l, w/2, 0, w/2])
field.walls.append([ l,-w/2, 0,-w/2])

fieldBeacon=BeaconSource(4)
fieldBeacon.position.x=l
fieldBeacon.position.y=0