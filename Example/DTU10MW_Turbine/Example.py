
from HAWC2_TCP import HAWC2Interface
import numpy as np
import sys

simTime, sampleTime          = 100, 0.01
HAWC2Interface.N_iter        = int(simTime/sampleTime)
HAWC2Interface.HAWC2_command = 'hawc2mb.exe'



@HAWC2Interface.update_function
def update(array1):
    '''This function is integrated into a HAWC2 simulation. It is called each
    time step. It receives a numpy array of the HAWC2 outputs as the first
    argument, and keyword arguments supplied by the HAWC2Interface.run()
    function. The function then returns a list or numpy array back to HAWC2 as
    an input vector. '''
    t, azim = array1[0], array1[1]

    theta    =   [0,0,0]
    theta[0] =   1*np.cos(azim + 0.174)
    theta[1] =   1*np.cos(azim + 0.174 - 2/3*np.pi)
    theta[2] =   1*np.cos(azim + 0.174 - 4/3*np.pi)

    return theta
    
    
    
def main():
    htc_file = sys.argv[1]
    HAWC2Interface.run(htc_file)



if __name__ == '__main__':
    main()
