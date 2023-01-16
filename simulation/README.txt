To simulate the time course of binocular rivalry in Matlab:

>> run_once

Adjust type of noise with NoiseSwitch. Other noise and simulation parameters can be adjusted at the top of the script. The simulation will produce a plot unless PlotSwitch is set to 0. 


--------------------------


To simulate a complete diagram with two parameters varying (contrast, noise intensity or temporal correlation):

>> run_diagram

This simulation will output a .mat file with 8 matrices, 2 for each metric. The simulation will take some time.


--------------------------


To change the type of adaptation, edit the system differential equations in evolDriveFiringAdap.