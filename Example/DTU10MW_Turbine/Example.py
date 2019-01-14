"""
Institution : DTU
Course      : Master Thesis Project
Date        : 20-Jan-2018
Author      : Jaime Liew - S141777
Email       : Jaimeliew1@gmail.com
Description : Example script for HAWC2_TCP link. Adds a sinusoidal pitch angle
demand to each blade.
"""

from HAWC2_TCP import HAWC2Interface
from numpy import pi, cos

HAWC2_COMMAND = 'hawc2mb.exe'

def main():
    '''HAWC2Interface is an object that links the HAWC2 executable
    (HAWC2_COMMAND) with a python function (update)'''
    HAWC2 = HAWC2Interface(HAWC2_COMMAND, update)

    '''run the simulation by specifying the relative htc filepath and the number
    of iterations in the simulation. Additional keyword arguments will be passed
    to the update function (in this case, amp).'''
    simTime, sampleTime = 100, 0.01
    N_iters = int(simTime/sampleTime)

    HAWC2.run('htc/TCPExample.htc', N_iters, amp=0.02)



def update(array1, amp=0.02):
    '''This function is integrated into a HAWC2 simulation. It is called each
    time step. It receives a numpy array of the HAWC2 outputs as the first
    argument, and keyword arguments supplied by the HAWC2Interface.run()
    function. The function then returns a list or numpy array back to HAWC2 as
    an input vector. '''
    t, azim = array1[0], array1[1]

    theta    =   [0,0,0]
    theta[0] =   amp*cos(azim + 0.174)
    theta[1] =   amp*cos(azim + 0.174 - 2/3*pi)
    theta[2] =   amp*cos(azim + 0.174 - 4/3*pi)

    return theta



if __name__ == '__main__':
    main()
