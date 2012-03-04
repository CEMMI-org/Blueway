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
	
	data = numpy.zeros([50, 3, 4])
	
	x=0
	y=0
	xv=incrementor
	yv=incrementor
	brightness = 1.0
	
        while ((not opts.time) or stopwatch.elapsed() / 1000 < opts.time):
		

		if (opts.time and (opts.time - stopwatch.elapsed()/1000.0) <= 2):
			brightness2 = ((opts.time - stopwatch.elapsed()/1000.0))/2
			if brightness2 < brightness:
				brightness = brightness2

		
		data[:,0,:] = brightness * colorf[0] * box[x:x+50, y:y+4]
		data[:,1,:] = brightness * colorf[1] * box[x:x+50, y:y+4]
		data[:,2,:] = brightness * colorf[2] * box[x:x+50, y:y+4]
		
		route_display(numpy.reshape(data, (150,4)))

		#random color shifting		
		colorf[:] *= 1+(numpy.random.random(3))		
		colorf[:] *= 1/(colorf[0] + colorf[1] + colorf[2])

		time.sleep((opts.delay or 250)/1000.)
		
		x += xv
		y += yv
		
		if (x > 49) :
			x = 49
		elif (x < 0):
			x = 0
			
		if (y > 95):
			y  = 95
		elif (y < 0 ):
			y = 0
		
		if ( x >= 49 or x <= 0):
			if (numpy.random.random(1) > .75):
				x -= xv
			else:
				xv *= -1
			
 			
		if ( y >= 95 or y <= 0 ):
			if (numpy.random.random(1) > .75):
				brightness = 1 + (3 * numpy.random.random(1))
				y -= yv

			else:
				brightness = 1
				yv *= -1

			#new color
			colorf = numpy.random.random(3)
			colorf[:] *= 1/(colorf[0] + colorf[1] + colorf[2])
		
		
	print 'done'
	sys.exit(0)
