==================================
|                                |
|     Python Robot Simulator     |
|                                |
==================================
by Santiago Cifuentes

===========================================================================================================

- PyRobotSim aims to be a lightweight, simple simulation framework for exploring control algorithms for one or many robots interacting among themselves and the world that surround them.

- The process of building a robot and the robot control logic tries to mimic the process of building a small real robot
	* Simulated robots are built by attaching 'parts' together, then adding simple commands to set or get properties of the different parts 
		e.g.: attaching a servo to somewhere in a chassis, then attaching a sensor to the servo; then adding a 'set_servo_angle' and 'get_sensor_value' commands
	* Each part is intended to take care of itself, so it can be plugged on any new robot
		The framework provides convenient methods to do this easily, like recursive calculation of a child's position in the world coordinates, just look at the existing parts!
	* Since it is written in python new parts can be added at your convenience
  
- The simulation part covers the physical elements and the low level, atomic, commands that will be present at the robot 'firmware'.
	- The main characteristics of the simulation system are :
		The simulation of all elements is done in a single thread in a synchronous, sequential way:
		1) All positions are updated ( by calling a update position method in all active world objects )
		2) Collisions handled : if the movement due to the position update lead to any contact between two object, the movement is restricted to just reach the contact point)
			- There is no dynamics simulation in the collisions (yet), objects just stop moving, they are forbidden to move in a direction that involves intersection of two objects
		3) All sensors are updated (by calling a update sensors method in all active world objects)
		4) All control requests are attended (by calling the associated method on all active world objects)
			- The default way on which the simulated objects get commands from the controller objects is to just attend UDP messages and answer to them, where each object have its own channel with its controller

- The control part covers the all the higher level logic of the robot, each controller runs in its own thread
	* Since typically the controller interact with the simulated object through UDP messages, and it runs in a different thread from the simulated object, it is possible to fully stop, block or crash the controller : the simulated object will keep going on
	* Actually there is no need on having a controller for each robot, nor to have it being executed by PyRobotSim. 
		Anything able to send UDP messages can control the simulated robots.

- A simple visualization is provided to see what is happening in the simulated world
	* It runs in its own thread and do not affect the simulation process itself.
		
===========================================================================================================
		
- Whole simulation starts by running SimMain.py and passing a scenario file to it
  e.g : python SimMain.py TestScenario\Scenario_1.py

  SimMain will :
	* launch a thread for the simulated world (and all their elements)
	* launch a thread for the representation of the simulated world (paints it using penGL)
	* launch a thread for each 'robot controller' element

- The Scenario file is just regular python script that defines the basic elements of the simulation
	* An instance of WorldDescirption() called 'world' and a list(can be empty) called 'controllers' is all that is needed in the scenario file
	* All simulated objects that are wanted in a simulation should be instantiated and added to the 'world'
		- These can be WallsObjects and WorldObjects
		- Since the scenario itself is a python script, the definitions can be in other python scripts, they only need to be imported.
	* All the control scripts that should be executed, need to be added to the 'controllers' list
		- It is also possible to manually launch the control scripts from a different command line once the simulated part is running
	
===========================================================================================================

- The currently provided 'parts' to build the robots are :
	* Differential Robot Chassis
	* Omnidirectional Robot Chassis
	* Servo Motor
	* Distance sensor
	* Compass Sensor
	* Gyro Sensor
	* Beacon Source & Beacon receiver
	
	* Also a simple UDP Server and Client classes are provided to handle interaction between the simulated robot and its control logic