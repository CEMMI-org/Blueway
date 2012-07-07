#!/usr/bin/env python
# above line for unix only

# imports 
import optparse, time, sys
from numpy import ones, zeros, array, arange, linspace, pi, sin, trunc
from time import sleep

import util.TimeOps as timeops
from display.route_display import *

# configuration options for how the display command is routed may be found
# in config/__init__.py  DEFAULT file-based rendering will be deprecated soon


def main():
     incr, loopStart, delay, totalTime = getCommandLineOptions()
     stopwatch = timeops.Stopwatch()
     stopwatch.start()

     scrollLen = 101
     numWaves = 8
     
     lights = LightMatrix() 
     lights.display()

     wavespace = linspace(0, numWaves*2*pi, scrollLen)
     wavespace = sin(wavespace)
     #print trunc(wavespace * 100)
     #print wavespace.size
     scrollspace = arange(scrollLen)
     #print scrollspace

     
     while ((not totalTime) or stopwatch.elapsed() / 1000 < totalTime):
          #if (stopwatch.elapsed() < 2000):
          #      brightness = stopwatch.elapsed() / 2000
          lights.changeRow(0, [0,1,0])
          lights.changeRow(1, [0,1,0])
          lights.changeRow(2, [0,1,0])
          lights.changeRow(3, [0,1,0])
          lights.display()
          sleep(1/10.)

          for scrollStart in scrollspace:
               if ((totalTime) and stopwatch.elapsed() / 1000 >= totalTime):
                    return 
               scrollPos = scrollStart
               for i in range(lights.cols):
                    if scrollPos >= scrollLen:
                         scrollPos = 0
                    #print scrollPos
                    #print trunc(wavespace[scrollPos] * 100)
                    if wavespace[scrollPos] >= 0:
                         lights.changePixel(0, i, [0, 1.0-wavespace[scrollPos], 0])
                         lights.changePixel(1, i, [0, 1.0-wavespace[scrollPos], 0])
                         lights.changePixel(2, i, [0, 1.0-wavespace[scrollPos], 0])
                         lights.changePixel(3, i, [0, 1.0-wavespace[scrollPos], 0])
                    else:
                         lights.changePixel(0, i, [0.0-wavespace[scrollPos], 1, 0.0-wavespace[scrollPos]])
                         lights.changePixel(1, i, [0.0-wavespace[scrollPos], 1, 0.0-wavespace[scrollPos]])
                         lights.changePixel(2, i, [0.0-wavespace[scrollPos], 1, 0.0-wavespace[scrollPos]])
                         lights.changePixel(3, i, [0.0-wavespace[scrollPos], 1, 0.0-wavespace[scrollPos]])
                    lights.display()
                    scrollPos += 1
                    #sleep(delay/1000.) # sleep takes seconds
             

                         


class LightMatrix:
     """ Class for storing data to be sent to lights """

     #eventually take these two from config:
     rows = 4 
     cols = 50
     channels = 3

     def __init__(self,intensity = 0.0):
          """ create NumPy matrix of rows x 50 x RGB 
              with given intensity (optional, defaults to 0.0 'off')"""
          self.data=ones([self.rows,self.cols,self.channels])*intensity

          self.totalChannels = self.channels*self.cols

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
     parser.add_option("--time", action="store", type="int", help="number of seconds to run")
     (opts, args) = parser.parse_args()
     msDelay = opts.delay or 100 # in milliseconds
     incr = int(args[0])
     time = opts.time or None      
     loopStart = opts.start or 0  #opts.start will be "None" if not specified
     
     return incr, loopStart, msDelay, time

if __name__ == '__main__':
     main()
