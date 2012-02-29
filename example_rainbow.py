#!/usr/bin/env python
# above line for unix only

import optparse, time, sys, colorsys
from display.route_display import *
from numpy import ones, zeros

#CONFIGURATION
#-----------------

# The number of RGB pixels in the strand
numPx = 150/3 # 150 is the number of rgb commands, /3 is the number of "pixels" in each strand

# Data array of pixels x 4 strands
data = ones([numPx*3,4])*1.00

strandRemap = [0,1,3,2]


# UTILITY FUNCTIONS
#--------------------------
def setRGB(px, r, g, b):
     data[px*3    ] = r
     data[px*3 + 1] = g
     data[px*3 + 2] = b

# Set a pixel to a color by HSV
# param px pixel number to set
# param h hue, 0.0 - 1.0
# param s saturation (amount of color), 0.0 (white/grey) - 1.0 (full color)
# param v value (amount of darkness/black), 0.0 (black) - 1.0 (full brightness)
def setHSV(px, h, s, v, strand = -1):
     rgb = colorsys.hsv_to_rgb(h, s, v)

     #correct for strand re-ordering
     strand = strandRemap[strand]
     
     if (strand == -1):
          data[px*3    ] = rgb[0]
          data[px*3 + 1] = rgb[1]
          data[px*3 + 2] = rgb[2]
     else:
          data[px*3    , strand] = rgb[0]
          data[px*3 + 1, strand] = rgb[1]
          data[px*3 + 2, strand] = rgb[2]
     #print 'setting ', px, ' to hsv: ', h, s, v, '   and rgb: ' , rgb


if __name__ == '__main__':
     parser = optparse.OptionParser(usage="%prog [options] incrementor")
     parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
     parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
     (opts, args) = parser.parse_args()
     if len(args) != 1:
          parser.error("incorrect number of arguments")     

     incrementor = int(args[0])
     
     
     i = 0
     while(True):
          for px in range(numPx):
               for strand in range(4):
                    setHSV(px, float((px + i + strand*5) % numPx)/float(numPx), 1, 1, strand)
          route_display(data)
          print 'set range ', i
          time.sleep((opts.delay or 500)/1000.)
          i += 1
          if (i == numPx):
               i=0

     px = opts.start or 0  #opts.start will be "None" if not specified

     print 'done'
     sys.exit(0)


