#!/usr/bin/env python

# above line for unix only



import optparse, time, sys

from display.route_display import *

from numpy import ones, zeros



def CopyIntoArrayFromLeft(smArray, lgArray, lgPosition):

	smLen = len(smArray)

	lgLen = len(lgArray)

	lgStart = lgPosition - smLen

	smStart = 0

	if (lgStart < 0):

		smStart = lgStart * -1

		lgStart = 0

	#print smStart

	#print smLen

	#print lgStart

	#print lgPosition

	if (lgPosition > lgLen):

		lgPosition = lgLen

		smLen = lgPosition - lgStart

	lgArray[lgStart:lgPosition] = smArray[smStart:smLen]

	return



if __name__ == '__main__':

	chainLength = 50

	chainWidth = 4

	delay = .05

	data = zeros([chainLength*3,chainWidth])

	trailRight = [1.0, 1.0, 1.0, .75, .75, .75, .5, .5, .5, .25, .25, .25, 0.0, 0.0, 0.0]

	trailLeft = trailRight.reverse()

	row = 0

	rowCount = 0

	loopCount = 0

	while rowCount <= 100:

		while loopCount <= chainLength*3+len(trailRight):

			#print data

			route_display(data)

			time.sleep(delay)

			#raw_input();

			CopyIntoArrayFromLeft(trailRight,data[:,row],loopCount)

			loopCount += 3

		rowCount += 1;

		row = rowCount % 4

		loopCount = 0

	print 'done'

	sys.exit(0)
