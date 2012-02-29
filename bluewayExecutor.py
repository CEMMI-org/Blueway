#!/usr/bin/env python
# above line for unix only

'''
Object-oriented Blueway pattern executor.

Implement your patterns as classes extending light_matrix.BluewayPattern (i.e. initialize with 
a LightMatrix param and implement a tick() method) then:
  1) import your BluewayPattern in this file under the "USER IMPORTS" section
  2) adjust the initializeUserPatterns() method to instantiate your patterns 
     with all appropriate parameters for your parameters, using the command line arguments
     array if needed.

TO RUN:
Run this python class with the following options:
  --tickDelay ###: number of ms to wait before each pattern tick (default: 100)
  --secondsPerPattern ##: number of seconds to show each pattern for before moving on to the next one
  <args>: Any additional arguments will be passed to the initializeUserPatterns() method, and you can
          read and use them as needed for your patterns list.
'''

import optparse, time, sys
from numpy import ones, zeros, array
from time import sleep

from display.route_display import *
from light_matrix import LightMatrix

#-----------------------
# USER IMPORTS
#   Import your light_matrix.BluewayPattern extensions here!
from normalDistributedPixels import *
from riverWipe import *
from rainbowRiver import *

userPatterns = [] #Array to keep track of BluewayPattern instances
def initializeUserPatterns(args, tickDelay, secondsPerPattern):
     '''USER INSTANTIATIONS
     -------------------------------
     Add all of your user patterns here by instantiating new instances of them
     and appending the instance to userPatterns.
     
     Your BluewayPattern implementations' constructors should all have one LightMatrix param
     that they passes to the superclass BluewayPattern's constructor.  Get a LightMatrix instance
     for your pattern by calling getPatternLM()
     
     All of the command-line arguments are passed here incase you want to instantiate your patterns
     with specific command-line arguments.
     
     For convenience, you are told how many ms per tick your pattern will be executed with
     (tickDelay) and the number of seconds your pattern is given to run (secondsPerPattern).  
     Use these if your pattern wants to be customized by these timing params. 
        
     @param args: all command-line arguments incase you want to parameterize your pattern
                  executions through a specific command-line argument.  Note that these tend
                  to be strings... you may need to add a cast to int() or float()
     @param tickDelay: The number of ms in between each tick that your patterns will be executed with
     @param secondsPerPattern: The number of seconds your pattern will be allocated'''
     
     #userPatterns.append(Example3Pattern(getPatternLM()))
     #userPatterns.append(Example3Pattern(getPatternLM(), int(args[0]), int(args[1])))
     userPatterns.append(RainbowRiver(getPatternLM(), getPatternLM(), tickDelay, 10., 
                                      hueMean = .7, hueStdDev = .1, satMean = .7, satStdDev = .1,
                                      numRainbows = 3, rainbowWidth = 0))
     
     userPatterns.append(RiverWipe(getPatternLM(), 2000./tickDelay, whiteWidth = 20))
     userPatterns.append(RainbowRiver(getPatternLM(), getPatternLM(), tickDelay, 10., 
                                      hueMean = .7, hueStdDev = .1, satMean = .7, satStdDev = .1,
                                      numRainbows = 3, rainbowWidth = 10))
     #userPatterns.append(NormalDistributedPixels(getPatternLM(), 5000./tickDelay, 
     #                                            float(args[0]), float(args[1]),
     #                                            float(args[2]), float(args[3])))

# --------- END USER CONFIG ------------

lms = []
def getPatternLM():
     '''Gets a new LightMatrix instance for a userPattern.  
     Expected to be called only once per pattern'''
     lm = LightMatrix(None, 1.0)
     lms.append(lm)
     return lm

def main():
     config = getCommandLineOptions()
     tickDelay = config[0]
     secondsPerPattern = config[1]
     args = config[2] # any misc. user args

     # initialize master display at full white (1.0)
     lights = LightMatrix(route_display, 1.0) 
     
     # initialize all patterns, passing to each any user-defined args
     initializeUserPatterns(args, tickDelay, secondsPerPattern)
     
     # send values to the lights/simulator for a count of 2 seconds
     # to give the browser time to open, etc.
     print "initializing..."
     for i in range(2):
          lights.display()
          sleep(1)
     print "...done init()"
     
     # Loop through all patterns
     numberOfTicks = secondsPerPattern * 1000 / tickDelay
     patternI = 0
     tickI = 0
     while True:
          print 'Playing pattern ', patternI
          #print 'lights.data: ', lights.data
          
          while (tickI < numberOfTicks):
               #print 'tick ', tickI, '/', numberOfTicks
               userPatterns[patternI].tick()
#               try:
#                    userPatterns[patternI].tick()
#               except Exception as err:
#                    print 'Pattern ', patternI, ' errored out: \n  ', err.__class__, ': ', err
#                    print 'Moving on to next pattern...'
#                    patternI = (patternI + 1) % len(userPatterns)
#                    sleep(tickDelay / 1000.)
#                    continue
               
               #display the Pattern's modifications
               lights.data = userPatterns[patternI].lights.data
               lights.display()
               
               #and tick
               tickI += 1
               sleep(tickDelay / 1000.)
          
          # Move on to next pattern, or start from beginning
          patternI = (patternI + 1) % len(userPatterns)
          tickI = 0

def getCommandLineOptions():
     """ interprets and returns script-specific options"""
     parser = optparse.OptionParser(usage="%prog [options] pattern-specific arguments")
     parser.add_option("--tickDelay", action="store", type="int", help="Delay in ms for each tick of the pattern")
     parser.add_option("--secondsPerPattern", action="store", type="int", help="How many seconds to display each pattern for")
     (opts, args) = parser.parse_args()
   
     tickDelay = opts.tickDelay or 100 # in milliseconds
     secondsPerPattern = opts.secondsPerPattern or 10
     
     return (tickDelay, secondsPerPattern, args)

if __name__ == '__main__':
     main()