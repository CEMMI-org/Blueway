#!/usr/bin/env python
# above line for unix only

# imports 
import optparse, time, sys, colorsys
from numpy import *
from time import sleep

import util.TimeOps as timeops
from display.route_display import *

# configuration options for how the display command is routed may be found
# in config/__init__.py  DEFAULT file-based rendering will be deprecated soon

OFF = [0,0,0]
CYAN = [0,1,1]
MAGENTA = [1,0,1]
YELLOW = [1,1,0]
ON = [1,1,1]

def main():
     incr, loopStart, delay, totalTime = getCommandLineOptions()
     stopwatch = timeops.Stopwatch()
     stopwatch.start()

     # initialize a display at full white (1.0)
     lights = LightMatrix(1.0) 
     
     # send values to the lights/simulator for a count of 2 seconds
     # to give the browser time to open, etc.
     print "initializing...",
     for i in range(2):
          lights.display()
          sleep(1)
     print "...done init()"
     
     # set up an array to cycle through colors
     colors = [CYAN, MAGENTA, YELLOW, OFF, ON]
     colorIndex = 0

     loopCount = loopStart # default 0
     
     xc = 25;
     pixelSize = 50
     timeDisplacement = 1     
     calculation1 = math.sin( math.radians(timeDisplacement * 0.61655617))
     calculation2 = math.sin( math.radians(timeDisplacement * -3.6352262))
     # loop forever until ctrl-c is pressed
  
     while ((not totalTime) or stopwatch.elapsed() / 1000 < totalTime):
          #if (stopwatch.elapsed() < 2000):
          #      brightness = stopwatch.elapsed() / 2000

          for x in range(0,lights.rows) : #for (int x = 0; x < pg.width; x++, xc += pixelSize) :
              xc = xc + pixelSize
              yc = 25
              s1 = 128 + 128 * math.sin(math.radians(xc) * calculation1 )
              for y in range(0,lights.cols) : #for (int y = 0; y < pg.height; y++, yc += pixelSize) :
                  yc = yc + pixelSize
                  s2 = 128 + 128 * math.sin(math.radians(yc) * calculation2 )
                  s3 = 128 + 128 * math.sin(math.radians((xc + yc + timeDisplacement * 5.0) / 2.00))
                  s  = (s1+ s2 + s3) / 3.0
                  lights.display()
                  #print s
                  color = [s, 255 - (s / 2.0), 255]
                  #print color
                  color[0]= color[0]/255.00
                  color[1]= color[1]/255.00
                  color[2]= color[2]/255.00
                  #print color
                  color = colorsys.hsv_to_rgb(color[0], color[1], float(color[2]))
                  #lights.convertToRGB(color)
                  #print color
                  lights.changePixel(x, y, color)
                  
                  
                
              
class LightMatrix:
     """ Class for storing data to be sent to lights """

     #eventually take these two from config:
     rows = 4 
     cols = 50
     channels = 3
     rgbColor = [0,0,0]
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
          """ pa ss in which column to change and either:
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
     
     def tryAppend(self, x, y, step, ratio, pixArray):
          if x<=5 and x>=0 and y<=49 and y>=0 : # && self.data[x,y]==[0,0,0] || self.data[x,y]== [1,1,1] ):
              pixArray.append([x,y,step,ratio])
     
     def fade(self, x , y):
          pix = []
          pix.append([x,y,0,0])
          steps =500
          spread =100
          for step in range(steps):
              #ratio = 0
              #ratio2 = 0
              for idx, fixture in enumerate(pix):
                  pix[idx][3] += (step-pix[idx][2]) % steps / float(steps)
                  tmpPix = pix
                  if step>0 and step%100==0 and step<400 :
                      #print step
                      x2=pix[idx][0]
                      y2=pix[idx][1]
                      self.tryAppend(x2+1,y2+1,step,0,tmpPix)
                      self.tryAppend(x2-1,y2-1,step,0,tmpPix)
                      self.tryAppend(x2+1,y2-1,step,0,tmpPix)
                      self.tryAppend(x2-1,y2+1,step,0,tmpPix)
                      self.tryAppend(x2,y2+1,step,0,tmpPix)
                      self.tryAppend(x2+1,y2,step,0,tmpPix)
                      self.tryAppend(x2-1,y2,step,0,tmpPix)
                      self.tryAppend(x2,y2-1,step,0,tmpPix)
                  #print pix
                  self.changePixel(pix[idx][0], pix[idx][1], colorsys.hsv_to_rgb(pix[idx][3], 1.0, 1-pow(pix[idx][3],5)))
                  #if step>25:
                   #   ratio2 += (step-25) % steps / float(steps)
                    #  self.changePixel(pix[0][0], pix[0][1]+1, colorsys.hsv_to_rgb(ratio2, 1.0, 1-pow(ratio2,5)))
                     # self.changePixel(pix[0][0], pix[0][1]-1, colorsys.hsv_to_rgb(ratio2, 1.0, 1-pow(ratio2,5)))
              self.display()
            
          sleep(1)
    
          
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
     if len(args) != 1:
          parser.error("incorrect number of arguments")     
     msDelay = opts.delay or 100 # in milliseconds
     incr = int(args[0])
     time = opts.time or None
     loopStart = opts.start or 0  #opts.start will be "None" if not specified
     
     return incr, loopStart, msDelay, time

if __name__ == '__main__':
     main()
