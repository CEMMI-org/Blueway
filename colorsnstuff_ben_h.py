#!/usr/bin/env python
# above line for unix only

import optparse, time, sys
from display.route_display import *
from numpy import ones, zeros
import numpy as np
import util.TimeOps as timeops
if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] incrementor")
	parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
	parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
	parser.add_option("--time", action="store", type="int", help="number of seconds to run")

	(opts, args) = parser.parse_args()
	stopwatch = timeops.Stopwatch()
	stopwatch.start()

#	if len(args) != 1:
#		parser.error("incorrect number of arguments")	
	try:
		incrementor = int(args[0])
	except:
		incrementor = 1
#	incrementor = int(args[0]) or 1
	loopCount = opts.start or 0  #opts.start will be "None" if not specified
    
    #linear gradient from 'from_hue' to 'to_hue'
	def pret2(from_hue, to_hue):
		diff = [to_hue[i] - from_hue[i] for i in range(3)]
            
		a = np.ones(150)
		ar = np.concatenate([np.linspace(0,1,25), np.linspace(1,0,25)])
		for i in range(0,150):
			a[i] = ar[i/3] * diff[i%3] + from_hue[i%3]
		return a
    
    #ar len 50
	def pret(ar, hues):
		a = np.ones(150)
		for i in range(0,150):
			a[i] = ar[i/3] * hues[i%3]
		return a
            
    
    #ar len 150
	def horiz(ar):
		a = np.zeros(600).reshape([150,4])
		for i in range(0,150):
			for j in range(0,4):
				a[i][j] = ar[i]
		return a.flatten()
    
	def horiz2(ar, ar2):
		a = np.zeros(600).reshape([150,4])
#		diff2 = [0,.6666,.3333,1.]
		diff2 = [0,.55,.45,1.]		# emulator
#		diff2 = [0,0.45,1,.55]		# LIVE
		for i in range(0,150):
			diff = ar2[i] - ar[i]
			for j in range(0,4):
				a[i][j] = ar[i] + diff * diff2[j] #(j*1.0/4)
		return a.flatten()

	def horiz3(ar, ar2):
		a = np.zeros(600).reshape([150,4])
#		diff2 = [0,.6666,.3333,1.]
#		diff2 = [0,.55,.45,1.]
# 1,4,2,3  		
		diff2 = [0,1,1,1]
		for i in range(0,150):
			diff = ar2[i] - ar[i]
			for j in range(0,4):
				a[i][j] = ar[i] + diff * diff2[j] #(j*1.0/4)
		return a.flatten()

# 1,3,4,2
# 1,4,2,3            
    
	FROM = [.2,0,1]
	TO = [1,0,.4]
	FROM2 = [1,0,.2]
	TO2 = [.4,0,1]
#	FROM = [1,0,0]
#	TO = [1,0,0]
#	FROM2 = [0,0,1]
#	TO2 = [0,0,1]
	FROM = [1,0,0]
	TO = [1,1,0]
	FROM2 = [0,1,0]
	TO2 = [0,0,1]
	
	frommat = [FROM2[i] - FROM[i] for i in range(3)]
	tomat = [TO2[i] - TO[i] for i in range(3)]
	
	
	hue = [0.5,0,0]
	mult = [0.,0.,1.]
	mult2 = np.concatenate([np.linspace(0,1,25)**2, np.linspace(1,0,25)**2])
#	print horiz(pret(ones(50),hue))
	thing = horiz(pret(mult2, mult)) + horiz(pret(ones(50),hue))
#	print thing
	fade = np.concatenate([np.linspace(0,1,5)**2, np.linspace(1,0,5)**2])
	lspace = np.concatenate([np.linspace(0,1,300)**2, np.linspace(1,0,300)**2])
    
    
	hue_m = np.array([ hue[(i%12)/4] + lspace[i] * mult[(i%12)/4]  for i in range(0,600)])
	hue_m = hue_m.reshape([150,4])
#	print hue_m
# 10.32.1.*
# subnet 255.255.0.0
#	data = ones([150,4])*hue_m
	#thing1 = 
	thing = horiz(pret2(FROM,TO))
	thing = horiz2(pret2(FROM,TO),pret2(FROM2,TO2))
	data = thing.reshape([150,4])
	asd = 1
	MULTLENGTH = 67
	vmult = np.concatenate([np.linspace(0,1,MULTLENGTH/2+1),np.linspace(1,0,MULTLENGTH/2)])
	
        while ((not opts.time) or stopwatch.elapsed() / 1000 < opts.time):
		#if (stopwatch.elapsed() < 2000):
		#	brightness = stopwatch.elapsed() / 2000
		route_display(data)
#		time.sleep((opts.delay or 500)/1000.)
		time.sleep(0.1)
#		data[loopCount] = 0 
		from1 =  [ FROM[i] + frommat[i] * vmult[loopCount % MULTLENGTH] for i in range(3) ]
		from2 =  [ FROM[i] + frommat[i] * vmult[(loopCount + 1) % MULTLENGTH] for i in range(3) ]
		to1 = [ TO[i] + tomat[i] * vmult[loopCount % MULTLENGTH] for i in range(3) ]
		to2 = [ TO[i] + tomat[i] * vmult[(loopCount + 1) % MULTLENGTH] for i in range(3) ]
		thingy1 = horiz2(pret2(from1,to1),pret2(from2,to2))
		data = thingy1.reshape([150,4])
		data = np.concatenate([data[((loopCount%25)*6):],data[:((loopCount%25)*6)]])
        
        
#		data = np.concatenate([data[3:], data[:3]])
		loopCount += incrementor
	print 'done'
	sys.exit(0)
