import sys
import time
import numpy as np
import numpy.random as npr

sys.path.append('..')
from simulation import vrep
from robots.ur5 import UR5
from grippers.rg2 import RG2
import utils.vrep_utils as utils
from utils import transformations

VREP_BLOCKING = vrep.simx_opmode_blocking

def main():
  # Attempt to connect to simulator
  vrep.simxFinish(-1)
  sim_client = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
  if sim_client == -1:
    print 'Failed to connect to simulation. Exiting...'
    exit()
  else:
    print 'Connected to simulation.'

  # Create UR5 and restart simulator
  gripper = RG2(sim_client)
  ur5 = UR5(sim_client, gripper)
  vrep.simxStopSimulation(sim_client, VREP_BLOCKING)
  time.sleep(2)
  vrep.simxStartSimulation(sim_client, VREP_BLOCKING)
  time.sleep(2)

  # Generate a cube
  position = [0., 0.5, 0.0]
  orientation = [0, 0, np.radians(45)]
  color = [255, 0, 0]
  cube = utils.generateCube(sim_client, 'cube', position, orientation, color)
  time.sleep(2)

  # Execute pick on cube
  pose = transformations.euler_matrix(np.pi/2, np.radians(45), np.pi/2)
  pose[:3,-1] = [0, 0.5, 0.0]
  offset = 0.2
  ur5.pick(pose, offset)

  pose = transformations.euler_matrix(np.pi/2, 0.0, np.pi/2)
  pose[:3,-1] = [0.0, 0.5, 0.5]
  ur5.moveTo(pose)

  pose = transformations.euler_matrix(np.pi/2, 0.0, np.pi/2)
  pose[:3,-1] = [0.25, 0.25, 0.0]
  ur5.place(pose)

  # Wait for arm to move the exit
  time.sleep(1)
  vrep.simxStopSimulation(sim_client, VREP_BLOCKING)
  exit()

if __name__ == '__main__':
  main()
