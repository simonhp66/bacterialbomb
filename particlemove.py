# -*- coding: utf-8 -*-
"""
Created on Sun May  2 16:16:22 2021

@author: Simon
"""
# This file is imported into the bomb10.py file
# It is used for creating a class of particles
# Various methods are defined to move the particles

import random

# Creating class
class Particle:
    """This class is used to iterate particles as they move"""    
    
    def __init__(self,x,y,z,ws,environment):
        """The particles set up in Bomb.py are identical on creation"""
        self.x = x
        self.y = y
        self.z = z
        self.ws = ws  #Stores windspeed
        self.environment = environment  # Stores digital elevation model
        self.landed = 0  # Switches to 1 when particle has landed
        self.refheight = z # This is the starting "z" 
    
        
    # Method used for printing particle details    
    def __str__(self):
        """Prints the key attributes of each particle, used for testing"""
        return (str("x")+ str(self.x)+
                " y"+str(self.y)+" z"+str(self.z)+ " Elevation "+
                str(self.environment[self.y][self.x]))
    
    
    # Method used for moving particle up or down           
    def zmove(self):
        """Moves the height (or z) of each particle during 1 iteration"""
        # Defines a turbulence factor based on windspeed
        if self.ws > 8:
            turb = 3
        elif self.ws > 5:
            turb = 2
        elif self.ws > 3:
            turb = 1
        else:
            turb = 1
        #print ("Up/down cycle")
        # The up or down movement is amplified by higher turbulence
        if self.z> self.refheight-1:  # Up/down movement occurs above building
            #print("Above")
            rh = random.randint(0,9)  # Used for probability of up/down 
            #print ("rh= ",rh)
            if rh < 2:
                self.z += (1*turb)  # 20% chance going up 
                #print("Up",self.z)
            elif rh > 2:
                self.z -= (1*turb)  # 70% chance going down
                #print("Down",self.z)
            # if rh equals 2 there no change - 10% chance it stays same level
        else:  # Turbulence assumed not to apply at 75m and below
            if self.landed == 0: #This switches to 1 when the particle lands 
                self.z -= 1
                #print("Down", self.z)
            #else:
                #print("Landed", self.z)
    
    
    # Method used to assess whether the particle has landed    
    def landing(self):
        """Assesses whether the particle has landed or not on each iteration"""
        if self.refheight == 76:  # True where flat plain is selected in GUI
            if self.z ==0:  # When z is zero it has landed
                #print("Landed, coordinates fixed")
                #print("x ", self.x, "y ", self.y, "Height", self.z)
                #print("Elevation", self.environment[self.y][self.x])
                self.landed = 1  # Switches to landed so coordinates are fixed
        else: # Will be the case if DEM selected in GUI
            if self.z <= self.environment[self.y][self.x]:  # < Elevation
                self.z = self.environment[self.y][self.x]
                self.landed = 1  # Switches to landed to prevent further mvt.
            #print("Landed, coordinates fixed")
            #print("x ", self.x, "y ", self.y, "Height", self.z)
            #print("Elevation", self.environment[self.y][self.x])
     
        
    # Method used to change the x and y coordinates until particle lands
    # Windpseed selected in GUI can amplify movement Eastwards     
    def xymove(self):
        """Moves the particle x and y coordinates on each iteration"""
        #print("XY Coordinate cycle)
        if self.landed == 1:
            #print("Landed, no xy move")
            self.x = self.x
        else:
            if self.ws > 6:  # Easterly movement multiplied at higher windspeed
                multiple = 2 
            else:
                multiple = 1                  
            rm = random.randint(0,19)
            #print ("rm =", rm)
            if rm == 0:
                self.x -= 1  # 5% chance of Westerly movement
            elif rm < 3:
                self.y += 1  # 10% chance of Northerly movement
            elif rm < 5:
                self.y -= 1  # 10% chance of Southerly movement
            else:
                self.x += (1*multiple) # High winds Easterly movement amplified   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            