#!/usr/bin/env python
# above line for unix only

import optparse, time, sys, math
from display.route_display import *
import numpy
import util.TimeOps as timeops

if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] incrementor")
	parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
	parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
	parser.add_option("--time", action="store", type="int", help="number of seconds to run")
	
	(opts, args) = parser.parse_args()
	if len(args) != 1:
		parser.error("incorrect number of arguments")	

	incrementor = int(args[0])

	stopwatch = timeops.Stopwatch()
	stopwatch.start()


	box = numpy.ones([100,100]) * 1.0
	
	for x in range(100):
		for y in range(100):
			xd = abs(x-50)/50.0
			yd = abs(y-50)/50.0
			td = math.sqrt(math.pow(xd,2)+ math.pow(yd,2))
			box[x,y] =  1 - td
			if box[x,y] < 0:
				box[x,y] = 0

	
	#print box
	
	colorf = numpy.random.random(3) + .01
	colorf[:] *= 1/(colorf[0] + colorf[1] + colorf[2])
	
	data = numpy.zeros([50, 3, 4]) * 1.0
	
	x=[0,25,47]
	y=[0,60,30]
	xv=[incrementor, -1*incrementor, incrementor]
	yv=[incrementor, incrementor, -1*incrementor]
	
	
	brightness = [1.0,1.0,1.0]
	
        while ((not opts.time) or stopwatch.elapsed() / 1000 < opts.time):
		

		#fade
		if (stopwatch.elapsed() < 2000):
			mbrightness = stopwatch.elapsed() / 2000
		elif (opts.time and (opts.time - stopwatch.elapsed()/1000.0) <= 2):
			mbrightness = ((opts.time - stopwatch.elapsed()/1000.0))/2
		else:			
			mbrightness = 1
		
		

		for color in range(0,3):
			if brightness[color] > mbrightness:
				brightness[color] = mbrightness
				
			data[:,color,:] = brightness[color] * box[x[color]:x[color]+50, y[color]:y[color]+4]
		
		
		route_display(numpy.reshape(data, (150,4)))
	
		#random brightness shifting		
		#brightness[:] = (numpy.random.random(3)) / 5 + .8		
		

		time.sleep((opts.delay or 50)/1000.)
		
		
		
		for color in range(0,3):
		
			x[color] = x[color] + xv[color]
			y[color] = y[color] + yv[color]
			
			#print str(color)+" "+str(x[color])+" "+str(y[color])+" "+ str(xv[color])+" "+str(yv[color])
			if (x[color] > 49) :
				x[color] = 49
			elif (x[color] < 0):
				x[color] = 0
			
			if (y[color] > 95):
				y[color]  = 95
			elif (y[color] < 0 ):
				y[color] = 0
		
			if ( x[color] >= 49 or x[color] <= 0):
				if (numpy.random.random(1) > .75):
					x[color] -= xv[color]
				else:
					xv[color] *= -1
			
 			
			if ( y[color] >= 95 or y[color] <= 0 ):
				if (numpy.random.random(1) > .75):
					y[color] -= yv[color]
					brightness[color] = numpy.random.random(1)
				else:
					yv[color] *= -1
					brightness[color] = 1

			
		
	print 'done'
	sys.exit(0)
