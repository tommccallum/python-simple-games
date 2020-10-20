#!/usr/bin/python

## To help learn how to use the mouse


import pygame
import sys
import math
import random
import time

## global variables for control
width=640
height=480
state=False


## define a shape which has a border which flashes
class FlashingRectangle:
    x=200
    y=200
    width= 100
    height=100
    color=(255,0,0)
    it=0 ## iteration
    screen=None
    maxsteps=50
    
    ## current size during animation
    cx=0
    cy=0
    cw=0
    ch=0
    
    ## contructor
    def __init__(self, screen, x=200, y=200, width=100, height=100, color=(255,0,0)):
        self.screen=screen
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height

    def shrink(self):
        ## only shrink for half the steps
        if self.it >= int(round(self.maxsteps/2)):
            self.grow()
            return
        if self.it <=0:
            self.cx=self.x
            self.cy=self.y
            self.cw=self.width
            self.ch=self.height
        else:
            self.cw = self.cw - int(round((0.02 * self.cw)))
            self.ch = self.ch - int(round((0.02 * self.ch)))
            self.cx = self.x + int(round(( self.width - self.cw ) / 2))
            self.cy = self.y + int(round(( self.height - self.ch )/2))

    def grow(self):
        print("grow "+ str(self.it))
        if self.it < int(round(self.maxsteps/2)):
            self.shrink()
            return
        if self.it == self.maxsteps:
            cx=self.x
            cy=self.y
            cw=self.width
            ch=self.height
        else:
            print("cw:"+str(max(1,int(round((0.02 * self.cw))))))
            self.cw = self.cw + max(1,int(round((0.02 * self.cw))))
            if self.cw > self.width:
                self.width = self.cw
            self.ch = self.ch + max(1,int(round((0.02 * self.ch))))
            if self.ch > self.height:
                self.height = self.ch
            self.cx = self.x + int(round(( self.width - self.cw )/2))
            if self.cx < self.x:
                self.cx = self.x
            self.cy = self.y + int(round(( self.height - self.ch )/2))
            if self.cy < self.y:
                self.cy = self.y

    ## draw routine
    def draw(self):
        self.shrink()
        pygame.draw.rect( self.screen, self.color, (self.cx, self.cy, self.cw, self.ch), 0 )
        self.it = self.it + 1
        if self.it > self.maxsteps:
            self.it=0


## draw score
class TopBar:
    score=0
    level=0
    def __init__(self,screen):
        self.score=0
        self.level=0
        self.screen=screen

    def score(self,value):
        self.score=value
        self.draw()

    def level(self,value):
        self.level=value
        self.draw()

    def draw(self):
        txt = "Level: "+str(self.level)+" Score: "+str(self.score)
        ## display score text using a given font
        f = pygame.font.SysFont("monospace",15)
        label = f.render("Level: "+str(self.level)+" Score: "+str(self.score), 1, (0,0,0))
        screen.blit(label, (10,10))

## control the whole board
class board:
    screen=None
    rectangles=[]
    flashing=[]
    topbar=None

    def __init__(self,screen):
        self.screen=screen
        topbar=TopBar(screen)
        topbar.level=1
        
    def setup():
        ## build rectangles
        print("hello")
        
    def draw():
        screen.fill((255,255,255)) ## clear screen to background color (white)
        topbar.draw()    
        for ii in range(0,len(rectangles)):
            pygame.draw.rect( rectangles[ii] )
        pygame.update()

    def nextLevel():
        self.level = self.level +1
        self.setup()

    def isCompleted():
        print("is completed")

        
pygame.init()

## screen setup
## (0,0) is upper left hand corner
screen = pygame.display.set_mode( (width, height), 0, 32 )

screen.fill((255,255,255)) ## clear screen to background color (white)

if False:
    ## test screen
    tb = TopBar(screen)
    tb.draw()
    pygame.display.update()

## test rectangle
rct = FlashingRectangle(screen)
for ii in range(0,300):
    print("ii:"+str(ii))
    screen.fill((255,255,255)) ## clear screen to background color (white)
    rct.draw()
    pygame.display.update()
    pygame.time.wait(100)





while True:
    if state==True:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                board.onClick( pos )
                if board.isCompleted():
                    state=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit("Bye!")
                if event.key == pygame.K_n:
                    board.nextLevel()
    else:
        # waiting for player to restart
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state=True
                    startTime=time.clock()
                    score=0
                    cnt=0
                    sleep=initialSleep
                    direction_x = random.choice([-1,1])
                    direction_y = random.choice([-1,1])
                    level=1
                    radius = initialRadius
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit("Bye!")               
