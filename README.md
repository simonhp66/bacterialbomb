# bacterialbomb

Assignment 2 for University of Leeds coding course 5003M

## Project description

This is a coding project with the objective of mapping where particles may land from a fictitious bacterial bomb released in an urban environment.

The bomb is exploded on top of a 75m building and then particles move in three dimensions before eventually landing on the ground. 

The project has the following steps

1. Scraping the data file with the bomb location from the web
2. Identifying the bomb site
3. Modelling the particle movements for 5000 particles
4. Recording where the particles land
5. Producing a density map to show where the particles land
6. Saving the particle landing data to a text file

## Installation and usage

The package is made up of two python files. The main file is called bacterialbomb.py and there is an associated file called particlemove.py.

The model runs best at the command line. You will need to be connected to the web (for scraping the data). There is a GUI with instructions.

There are three options in the GUI. You can choose the number of particles. You can select the windspeed and you can select the surface that the particles land on (either a flat plain or a contoured surface). There is a Help drop down list concerning these three options.

The model doesn't run well in Spyder due to the GUI and the plots. If you wish to try this the Tools/Prefences/Ipython console/Graphics needs to be set to TKinter. 

## Jupyter Notebook

There is an associated Jupyter Notebook which explains how the code was developed, explains some of the challenges and describes each block of code. It also includes some information on testing and timing. It examines some of the ouput from the code. 

## Inputs and Outputs

The user defined inputs are number of particles, windspeed and surface. These are selected in the GUI.
The code scrapes a file called wind raster containing the bombsite from the web. 
The code also takes in an associated file called in.txt which contains the digital elevation model. There is a copy of this file in the repo.

The outputs are a density map showing where the particles land and this data is saved into a text file called citydata.txt.

## Sources and references

There is a separate word document with a source list and references.
There are also some comments in the code relating to sources.

## Licence

There is a Harvard style licence for this code within the repositary.
