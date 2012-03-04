#!/usr/bin/env python
# above line for unix only

import colorsys
from numpy import ones

class BluewayPattern(object):
     '''Base-class for Blueway patterns to be executed by the bluewayExecutor script.
     Defines standard conventions for your Blueway patterns so that multiple patterns 
     can be executed sequentially.
     
     The main idea is that you always have a LightMatrix instance at self.lights, and you
     modify it to draw one frame of your pattern every call to tick().  The bluewayExecutor
     handles outputting the pattern to the route_display, setting the frequency of the ticks,
     and switching between multiple patterns.'''
     
     # LightMatrix instance that you can access to change pixels in your pattern
     lights = None
     
     def __init__(self, lightMatrix):
          '''Default constructor.  Just saves the master lightMatrix as self.lights that
          your class extension can reference and use.
          
          Note: your pattern can implement its own constructor (eg to accept additional,
          pattern-specific params), but make sure your constructor still accepts a LightMatrix
          argument and that you chain your constructor to here by making a call like this:
               super(MyClassName, self).__init__(lightMatrix)
          
          @param lightMatrix: LightMatrix instance to be used by your Pattern'''
          self.lights = lightMatrix
     
     def tick(self):
          '''Method to draw the next 'frame' of your animation pattern.  The executor
          script calls this method once every <delay> ms.  This method should do stuff
          to self.lights and set up the next frame of your pattern animation.
          
          Do NOT try making a call to self.lights.display() or putting any sleep loop in here...
          all of that is done automatically by the executor.  Just set the appropriate state of 
          self.lights for the next frame of your pattern.'''
          raise NotImplementedError("Your BluewayPattern instance is expected to override the tick()"
                                    + " method with your pattern implementation!")

class LightMatrix:
     """ Class for storing data to be sent to lights 
     Rows, Columns, or Pixels can be set either by an RGB or HSV tuple
     
     For RGB, each tuple element is to be a float between 0 and 1 representing 
     the R, G, and B channels
     
     For HSV, each tuple element is to be a float between 0 and 1 where:
       hue: 0.0 is red, .333 is green, .667 is blue
       saturation: "amount of color" -- 0.0 is white/grey, 1.0 is full color
       value: "amount of darkness/black" -- 0.0 is black, 1.0 is full value (HS)
     
     For example, an HSV tuple of [.667, 1., 1.] is (just about) equivalent 
     to RGB [0.0, 0.0, 1.0]
     """

     #route_display function reference
     route_display = None

     #eventually take these two from config:
     rows = 4 
     cols = 50
     channels = 3
     
     #data array
     data = None

     def __init__(self, route_display, intensity = 0.0):
          """ create NumPy matrix of rows x 50 x RGB with
              the route_display instance to output to 
              and a given intensity (optional, defaults to 0.0 'off')"""
          self.data = ones((self.rows, self.cols, self.channels)) * intensity
          self.route_display = route_display

          self.totalChannels = self.channels*self.cols
     
     def getShape(self):
          '''Convenience method to return shape of underlying data array'''
          return (self.rows, self.cols, self.channels)

     def setRowRGB(self,row,color):
          """ pass in which row to change and either:
          a number to set for all channels (R,G,B) in all pixels of the row
               e.g: .5 for half-intensity to all 3 color channels across 50 columns
          an RGB array to set for all pixels in that row
               e.g. [1,0,0] for red across the row
          an array of RGB values for all pixels in the row
                e.g. [[1,0,0],[0,0,1],[1,0,0],[0,0,1], ... ] with 46 more in ...
                to alternate red and blue across all 50 pixels in a row"""
          self.data[row,:] = color
    
     def setRowHSV(self, row, color): 
          """ pass in which row to change and either:
          a number to set as the hue for all pixels in the row (saturation and value are 1)
               e.g: .33 for green to all pixels in the row
          an HSV array to set for all pixels in that row
               e.g. [.33,1,1] for full-green across the row
          an array of HSV values for all lights in the row
               e.g. [[0,1,1],[.667,1,1],[0,1,1],[.667,1,1], ... ] with 46 more in ...
               to alternate red and blue across all 50 columns in a row"""
          self.setRowRGB(row, self.__hsvColorToRgbColor(color)) 
          

     def setColumnRGB(self, col, color):
          """ pass in which column to change and either:
          a number to set for all channels (R,G,B) in all rows of the column
               e.g: .5 for half-intensity to all 3 color channels down 4 rows
          an RGB array to set for all lights in that row
               e.g. [1,0,0] for red down the column
          an array of RGB values for all lights in the column
                e.g. [[1,0,0],[0,0,1],[1,0,0],[0,0,1]] to alternate red and
                blue down all 4 rows in a column"""
          self.data[:,col] = color
     
     def setColumnHSV(self, col, color):
          """ pass in which column to change and either:
          a number to set as the hue for all pixels in the column (saturation and value are 1)
               e.g: .33 for green to all pixels in the column
          an HSV array to set for all pixels in that column
               e.g. [.33,1,1] for full-green across the colum
          an array of HSV values for all lights in the row
               e.g. [[0,1,1],[.667,1,1],[0,1,1],[.667,1,1]] to alternate red
               and blue down all 4 rows in a column"""
          self.setColumnRGB(col, self.__hsvColorToRgbColor(color))
          
     def setPixelRGB(self, row, column, color):
          """ pass in row,column of pixel location and either:
           a number to set for all channels (R,G, and B) of that pixel
           an RGB array that represents the color of that pixel"""
          self.data[row,column] = color
     
     def setPixelHSV(self, row, column, color):
          """ pass in row,column of pixel location and either:
           a number to set as the hue for that pixel (saturation and value are set to 1)
           an HSV array that represents the color of that pixel"""
          self.setPixelRGB(row, column, self.__hsvColorToRgbColor(color))
     
     def getPixelRGB(self, row, column):
          """ get the RGB array of the pixel at the position"""
          return self.data[row, column]
     
     def getPixelHSV(self, row, column):
          """ get the HSV tuple of the pixel at the position"""
          return colorsys.rgb_to_hsv(self.data[row, column, 0], self.data[row, column, 1], self.data[row, column, 2])

     def display(self):
          # reshaping 4,50,3 to 4,150 and then transposing to get 150,4
          outData=self.data.reshape(self.rows, self.totalChannels).transpose()
          self.route_display(outData)
     
     def __hsvColorToRgbColor(self, rgbColor):
          """The setXxxRGB methods have a convention where the "color" variable is either
          a number, an RGB array, or an array of RGB values.  This convention is adopted
          for the setXxxHSV methods.  Since the HSV methods call the RGB methods to 
          encourage code reuse, we need to convert the HSV params into a 
          convention-equivalent RGB param"""
          if type(rgbColor) == int:
               # single hue
               return colorsys.hsv_to_rgb(rgbColor, 1, 1)
               
          elif type(rgbColor) == list and type(rgbColor[0] == int):
               # HSV list
               return colorsys.hsv_to_rgb(rgbColor[0], rgbColor[1], rgbColor[2])
               
          elif type(rgbColor) == list and type(rgbColor[0] == list):
               # list of HSV lists
               return [colorsys.hsv_to_rgb(x[0], x[1], x[2]) for x in rgbColor]
          
          else:
               raise TypeError("Unknown HSV argument type!")    

# UTILITY METHODS
#-------------------
def minWrapAround(begin, end):
     '''Helper function to return min distance between two values, each [0,1], considering wrap-around.
     eg:
     .2, .4 -->  0.2
     .4, .2 --> -0.2
     .1, .9 --> -0.2  (not  0.8)
     .9, .1 -->  0.2  (not -0.8)
     '''
     dist = end - begin
     
     if (dist > 0.5):
          return dist - 1
     elif (dist < -0.5):
          return dist + 1
     else:
          return dist
     


def colorTweenHSV(begin, end, pos = 0.5):
     """Returns an in-between ("tween") color tuple that is somewhere between begin and end, 
     as specified by pos
     
     begin and end are HSV tuples ([0] wraps around, [1] and [2] don't)
     pos is a number between 0 and 1 that determines the position of the tween from begin to end
       e.g. a pos of 0.5 is exactly halfway between begin and end (in other words, the average),
            a pos of 0.0 returns begin, and a pos of 1.0 returns end
     returns a tweened tuple between begin and end"""
     
     pos = max(0, min(1, pos)) # enforce limits on pos
     return (begin[0] + minWrapAround(begin[0], end[0]) * pos, # hues can wrap around
             begin[1] + (end[1] - begin[1]) * pos,          # sat and value don't
             begin[2] + (end[2] - begin[2]) * pos) 

def colorTweenRGB(begin, end, pos = 0.5):
     """Returns an in-between ("tween") color tuple that is somewhere between begin and end, 
     as specified by pos
     
     begin and end are RGB tuples (the tween operates on the shortest distance from begin[i] to end[i],
     including a wrap-around path).
     
     pos is a number between 0 and 1 that determines the position of the tween from begin to end
       e.g. a pos of 0.5 is exactly halfway between begin and end (in other words, the average),
            a pos of 0.0 returns begin, and a pos of 1.0 returns end
     returns a tweened tuple between begin and end"""
     
     pos = max(0, min(1, pos)) # enforce limits on pos
     return (begin[0] + minWrapAround(begin[0], end[0]) * pos, # all interpolations take min distance
             begin[1] + minWrapAround(begin[1], end[1]) * pos, # including wrap-around
             begin[2] + minWrapAround(begin[2], end[2]) * pos)
