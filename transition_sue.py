#!/usr/bin/env python
# above line for unix only

# imports 
import optparse, time, sys
from numpy import ones, zeros, array, apply_along_axis,where
from time import sleep

from display.route_display import *

# configuration options for how the display command is routed may be found
# in config/__init__.py  DEFAULT file-based rendering will be deprecated soon

BLACK = [0,0,0]
CYAN = [0,1,1]
MAGENTA = [1,0,1]
YELLOW = [1,1,0]
RED = [1,0,0]
GREEN = [0,1,0]
BLUE = [0,0,1]
WHITE = [1,1,1]

ALL_SIMPLE = ["BLACK","WHITE","CYAN","MAGENTA","YELLOW","RED","GREEN","BLUE"]
def main():
     incr, loopStart, delay = getCommandLineOptions()

     # initialize a display at full white (1.0)
     lights = LightMatrix(0.0) 
     
     # send values to the lights/simulator for a count of 2 seconds
     # to give the browser time to open, etc.
     print "initializing...",
     for i in range(2):
          lights.display()
          sleep(1)
     print "...done init()"
     
     # set up an array to cycle through colors
     colors = [["RED","GREEN"],
               ["GREEN","BLUE"],
               ["BLUE","RED"],
               ["YELLOW","CYAN"],
               ["CYAN","MAGENTA"],
               ["MAGENTA","YELLOW"]]
     edge = 25
     
     for name in ALL_SIMPLE:
          lights.createWindow(name,globals()[name],edge)
     colorIndex = 0
     loopCount = loopStart # default 0

     # loop forever until ctrl-c is pressed
     while 1:
          # loop over all columns of the lights, assigning the new value
        
          loopCount=loopStart #0
          color1, color2 = colors[colorIndex]

          while loopCount < lights.cols+edge: # and loopCount >= loopStart:
               lights.display()
               lights.clear()
               lights.insertWindow(color1,lights.cols-loopCount-1)
               lights.insertWindow(color2,loopCount-edge)
               sleep(delay/1000.) # sleep takes seconds
               loopCount += incr
     
          # After getting up to 50 or down to -1, increment the colorIndex.
          colorIndex += 1
          # The modulo operator "%" says take the remainder of a division, so
          # colorIndex will count: 0,1,2,3,4,0,1,2,3,4 since len(colors) == 5 .
          colorIndex = colorIndex % len(colors)
      
class LightMatrix:
     """ Class for storing data to be sent to lights """

     #eventually take these two from config:
     rows = 4 
     cols = 50
     channels = 3
     windows = {}

     def __init__(self,intensity = 0.0):
          """ create NumPy matrix of rows x 50 x RGB 
              with given intensity (optional, defaults to 0.0 'off')"""
          self.data=ones([self.rows,self.cols,self.channels])*intensity

          self.totalChannels = self.channels*self.cols

     def clear(self):
         """clears screen to left of window"""
         self.data*=0

     def createWindow(self,name,color,width=10):
          """ creates a named window of specified width and color"""
          data=ones([self.rows,width,self.channels])
          data[:,:,:]=color
          self.windows[name]=data

     def insertWindow(self,name,index):
         """inserts window into the display, combines overlapping colors
            by showing the combination i.e. RED+GREEN = YELLOW
            or showing the color in common: CYAN+YELLOW = GREEN """ 

         window=self.windows[name]
         idx1=index
         idx2=index+window.shape[1]

         #make sure idx1 and idx2 fall within bounds
         idx1=min(max(0,idx1),self.data.shape[1])
         idx2=min(max(0,idx2),self.data.shape[1])

         existing = self.data[:,idx1:idx2].view()
         # assumes window is uniform, so doesn't matter where we cut it off
	 new = window[:,0:abs(idx2-idx1)].view()
	 self.data[:,idx1:idx2] = new+existing
         
         maxVal = max(self.data.flatten())
         
         #case where we want just the color(s) in common...
         if maxVal > 1:
	      testOne = lambda(color):any(color==maxVal)
              indices=apply_along_axis(testOne,2,existing)
              existing[indices]-=1

     def changeRow(self,row,color):
          """ pass in which row to change and either:
          a number to set for all channels (R,G,B) in all columns of the row
               e.g: .5 for half-intensity to all 3 color channels across 50 columns
          an RGB array to set for all lights in that row
               e.g. [1,0,0] for red across the row
          an array of RGB values for all lights in the row
                e.g. [[1,0,0],[0,0,1],[1,0,0],[0,0,1], ... ] with 46 more in ...
                to alternate red and blue across all 50 columns in a row"""
          self.data[row,:] = color

     def changeColumn(self, col, color):
          """ pass in which column to change and either:
          a number to set for all channels (R,G,B) in all rows of the column
               e.g: .5 for half-intensity to all 3 color channels down 4 rows
          an RGB array to set for all lights in that row
               e.g. [1,0,0] for red down the column
          an array of RGB values for all lights in the column
                e.g. [[1,0,0],[0,0,1],[1,0,0],[0,0,1]] to alternate red and
                blue down all 4 rows in a column"""
          self.data[:,col] = color
          
     def changePixel(self, row, column, color):
          """ pass in row,column of pixel location and either:
           a number to set for all channels (R,G, and B) of that pixel
           an RGB array that represents the color of that pixel"""
          self.data[row,column] = color

     def display(self):
          # reshaping 4,50,3 to 4,150 and then transposing to get 150,4
          outData=self.data.reshape(self.rows, self.totalChannels).transpose()
          route_display(outData)

def getCommandLineOptions():
     """ interprets and returns script-specific options"""
     parser = optparse.OptionParser(usage="%prog [options] incrementor")
     parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
     parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
     (opts, args) = parser.parse_args()
     if len(args) != 1:
          parser.error("incorrect number of arguments")     
     msDelay = opts.delay or 100 # in milliseconds
     incr = int(args[0])
          
     loopStart = opts.start or 0  #opts.start will be "None" if not specified
     
     return incr, loopStart, msDelay

if __name__ == '__main__':
     main()
