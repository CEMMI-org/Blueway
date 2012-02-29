from config import CONFIG
import pygame, sys
from pygame.locals import Color
#import pdb
from numpy import maximum,minimum, array
import util.TimeOps as timeops

class GameScreen:
    size = []
    locs = []
    pixels = []
    def __init__(self):
        pygame.init()    

    def setup_screen(self,size,locs):
        self.size = array(size)*CONFIG.scale
        self.locs = locs
        #size = (1000, 200)
        self.screen = pygame.display.set_mode([self.size[2]+CONFIG.margin,self.size[3]])
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color(0,0,0))
        self.stopwatch = timeops.Stopwatch()
        self.stopwatch.start()

    def render(self, px=None, currentTime=timeops.time()):
        if px != None:
            self.pixels = px    

        # David C's mod to prevent queue overflow 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            lastevent = event

        if CONFIG.scale:
            scale = CONFIG.scale
        else:
            scale = 1
        for i in range(len(self.locs)):
            loc = array(self.locs[i])
            value = self.pixels[i]
            if not(all(value == (0,0,0))):
            	pygame.draw.circle(self.background, value, loc*scale, scale)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption("fps: "+str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
