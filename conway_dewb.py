#!/usr/bin/env python

# Simple Conway's Game of Life implementation.
# Michael Dewberry Feb 2012

# Oversamples a 48x50 "world" and condenses the top third 
# into the red channel, the middle into the green channel,
# and the lower third into blue.  Four world cells are averaged
# into each channel.

# Almost all of the behaviors can be overridden by subsituting 
# different function arguments into life().

# If framesPerGeneration is more than 1, there's an opportunity to
# animate the transitions.  Set fadeGenerations to 1 to do a simple
# linear RGB fade or use a combineFunc that produces different results 
# for different values of gRenderFrame.

# Todo: 
# - Change RGB fade to HSV fade
# - Move gOptions to opts for command-line use
# - Change hardcoded 48x50 world size to parameters

import optparse, time, sys, math, pdb, numpy
from display.route_display import *
from copy import deepcopy
from math import pi


def lerp(x, y, t):
	return x+t*(y-x)

def combFn_first(values):
	return values[0]
	
def combFn_average(values):
    return sum(values, 0.0) / len(values)
    
def combFn_sortFade(values):
	fc = gOptions['framesPerGeneration']
	return numpy.sort(values)[gRenderFrame%fc]
	
def combFn_maxFade(values):
	fc = gOptions['framesPerGeneration']
	return max(values)*(gRenderFrame%fc+1)/(1.0*fc)

def w2d_interleave(world, data, combineFn):
	# world is 48x50 matrix with 4 values per color in row
	# need 150x4 rgbrgbrgb matrix
	# combineOp turns four values into a single color
	x = 0
	for row in world:
		for ci in [0, 1, 2, 3]:
			st = 12*ci
			data[x+0,ci] = combineFn(row[st+0:st+4])
			data[x+1,ci] = combineFn(row[st+4:st+8])
			data[x+2,ci] = combineFn(row[st+8:st+12])
		x = x + 3

def w2d_colorplanes(world, data, combineFn):
	# world is 48x50 matrix with 4 values per color in row
	# need 150x4 rgbrgbrgb matrix
	# combineOp turns four values into a single color
	x = 0
	for row in world:
		for ci in [0, 1, 2, 3]:
			st = 4*ci
			data[x+0,ci] = combineFn(row[st+ 0:st+ 4])
			data[x+1,ci] = combineFn(row[st+16:st+20])
			data[x+2,ci] = combineFn(row[st+32:st+36])
		x = x + 3
		
def initFn_random():
	return numpy.random.randn(50,48) * 0.5 + 0.5
	
def initFn_randomWhite():
	world = numpy.zeros([50,48])
	plane = numpy.random.randn(50,16) * 0.5 + 0.5
	offset1 = numpy.random.randn(50,16) * 0.0005
	offset2 = numpy.random.randn(50,16) * 0.0005
	world[:,0:16] = plane
	world[:,16:32] = plane + offset1
	world[:,32:48] = plane - offset2
	return world
	
def initFn_randomPurple():
	world = numpy.zeros([50,48])
	plane = numpy.random.randn(50,16) * 0.5 + 0.5
	offset = numpy.random.randn(50,16) * 0.0005
	world[:,0:16] = plane
	world[:,32:48] = plane - offset
	return world	
	
def initFn_random():
	world = numpy.random.randn(50,48) * 0.5 + 0.5
	return world

def runFn_rollX(world):
	return numpy.roll(world, 1, axis=0)
	
def runFn_rollY(world):
	return numpy.roll(world, 4, axis=0)
	
def wrapcoord(arr, x, y):
	size = arr.shape
	if x < 0:
		x = x + size[0]
	if y < 0:
		y = y + size[1]
	if x >= size[0]:
		x = x - size[0]
	if y >= size[1]:
		y = y - size[1]
	return arr[x,y]

def neighbors(world, i, j):
	n = numpy.zeros(8)
	n[0] = wrapcoord(world,i-1,j-1)
	n[1] = wrapcoord(world,i-1,j)
	n[2] = wrapcoord(world,i-1,j+1)
	n[3] = wrapcoord(world,i,j-1)
	n[4] = wrapcoord(world,i,j+1)
	n[5] = wrapcoord(world,i+1,j-1)
	n[6] = wrapcoord(world,i+1,j)
	n[7] = wrapcoord(world,i+1,j+1)
	return n

def runFn_continuousConway(world):
	# from Game of Life Cellular Automata (Adamatzky) 13.2 p241
	# http://books.google.com/books?id=5iz6C0zzWKcC&pg=PA241
	T = 2.0
	e0 = 2.25
	x0 = 6.0
	fudge = 1.55 # default value of 2.0 from book blows up. higher vals die off slower
	def F(z): 
		return 1.0/(1.0 + math.exp(-2.0*z/0.3))
	def x(i,j):
		return world[i,j] + fudge*numpy.sum(neighbors(world,i,j))
	def E(i,j):
		return e0-math.pow(x(i,j)-x0, 2)
	wt1 = numpy.zeros([50,48])
	for i in range(0,50):
		for j in range(0,48):
			wt1[i,j] = F(E(i,j))
	return wt1

def life(initFunc, runFunc, combineFunc, w2dFunc, restart):
	global gGeneration
	global gRenderFrame
	global gOptions
	data = numpy.zeros([150,4])
	world = initFunc()
	gGeneration = 0
	prevGenFrameData = data

	while 1:
		world1 = runFunc(world)
		fc = gOptions['framesPerGeneration']
		for gRenderFrame in range(0, fc):
			w2dFunc(world1, data, combineFunc)
			if gGeneration > 0 and gOptions['fadeGenerations'] > 0:
				route_display(lerp(prevGenFrameData, data, (gRenderFrame+1/fc)))
				time.sleep((opts.delay or 500)/1000.)
			else:
				route_display(data)
				time.sleep((opts.delay or 500)/1000.)
		world = world1
		prevGenFrameData = deepcopy(data)
		gGeneration += 1
		if restart > 0 and gGeneration >= restart:
			gGeneration = 0
			black = numpy.zeros([150,4])
			for ff in range(0,3):
				route_display(lerp(prevGenFrameData, black, (ff+1/3)))
				time.sleep((opts.delay or 500)/1000.)
			world = world1 = initFunc()
			w2dFunc(world1, data, combineFunc)
			for ff in range(0,3):
				route_display(lerp(black, data, (ff+1/3)))
				time.sleep((opts.delay or 500)/1000.)
			
			
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] incrementor")
	parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
	parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
	parser.add_option("--resetgen", action="store", type="int", help="number of generations to run before restarting")
	(opts, args) = parser.parse_args()
	
	gGeneration = 0
	gRenderFrame = 0
	gOptions = { 'framesPerGeneration' : 6, 'fadeGenerations' : 1 } 
				
	#life(initFn_random, runFn_rollX, combFn_average, w2d_interleave, -1)	
	#life(initFn_bar, runFn_roll, combFn_average, w2d_interleave, -1)	
	#life(initFn_random, runFn_continuousConway, combFn_average, w2d_colorplanes, 25)	
	#life(initFn_randomWhite, runFn_continuousConway, combFn_average, w2d_colorplanes, 50)	
	#life(initFn_randomWhite, runFn_continuousConway, numpy.median, w2d_colorplanes, 50)	
	#life(initFn_randomWhite, runFn_continuousConway, combFn_sortFade, w2d_colorplanes, 50)	
	#life(initFn_randomWhite, runFn_continuousConway, combFn_maxFade, w2d_colorplanes, 50)	

	life(initFn_randomPurple, runFn_continuousConway, combFn_average, w2d_colorplanes, opts.resetgen or 50)	

	
	sys.exit(0)
