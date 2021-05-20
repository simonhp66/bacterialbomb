# -*- coding: utf-8 -*-
"""
Created on Sun May  2 10:11:50 2021

@author: Simon
"""

# Imports
import matplotlib.pyplot
import csv
from bs4 import BeautifulSoup
import requests
import particlemove # Associated file used to move particles
import tkinter as tk
import time


# Model variables
num_of_iterations = 200  # This no. allows all particles to land in high wind
num_of_particles = 0  # This creates the object it is updated in the GUI
wind_speed = 0  # This is updated in the GUI 


# Creating lists
particles = [] #Used to hold particle data
citydata = [] #Used to hold bombsite and then particle landing position data
environment = [] #Used to hold a digital elevation model

# Start a timer to time the code
start = time.time() #Used for measuring how long it takes at the end

# Setting up GUI, this part of the code runs before main() at the bottom
# The overall strucutre and some elements of the GUI were developed based 
# on tutorials under the name The New Boston found on You Tube (see references)

# This is the routine that runs when the user clicks the run button
def routine():
    """The function called by pressing Run in the GUI, collects user inputs"""
    global num_of_particles  # Used in other functions so made global
    num_of_particles = int(my_entry.get())
    print("The number of particles is", num_of_particles)
    global wind_speed  
    wind_speed = int(scale_widget.get())
    print("The wind speed is ", wind_speed)
    global topography  # Used to select the type of surface or basemap
    topography = str(listbox_widget.get(tk.ANCHOR))
    print("The model uses a", topography)
 
# The functions below print help instructions when selected    
def particlehelp():
    """Prints some help relating to particle numbers when requested in GUI"""
    print("HELP")
    print("The number of particles chosen will influence the speed")
    print("5000 particles will typically take about 5 seconds")
    print("If you are interested in rare events where particles land far from")
    print("the main landing area then you may want to use more particles")
       
def windspeedhelp():
    """Prints some help relating to windspeed when requested in the GUI"""
    print("HELP")
    print("The higher windspeed causes more turbulence")
    print("Resulting in particles being more dispersed")
    print("The wind direction is fixed as Easterly")
    print("In strong wind (above 6) the particles are blown further East")

def surfacehelp():
    """Prints some help relating to the surface choice when requested in GUI"""
    print("HELP")
    print("The basic model assumes a uniform flat surface or flat plain")
    print("The digital elevation model uses a contoured surface")
    print("The contoured surface used slopes down in an Easterly direction")
    print("This means that particles travel further using the DEM")    
        
# Set up the GUI window and size    
root = tk.Tk()
root.geometry("500x300")
root.title("Bacterial Bomb") #Add a title to the GUI window  

# Add a menu with help function
# Source: https://www.youtube.com/watch?v=PSm-tq5M-Dc
menu1 = tk.Menu(root)
root.config(menu=menu1)
subMenu = tk.Menu(menu1)
menu1.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="Particle choice", command=particlehelp)
subMenu.add_command(label="Windspeed", command=windspeedhelp)
subMenu.add_command(label= "Surface", command=surfacehelp)

# Add a button used for running the program, routine run when button clicked 
button1 = tk.Button(root, text ="Run", command=routine)
button1.grid(row=6, column=0)

# Add a label above the entry box
label2 = tk.Label(root, text="Enter number of particles: 5000 recommended")
label2.grid(row=2, column=4, padx=5, pady=5)

# Add an entry box used for number of particles
my_entry = tk.Entry(root, width=15)
my_entry.grid(row=3, column=4)

# Add a label above the scale widget
label3 = tk.Label(root, text="Enter wind speed (beaufort scale)")
label3.grid(row=4, column=4)

# Add a scale widget for windspeed
# Source: dummies.com/programming/python/using-tkinter-widgets-in-python/
scale_widget = tk.Scale(root, from_=0, to=12, orient=tk.HORIZONTAL)
scale_widget.set(4)
scale_widget.grid(row=5, column=4)

# Add a label above the scale widget
label4 = tk.Label(root, text="Enter the type of surface")
label4.grid(row=7, column=4)

# Add a drop down box for choosing the type of surface
listbox_entries = ["Flat plain", "Digital elevation model"]
listbox_widget = tk.Listbox(root, height=2, width=25)
for entry in listbox_entries:
    listbox_widget.insert(tk.END, entry)
listbox_widget.grid(row=8, column=4, padx=5, pady=5)

textbox = tk.Text(root,height=4, width=20, padx=5,
                  pady=5, font=("Helvetica",10))
textbox.insert(
    tk.END,"INSTRUCTIONS\nChoose parameters\nPress Run\nClose this window\n")
textbox.grid(row=0, column=0, padx=5, pady=5)


root.mainloop()# GUI window keeps running until it is closed 

# The following functions are all called in main at the bottom. They are listed
# in order that they are called.


# Scraping data from the web to identify bomb location (need to be online)
# Website address line is too long but could not make it work splitting it up
def getdata():
    """Scrapes file with the bomb site from the web and saves it as citydata"""
    city = []
    url ="http://www.geog.leeds.ac.uk/courses/computing/study/core-python-odl2/assessment2/wind.raster"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    city = soup.find_all("p")
# Save beautiful soup resultset as text file to access the individual numbers
# Saving to a file then reading that file seems rather inefficent
# Need to find a better way to access the data using BeautifulSoup
    with open('city.txt', 'w') as testfile:
        for row in city:
            testfile.write(' '.join([str(a) for a in row]) + '\n')

# This code opens the text file and defines the reader, the new line separator
# in the dataset, and the format of the data with one decimal place.
# Code mainly copied from agent based model work. 
    f = []
    f = open('city.txt', newline='\n')
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: #Fill the list with 2D data row by row
        citydata.append(row)
    del citydata[300]  # Deletes a fragment of html syntax
    f.close() 
    #print(citydata[0]) #Testing prints
    #print(len(citydata))#Expecting 300 items, but gives 301
    #print(citydata[300]) #Check what is the last item to make 301
    #del citydata[300] #Deletes a fragment of html syntax
    #print(len(citydata)) #We now have a list with data for a 300x300 frame

# This code reads an environment data file to use as a DEM basemap.
# Then, if chosen, instead of landing on flat surface particles land on a DEM.
# This code is copied from agent based model work.
def getenvironment():
    """Reads a file with a contoured surface and saves it as environment"""
    file = []
    file = open('in.txt', newline='')
    reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:  # Fill the list with 2D data row by row
        environment.append(row)
    file.close() 
# Find height of land at bomb site
# Particle assumed to be released from height of building + height of land 
    #print(environment[150][50]) # Land is 200m at bomb site


# Plot the data for intial exploration
#matplotlib.pyplot.imshow(citydata)
#matplotlib.pyplot.axis([0,299,0,299])
#matplotlib.pyplot.show() # Appears to be data around x50 y150


# This code identifies the bomb site 
def findbomb():
    """Indentifies the x and y coordinates of the bomb site"""
    for i in range (len(citydata)):
        for j in range (len(citydata[i])):
            if citydata[i][j]>0:
                #print(citydata[i][j])
                global xb
                global yb
                xb = j  # The coordinates of the bomb                
                yb = i 
                
# So now we know that there is a single bombsite at location x50,y150.
# It is marked by the number 255, whilst all other cells have zero


# This function creates particles used in function below
# Assume a human stands on the building to release particles 1m above roof
# If "Flat plain" is selected particle height is 75m plus 1m = 76m
# If "DEM" is selected particle height is 200m + 76m = 276m  
def createparticles():
    """Creates the number of particles specified in the GUI"""
    if topography == "Digital elevation model": #Selected in GUI
        z = 276 # The elevation in the DEM at the bomb site is 200m
    else:
        z = 76  
    
    for i in range(num_of_particles):
        x = xb
        y = yb
        ws = wind_speed
        particles.append(particlemove.Particle (x, y, z, ws, environment))
        #print(particles[i])  # Used for testing
        #print(particles[0].x)


# This function iterates the particles through methods in particlemove.py
def iterateparticles():
    """Iterates particles through the move methods in particlemove.py"""
    for j in range(num_of_iterations):
        #print("Iteration")
        for i in range(num_of_particles):
            #print("Particle moving") 
            particles[i].zmove()  # Moves particles up or down
            particles[i].landing()  # Considers if the particle has landed
            particles[i].xymove()  # Moves particles x or y coordinates

        #for i in range(num_of_particles):
            #print(particles[i])


# Plot the data as a density map.
# Firstly record the number of particles in each cell of citydata
# Increment the citydata file for each particle landing
# Then plot this data as a density map
# Two mapping options based on Flat plain or DEM selection
def plotdata():
    """Records coordinates of each landing particle and plots a density map""" 
    #print("Plotting data")
    for i in range(num_of_particles):
        citydata[particles[i].y][particles[i].x] += 1  # Increment per particle 
    citydata[150][50] -= 255 #Set bomb site data to zero
    
    #for i in range(len(citydata)):
        #for j in range(len(citydata[i])):
            #if citydata[i][j]>60: #Used to examine the upper range of data
                #print("x ",i,"y ",j,"number ", citydata[i][j])

# If the user has chosen a Flat plain in the GUI the topography = Flat plain
    if topography == "Flat plain":
        #print("Flat plain")    
        # Vary the max in line below to see broad range or high central points
        matplotlib.pyplot.imshow(citydata, vmin=0,vmax=40)
        matplotlib.pyplot.colorbar(label="Particles")
        matplotlib.pyplot.title("Map showing distribution of particles",
                                fontdict=None, loc=None, pad = None, y = None)
        matplotlib.pyplot.text(45, 80, s="X marks the bomb site", fontsize=7)
        matplotlib.pyplot.text(
            45, 76,s="White dots mark cells where single particles landed",
            fontsize=7)
        matplotlib.pyplot.axis([45, 200, 100, 200])
        matplotlib.pyplot.scatter(50, 150, marker="x", linewidth=3, c="w")
        # Lines below add white dots where there is a single particle
        for i in range(len(citydata)):
            for j in range(len(citydata[i])):
                if citydata[i][j] == 1:
                    matplotlib.pyplot.scatter(j, i, s=0.3, c="w")
        matplotlib.pyplot.show()
            
    else: #If DEM has been chosen
        #print("Digital elevation model")
        matplotlib.pyplot.contourf(environment)
        matplotlib.pyplot.colorbar(label="Elevation")
        matplotlib.pyplot.title(
            "Map showing distribution of particles",
            fontdict=None, loc=None, pad=None, y=None)
        # Next two lines are too long, splitting them mad the plot look poor
        matplotlib.pyplot.text(45, 66, s="X marks the bomb site, White dots mark cells where single particles landed",fontsize=7)
        matplotlib.pyplot.text(45, 62, s="Pink dots mark cells where 2 to 15 particles landed, Red dots mark cells where more than 15 landed",            fontsize=7)
        matplotlib.pyplot.axis([45, 300, 80, 220])
        matplotlib.pyplot.scatter(50, 150, marker="x", linewidth=3, c="w")
        # Code below creates a scatter plot showing different intensities
        for i in range(len(citydata)):
            for j in range(len(citydata[i])):
                if citydata[i][j] > 15:
                    matplotlib.pyplot.scatter(j, i, s=0.3, c="r")
                elif citydata[i][j] > 1 <16:
                    matplotlib.pyplot.scatter(j, i, s=0.3, c="tab:pink")
                elif citydata[i][j] == 1:
                    matplotlib.pyplot.scatter(j, i, s=0.3, c="w")
        matplotlib.pyplot.show()


# Save the density map to a text file (Need to eliminate decimal place)
def savedata():
    """Saves the landed particle coordinates into a text file, citydata.txt"""
    with open('citydata.txt', 'w') as testfile:
        for row in citydata:
            testfile.write(' '.join([str(a) for a in row]) + '\n')


# This is the main function that organises and calls the other functions
def main():
    """Runs the main functions and times the code"""
    mainstart = time.time()  #For timing the main program
    getdata()
    findbomb()
    getenvironment()
    createparticles()
    iterateparticles()
    plotdata()
    savedata()
    mainend = time.time()
    time_elapsed = mainend-mainstart
    print("TIMING")
    print ("Time elapsed", "%.4f" % time_elapsed,"seconds")
    print("End, file saved to citydata.txt")
        
main()
