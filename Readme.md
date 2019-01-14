Python-HAWC2 Interface
======================

Python-HAWC2 Interface allows your own Python function to be executed in HAWC2
simulations in real time. This repository contains the Pythonic wrapper module
named HAWC2_TCP, as well as a simple working example.

 

Installation
============

This repository is written for Windows.

[HAWC2 ](http://www.hawc2.dk/)should be installed and the executable HAWC2mb.exe
should either be in the PATH directory, or in the same folder as the python working directory.

TCPServer.dll should be placed in the control folder of the turbine model
directory. The DLL is available on the [HAWC2
website](http://www.hawc2.dk/download/dlls) in the MATLAB control download zip
file. It is also provided in this repository.

To install this package, clone the repository and pip install:

```
git clone https://github.com/jaimeliew1/Python-HAWC2-Interface.git
cd Python-HAWC2-Interface
pip install .
```

Example
=======

example.py provides a working example of the Python-HAWC2 Interface using the
[DTU10MW Reference Wind Turbine
Model](http://www.hawc2.dk/Download/HAWC2-Model/DTU-10-MW-Reference-Wind-Turbine).
The example script sends a sinusoidal pitch signal to all three blades.
