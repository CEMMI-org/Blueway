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

	data = numpy.random.random(600) * 1.0
	data = numpy.reshape(data, (50,3,4))
	data[:,1,:] -= .5
	data[:,2,:] -= .5
	
	brightness = 1

        while ((not opts.time) or stopwatch.elapsed() / 1000 < opts.time):

		if (stopwatch.elapsed() < 2000):
			brightness = stopwatch.elapsed() / 2000
		elif (opts.time and (opts.time - stopwatch.elapsed()/1000.0) <= 2):
			brightness = ((opts.time - stopwatch.elapsed()/1000.0))/2
		else:			
			brightness = 1


		
		route_display(brightness * numpy.reshape(data, (150,4)))
		#data = numpy.roll(numpy.reshape(data, (50,3,4)), 1, 2)
		data = numpy.roll(numpy.reshape(data, (50,3,4)), 1)
		time.sleep((opts.delay or 250)/1000.)
		
		if (loopCount % 12 == 0):
			data[:,:,1] = numpy.reshape(numpy.random.random(150), (50,3))
			data[:,1,1] -= .5
			data[:,2,1] -= .5	
		
		loopCount += incrementor
		       	
		
	print 'done'
	sys.exit(0)
