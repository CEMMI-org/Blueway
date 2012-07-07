#!/usr/bin/env python
# above line for unix only

import optparse, time, sys
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
	loopCount = opts.start or 0  #opts.start will be "None" if not specified

	stopwatch = timeops.Stopwatch()
	stopwatch.start()


	data = zeros([50,3,4]) * 1.0
	
	
	data[:,:,:] = numpy.reshape(numpy.random.rayleigh(1,600), (50,3,4))

	count = 0
	while count < 4:
		data[:,:,count] = numpy.sort(data[:,:,count])
		count += 1

	data[:,0,:] -= .7
	data[:,1,:] -= .7

	brightness = 1
	thisD= numpy.reshape(data,(150,4))
        while ((not opts.time) or stopwatch.elapsed() / 1000 < opts.time):

		if (stopwatch.elapsed() < 2000):
			brightness = stopwatch.elapsed() / 2000
		elif (opts.time and (opts.time - stopwatch.elapsed()/1000.0) <= 2):
			brightness = ((opts.time - stopwatch.elapsed()/1000.0))/2
		else:			
			brightness = 1

		#lastD = thisD.copy()
		thisD = (brightness * numpy.reshape(data, (150,4)))
		route_display(thisD)#*.5+lastD*.5)
		data = numpy.roll(numpy.reshape(data, (50,3,4)), -2, 1)
		data = numpy.roll(data, -16 *(1 + 3*(incrementor-1)) )
		time.sleep((opts.delay or 250)/1000.)
		
		if (numpy.random.random(1) > .5):
			dot1 = [numpy.random.randint(0,50),numpy.random.randint(0,4)]
			dot2 = [numpy.random.randint(0,50),numpy.random.randint(0,4)]
			temp = data[dot1]
			data[dot1] = data[dot2]
			data[dot2] = temp
		
		
		loopCount += 1		
		
        	
		
	print 'done'
	sys.exit(0)
