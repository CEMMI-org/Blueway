#!/usr/bin/env python

# Flip the LED strip like a twisting ribbon.
# Michael Dewberry Feb 2012

import optparse, time, sys, math, pdb
from display.route_display import *
from numpy import ones, zeros, ndenumerate
from copy import deepcopy
from math import pi


def lerp(x, y, t):
	return x+t*(y-x)
	
def flip(column, t):
	col0 = deepcopy(column[:,0])
	col1 = deepcopy(column[:,1])
	column[:,0] = lerp(column[:,0], column[:,3], t)
	column[:,1] = lerp(column[:,1], column[:,2], t)
	column[:,2] = lerp(column[:,2], col1, t)
	column[:,3] = lerp(column[:,3], col0, t)
	return column
	
def cycleFlip(data, time, totalTime):
	out = deepcopy(data)
	width = opts.width or 28.0
	curve = opts.curve or 1.5
	loop = 0
	while loop < time + width:
		t = 1.0
		if loop > time - width:
			t = min(1.0, max(-1.0, 1.5*math.atan(0.1*(time-loop))/(2.0*pi)+0.5))
		out[loop:loop+3,:] = flip(out[loop:loop+3,:], t)
		loop = loop + 3
	return out		

if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] incrementor")
	parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
	parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
	parser.add_option("--width", action="store", type="int", help="Limit the flip calculation to <width> LEDs on each side of the breakpoint. Default 22")
	parser.add_option("--curve", action="store", type="float", help="Scaling factor controlling steepness of the arctan curve used for the flip. Default 1.5")
	parser.add_option("--second", action="store", type="int", help="Set greater than zero to add a second flip. 0 means no flip; >0 means number of LEDs to delay second flip.")
	(opts, args) = parser.parse_args()

	loopCount = opts.start or 0  #opts.start will be "None" if not specified
	secondphase = opts.second or 0	

	data = ones([150,4])
	data[:,0] = (1.0, 0.0, 0)*50 
	data[:,1] = (1.0, 0.0, 0.5)*50 
	data[:,2] = (1.0, 1.0, 0.0)*50 
	data[:,3] = (0.5, 0.5, 1.0)*50

	newdata = deepcopy(data)
	while 1:
		loopCount = 0
		while loopCount < 200:
			route_display(newdata)
			time.sleep((opts.delay or 500)/1000.)
		
			newdata = cycleFlip(data, loopCount*1.0, 200.)
			if secondphase > 0:
				newdata = cycleFlip(newdata, loopCount*1.0-secondphase, 200.)
	
			loopCount = loopCount + 3
		
		data = deepcopy(newdata)
		print 'done'
		
	sys.exit(0)
