'''
Pattern to wipe a white fading line down the Blueway

More of an experiment to figure out the matrix indexing required to animate patterns 
"downstream" and wrap around to the other end of the blueway.

Created on Feb 26, 2012

@author: dlo
'''
from light_matrix import *
import numpy as np


class RiverWipe(BluewayPattern):

     riverPattern = None
     curOffset = 0
     offsetIncrementor = 1
     interpolate = True

     def __init__(self, lightMatrix, ticksPerTween, hue=.667, whiteWidth = 5):
          '''
          Constructor
          @param lightMatrix: lights
          @param ticksPerTween: how many ticks to do one flow down the river
          @param whiteWidth: width, in pixels, of the white fade line
          '''
          super(RiverWipe, self).__init__(lightMatrix)
          
          # perform one movement of the river per tween
          self.offsetIncrementor = 1. / ticksPerTween 
          
          self.riverPattern = ones((self.lights.cols, 3))
          self.riverPattern[:, 0] = hue # set hue as the same down the line
          self.riverPattern[:whiteWidth, 1] = np.linspace(0, 1, whiteWidth) #fade from white over first few pixels
          
     def tick(self):
          off = int(self.curOffset * self.lights.cols)
          
          # Make an array view that starts at offset and then wraps around
          # (ie shift the pixels down)
          riverView = np.concatenate((self.riverPattern[off:,:], self.riverPattern[:off,:]), 0)
          
          if (self.interpolate):
               i = 0
               pos = (self.curOffset * self.lights.cols) % 1
               interpolated = ones(riverView.shape)
               riverViewFirst = riverView[0]
               while i < len(riverView) - 1:
                    interpolated[i] = colorTweenHSV(riverView[i], riverView[i+1], pos)
                    i += 1
               interpolated[i] = colorTweenHSV(riverView[i], riverViewFirst, pos)
               riverView = interpolated
          
          # Transform hsv to RGB
          riverView = np.array(map(lambda hsv: colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]), riverView))
          
          # Use the river view as the RGB row definition for each row.
          self.lights.data = np.concatenate((riverView, riverView, riverView, riverView), 0)\
                               .reshape((self.lights.rows, self.lights.cols, 3))
           
          # increment the row and wrap around
          self.curOffset = (self.curOffset + self.offsetIncrementor) % 1
          
          
        