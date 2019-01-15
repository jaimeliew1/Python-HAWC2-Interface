"""
Institution : DTU
Course      : Master Thesis Project
Date        : 20-Jan-2018
Author      : Jaime Liew - S141777
Email       : Jaimeliew1@gmail.com
Description : A Python wrapper class for interfacing HAWC2 simulations via TCP.
              The HAWC2 simulation requires a TCP DLL.
"""

import os, socket, time, threading
import numpy as np
import click



class HAWC2Interface(object):
    def __init__(self, hawc2_command, update_func, modeldir='./', port=1239):
        self.hawc2_command = hawc2_command
        self.update_func   = update_func
        self.modeldir      = modeldir
        self.port          = port


    def update(self, array1, **kwargs):
        return self.update_func(array1, **kwargs)



    def run(self, htc_filename, N_iter, kill=True, progressbar=True, **kwargs):
        if kill:
            os.system('taskkill /f /im {}'.format(self.hawc2_command))

        # change directory to wind turbine model directory.
        cwd = os.getcwd()
        os.chdir(self.modeldir)

        # Run HAWC2 simulation by starting another thread.
        def Thread_HAWC2_func():
            os.system('{} {}'.format(self.hawc2_command, htc_filename))
        thread_HAWC2 = threading.Thread(target=Thread_HAWC2_func)
        thread_HAWC2.start()

        # Connect Python to HAWC2 via TCP
        HAWC2 = HAWC2_TCP(PORT=self.port)

        # main iteration loop
        if progressbar:
            with click.progressbar(range(N_iter-1), label=htc_filename) as bar:
                for i in bar:
                    inData  = HAWC2.getMessage()
                    outData = self.update(inData, **kwargs)
                    HAWC2.sendMessage(outData)
        else:
            for i in range(N_iter-1):
                inData  = HAWC2.getMessage()
                outData = self.update(inData, **kwargs)
                HAWC2.sendMessage(outData)
        HAWC2.close()
        thread_HAWC2.join()

        os.chdir(cwd)





class HAWC2_TCP(object):
    def __init__(self, PORT=None, TCP_IP='127.0.0.1',connectAttempts=20):
        #Makes a TCP CLIENT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if PORT is not None:
            #Make TCP connection if a port number is provided.
            self.connect(PORT, TCP_IP, connectAttempts)

    def connect(self, PORT, TCP_IP='127.0.0.1', connectAttempts=20, printStatus=True):
        #If no port number is provided in object initiation, this function can
        #be used to connect to a port.
        #Attempts to connect to HAWC2 connectAttempts many times before raising
        #a ConnectionRefusedError.
        #prints connection status to console if printStatus is True.
        Connected = False
        Attempts = 0
        while not Connected:
            if Attempts >= connectAttempts:
                raise ConnectionRefusedError('Cannot connect to HAWC2.')
                break
            try:
                self.socket.connect((TCP_IP, PORT))
                Connected = True
                if printStatus:
                    print('HAWC2 Connected.')
            except ConnectionRefusedError:
                Attempts += 1
                if printStatus:
                    print('HAWC2 Not ready. Try again...')
                time.sleep(1)


    def getMessage(self, Nkeep=10, keys=None, BUFFER_SIZE=1024):
        #Waits until a message is received from HAWC2, and returns the message
        #in a numpy array. Keeps the first Nkeep elements. if Nkeep is not
        #provided, all elements are returned.
        #If a list of keys is provided, returns the data in a dictionary instead
        #of an numpy.ndarray.

        #!!! ConnectionResetError
        message = self.socket.recv(BUFFER_SIZE)
        data = message.decode('utf-8')
        if Nkeep is not None:
            data = np.array([float(x) for x in data.split(';')[1:Nkeep+1]])
        else:
            data = np.array([float(x) for x in data.split(';')[1:]])

        if keys is not None:
            assert len(keys) == Nkeep
            data = dict(zip(keys,data))

        return data

    def sendMessage(self, message):
        #Encodes and sends a message to HAWC2. message should be either a list
        #or a numpy array.
        out = ''.join(['{:2.8f};'.format(x) for x in message]) + '*'
        out = out.encode('utf-8')
        self.socket.send(out)

    def close(self):
        self.socket.close()
