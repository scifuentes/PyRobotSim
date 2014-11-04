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
import sys
import os
import importlib

def Run(world):
    from SimWorld import WorldSimulation
    from WorldView import WorldPainter    
    #import RobotLogic
    
    sim=WorldSimulation(world)
    paint=WorldPainter(world)

    sim.start()
    paint.start()
    #RobotLogic.main()
    try:
        paint.join()
        sim.join()
    
    except Exception,e:
        print 'uops: Run'
        print str(e)
        
    time.sleep(10)    
    
    
#==========================================    

if __name__ == "__main__":
   
    currDir=os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(1,currDir)
    sys.path.insert(1,'PartsBox')

    #import provided scenario
    scenario_path = os.path.dirname(sys.argv[1])
    scenario_file = os.path.basename(sys.argv[1])
    sys.path.insert(1,scenario_path)
    ScenarioLib=importlib.import_module(scenario_file)

    world=ScenarioLib.world
    Run(world)
    

    
    