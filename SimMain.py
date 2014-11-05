#=============================================================================================
#
#PyRobotSim - Main Executor
#               - imports the scenario file
#               - launches the simulation thread
#               - launches the visualization thread
#
#=============================================================================================
#by Santiago Cifuentes

import time
import thread
import sys
import os
import importlib

def Run(world,controlers):
    from SimWorld import WorldSimulation
    from WorldView import WorldPainter    
    
    sim=WorldSimulation(world)
    paint=WorldPainter(world)

    sim.start()
    paint.start()

    for control in controlers:
        control.start()
        
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
    if scenario_file.endswith('.py'):
        scenario_file=scenario_file[:-3]
    
    sys.path.insert(1,scenario_path)
    s=importlib.import_module(scenario_file)

    Run(s.world,s.controllers)
     
    