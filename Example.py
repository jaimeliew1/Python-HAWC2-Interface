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
import numpy as np
from numpy import pi, cos


class ExamplePitchSineWave(HAWC2Interface):
    # A class which executes your custom python function.
    def __init__(self, modeldir, amp):
        # If you would like to initialise variables, make sure to call
        # the super __init__ function as follows. Make sure to pass
        # self and the model directory arguments.
        HAWC2Interface.__init__(self, modeldir)
        self.amp = amp


    # This is where the magic happens. This function is called each
    # time step. it receives two arguments: self, and a numpy array of
    # the HAWC2 output. The function then returns a list or numpy array
    # back to HAWC2 as an input vector.
    # Set this function to what you want.
    def update(self, array1):
        t, azim = array1[0], array1[1]

        print('\r Time elapsed: {:2.2f}s'.format(t), end='')

        theta    =   [0,0,0]
        theta[0] =   self.amp*cos(azim + 0.174)
        theta[1] =   self.amp*cos(azim + 0.174 - 2/3*pi)
        theta[2] =   self.amp*cos(azim + 0.174 - 4/3*pi)

        return theta


simTime, sampleTime = 100, 0.01
N_iters = int(simTime/sampleTime)


HAWC2 = ExamplePitchSineWave('DTU10MW_Turbine/', 0.02)
# run the simulation by specifying the htc filepath (relative to the
# model directory) and the number of iterations in the simulation.
HAWC2.run('htc/TCPExample.htc', N_iters)

