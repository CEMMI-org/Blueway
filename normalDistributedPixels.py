#!/usr/bin/env python
# above line for unix only

import numpy as np
import colorsys
from light_matrix import *
from numpy.core.fromnumeric import reshape

class NormalDistributedPixels(BluewayPattern):
     '''
     LightMatrix pattern that sets each pixel's color to be normally-distributed from a 
     certain hue.  Pattern tweens from one normal distribution to the next
     
     @author: DLopuch
     '''
     
     #List of HSV tuples with same length as lights has pixels.  Acts as beginning of tween.  
     # Each pixel is a randomized hue as per distribution params  
     beginHSVs = None
     
     #List of HSV tuples. Same as above, but end of tween/beginHSVs of next cycle
     endHSVs = None
     
     #color distribution params
     hueMean = 0.0
     hueStdDev = 0.1
     satMean = 0.0
     satStdDev = 0.1
     
     #tweening parameters     
     currentPos = 0.0 #current tween position
     posIncr = 0.1
     
     
     alt = True
     altState = True


     def __init__(self, lightMatrix, ticksPerTween=10., 
                  hueMean = 0.0, hueStdDev = 0.1,
                  satMean = 1.0, satStdDev = 0.1):
          '''
          Constructor
          @param lightMatrix: LightMatrix instance wired up to a route_display, will be changed by this class
                    Note: This code assumes LightMatrix has exactly 3 channels -- ie RGB.
          @param ticksPerTween: how many ticks it takes to perform one tween
          @param hueMean: number between 0 and 1 to act as the mean pixel color
          @param hueStdDev: standard deviation for the hue, 
                    i.e. 68% pixels will be mean +/- 1 std dev of the hue, 95% within 2 std dev's, etc.
                    Note that hue wraps around -- i.e. if mean hue is 0.0 and std. dev is 0.1, 95% of t
                    pixel hues will be a normal distribution from 0.8-1, 0-.2 
          '''
          
          super(NormalDistributedPixels, self).__init__(lightMatrix)
          
          self.hueMean = float(hueMean)
          self.hueStdDev = float(hueStdDev)
          self.satMean = float(satMean)
          self.satStdDev = float(satStdDev)
          
          self.posIncr = 1. / abs(ticksPerTween)  #make sure it's positive
          
          
          self.beginHSVs = self.__generateRandomHSV()
          self.endHSVs = self.__generateRandomHSV() 
          
          
     def tick(self):
          
          #Okay, mouthful here...
          # 1: Concatenate beginHSV and endHSV lists from 2 nx3 lists to 1 nx6 list
          # 2: For each of the HSV tuples, map it through the color tween
          #    (the concatenation was so we could feed both begin and end as one parameter to the lambda)
          # 3: Turn that into a new numpy array, and then send it to the lights setter
          self.__setDMToHSVMatrix(np.array(map(lambda x: colorTweenHSV(x[0:3], x[3:6], self.currentPos),
                                               np.concatenate((self.beginHSVs, self.endHSVs), axis=1))))
          
          self.currentPos += self.posIncr
          
          if (self.currentPos >= 1.0):
               
               #alternate every other to flat hue if alternating
               self.altState = not self.alt or not self.altState
               
               self.currentPos = 0.0
               self.beginHSVs = self.endHSVs
               self.endHSVs = self.__generateRandomHSV()
               print 'Generating next random shape!'
          
     def __generateRandomHSV(self):
          '''Generates a list of randomized HSV tuples, with hue normally distributed as per distribution config.
          The list has as many HSV tuples as this instance's lights has pixels'''
          # First generate an HSV list with the same number of HSV tuples as the LightMatrix has pixels
          numPx = self.lights.rows * self.lights.cols
          hsv = ones((numPx, 3))
          
          hueStdDev = self.hueStdDev if self.altState else 0.001
          satStdDev = self.satStdDev if self.altState else 0.001
          
          # Randomize the hues to be normal
          hsv[:,0] = np.random.normal(self.hueMean, hueStdDev, numPx)
          hsv[:,0] %= 1 #wrap hues around (-0.1 --> 0.9;  1.1-->0.1)
          
          # Randomize saturations to be normal
          hsv[:,1] = np.random.normal(self.satMean, satStdDev, numPx)
          hsv[:,1] = map(lambda s: max(0, min(1, s)), hsv[:,1]) # limit to between 0 and 1
          
          return hsv
     
     def __setDMToHSVMatrix(self, hsvList):
          '''Sets this instance's lights's RGB data array to be the HSV list passed in
          @param hsvList: an HSV list of the shape spit out by generateRandomHSV'''
          
          # Transform hsv to RGB
          rgbs = np.array(map(lambda hsv: colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]), hsvList))
          
          # Reshape, then set as the lightMatrix's data
          self.lights.data = rgbs.reshape(self.lights.rows, self.lights.cols, 3)
     