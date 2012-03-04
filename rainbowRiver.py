'''
Created on Feb 27, 2012

@author: dlo
'''

from light_matrix import *
import numpy as np
import colorsys
from normalDistributedPixels import *


class RainbowRiver(BluewayPattern):
     '''The Magical Rainbow River!
     
     Effectively a mixer of two patterns:
       - A NormalDistributedPixels pattern flows down the Blueway
       - Periodically a wipe exposes the magical rainbow underneath 
     '''
     
     rainbowRiver = None  #1-row rainbow array down the river
     riverLights = None # a NormalDistributedPixels instance to keep track of the river lights
     
     # River flow params (c.f. riverFlow.py)
     riverOffset = 0 # current offset column of the river, 0.0 to 1.0 (gets *lights.cols)
     riverIncr = 0.0 # how much the river increments each tick
     
     # Rainbow Wipe
     wipeOffset = 1     # current offset column of the river, 0.0 to 1.0 (gets *lights.cols)
     wipeIncr = 0.0  # how much the wipe increments (decrements, technically) by each tick
     wipeWidth = 5
     rainbowWidth = 20
     
     
     def __init__(self, lights, riverLights, 
                  tickPeriodMs, 
                  riverPeriodSec, hueMean = 0.0, hueStdDev = 0.1, satMean = 1.0, satStdDev = 0.1,
                  rainbowPeriodSec = 1, numRainbows=1, wipeWidth = 5, rainbowWidth = 20):
          '''Constructor
          @param lights: Pattern's LightMatrix instance
          @param riverLights: Second LightMatrix for the flowing river
          @param tickPeriodMs: Number of ms in between ticks (tickDelay in bluewayExecutor)
          @param riverPeriodSec: Number of seconds for the river pattern to flow down the Blueway
          '''
          super(RainbowRiver, self).__init__(lights)
          
          self.riverLights = NormalDistributedPixels(riverLights, 10, hueMean, hueStdDev, satMean, satStdDev)
          self.riverLights.alt = False
          
          # flow params
          self.riverIncr = tickPeriodMs / 1000. / riverPeriodSec
          
          # rainbow wipe params
          self.rainbowWidth = rainbowWidth
          self.wipeIncr = tickPeriodMs / 1000. / rainbowPeriodSec
          self.wipeOffset = 1.
          
          # Initialize the rainbow river
          self.rainbowRiver = ones((lights.cols, 3))
          self.rainbowRiver[:,0] = np.linspace(0, numRainbows, lights.cols)
          self.rainbowRiver = np.array(map(lambda hsv: colorsys.hsv_to_rgb(hsv[0] % 1, hsv[1], hsv[2]), self.rainbowRiver))
          
          # Turn it into a lightmatrix data array -- assume 4 rows
          self.rainbowRiver = np.concatenate((self.rainbowRiver, self.rainbowRiver, self.rainbowRiver, self.rainbowRiver), 0)\
                                .reshape(4, lights.cols, 3)
     
     def tick(self):
          # Flow the river.  c.f. RiverFlow.tick()
          #------------------
          self.riverLights.tick()
          riverLM = self.riverLights.lights.data
          riverCols = self.riverLights.lights.cols
          
          off = int(self.riverOffset * riverCols) #int floors the offset
          #print 'flowing the river with offset ', off, '  (riverOffset:', self.riverOffset, '  riverIncr:', self.riverIncr
          
          # Make an array view that starts at offset and then wraps around
          # (ie shift the pixels down)
          riverView = np.concatenate((riverLM[:,off:,:], riverLM[:,:off,:]), 1)
          
          #TODO interpolate
          
          self.riverOffset = (self.riverOffset + self.riverIncr) % 1
          
          
          # Rainbow Wipe
          #------------------
          wipeOff = int(self.wipeOffset * riverCols)
          wipeOffEnd = wipeOff + self.rainbowWidth
          
          wipeOff = min(riverCols, max(0, wipeOff))
          wipeOffEnd = min(riverCols, max(0, wipeOffEnd))
          
          rainbowView = self.rainbowRiver[:, wipeOff:wipeOffEnd, :]
          
          self.wipeOffset -= self.wipeIncr
          if (self.wipeOffset < -float(self.rainbowWidth)/riverCols):
               #print 'resetting wipeOffset to 1. from ', self.wipeOffset
               self.wipeOffset = 1.
          
          
          
          # Create the final lights
          #------------------
          #print 'showing rainbow from ', wipeOff, ' to ', wipeOffEnd, '  (master offset/decrementor: ', self.wipeOffset, self.wipeIncr
          self.lights.data = np.concatenate((riverView[:,:wipeOff,:], rainbowView, riverView[:, wipeOffEnd:,:]), 1)
          
          
          
          
          
          
          
          
          
          
          
     
