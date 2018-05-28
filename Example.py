"""
Institution : DTU
Course      : Master Thesis Project
Date        : 20-Jan-2018
Author      : Jaime Liew - S141777
Email       : Jaimeliew1@gmail.com
Description : Example script for HAWC2_TCP link. Adds a sinusoidal pitch angle 
demand to each blade.
"""

from HAWC2_TCP import HAWC2_TCP
import numpy as np
import threading
import os

htc_filename = 'htc/TCPExample.htc'
iterations = int(100/0.025) # simulation time/sample time


#Kill already running instances of HAWC2
os.system('taskkill /f /im hawc2mb.exe')

# Run HAWC2 simulation by starting another thread. This is the most straight 
# forward way I could find using python.
os.chdir('DTU10MW_Turbine/')
def Thread_HAWC2_func():
    os.system('hawc2MB.exe ' + htc_filename)  
    
thread_HAWC2 = threading.Thread(target=Thread_HAWC2_func)
thread_HAWC2.start()

# Connect Python to HAWC2 via TCP
HAWC2 = HAWC2_TCP(PORT=1239)

################### Main loop ##########################
for i in range(iterations-1):
    #Get data from HAWC2
    inData  = HAWC2.getMessage(Nkeep=3)
    
    t, azim = inData[0], inData[1]
    print('\r Time elapsed: {:2.2f}s'.format(inData[0]), end='')
    
    theta    =   [0,0,0]
    theta[0] =   0.026*np.cos(azim + 0.174)
    theta[1] =   0.026*np.cos(azim + 0.174- 2/3*np.pi) 
    theta[2] =   0.026*np.cos(azim + 0.174- 4/3*np.pi)

    #Send data to HAWC2
    HAWC2.sendMessage(theta)
    
HAWC2.close()
thread_HAWC2.join()
