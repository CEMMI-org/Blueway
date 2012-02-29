'''
BluewayPattern demo example.  Implements the example2 pattern using the BluewayPattern
object-oriented approach specific for running sequences of patterns by bluewayExecutor.

@author: DLopuch
'''

from light_matrix import BluewayPattern, LightMatrix

OFF = [0,0,0]
CYAN = [0,1,1]
MAGENTA = [1,0,1]
YELLOW = [1,1,0]
ON = [1,1,1]


class Example3Pattern(BluewayPattern):  #your pattern class always extends BluewayPattern
     
     #superclass has field "lights", set by the super's constructor
     
     incr = 1
     curCol = 0
     
     # set up an array to cycle through colors
     colors = [CYAN, MAGENTA, YELLOW, OFF, ON]
     colorIndex = 0

     def __init__(self, lightMatrix, incr=1, colStart=0):
          '''
          Pattern Constructor.
          @param lightMatrix: LightMatrix instance to use in this Pattern
          @param incr: how many columns to increment by in each tick
          @param colStart: initial column to start changing colors
          '''
          
          #always include this constructor chaining -- chained constructor saves the LightMatrix as "self.lights"
          super(Example3Pattern, self).__init__(lightMatrix)
          
          self.incr = incr
          self.curCol = colStart
     
     def tick(self):
          '''Main pattern loop'''
          
          # If we've gone above or below column limits, get a new color and switch directions
          if (self.curCol < 0 or self.curCol >= self.lights.cols):
               #ensure the curCol index remains in the actual lights
               self.curCol = max(min(self.curCol,self.lights.cols-1),0)
               
               # Reverse the direction of pattern movement.
               self.incr = -self.incr
               
               # After getting up to 50 or down to -1, increment the colorIndex.
               self.colorIndex += 1
               # The modulo operator "%" says take the remainder of a division, so
               # colorIndex will count: 0,1,2,3,4,0,1,2,3,4 since len(colors) == 5 .
               self.colorIndex = self.colorIndex % len(self.colors)
          
          # Loop over all columns of the lights, assigning the new value
          self.lights.setColumnRGB(self.curCol, self.colors[self.colorIndex])
          self.curCol += self.incr
               
                
          






