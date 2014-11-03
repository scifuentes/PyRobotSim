#=============================================================================================
#
#Robot simulator - Main Executor
#  - imports the scenario file
#  - launches the simulation thread
#  - launches the visualization thread
#
#=============================================================================================
#by Santiago Cifuentes

import time
import thread


from SimWorld import WorldSimulation
from WorldView import WorldPainter

def Run(world):
    sim=WorldSimulation(world)
    paint=WorldPainter(world)
    
    #sim.run()
    
    sim.start()
    paint.start()
    try:
        paint.join()
        sim.join()
    except Exception,e:
        print 'uops: Run'
        print str(e)
        
    time.sleep(10)    
    
    
#==========================================    

if __name__ == "__main__":
    import sys
    import os
    import importlib
    
    currDir=os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(1,currDir)
    sys.path.insert(1,'PartsBox')

    #import provided scenario
    path_part = os.path.dirname(sys.argv[1])
    name_part = os.path.basename(sys.argv[1])
    sys.path.insert(1,path_part)
    ScenarioLib=importlib.import_module(name_part)

    world=ScenarioLib.world
    
    Run(world)