#!/usr/bin/python

##
## Game to improve LEFTCLICK, DOUBLECLICK, RIGHTCLICK
##

import pygame
import sys
import math
import random
import time

width=640
height=480

## large identical rectangles
x=50
y=50
rect_width=width - 2 * x
rect_height=height - 2 * y

COLORS = [(139, 0, 0), 
          (0, 100, 0),
          (0, 0, 139)]
TEXT= ["LEFT", "2 LEFT", "RIGHT"]

def random_color():
    return random.choice(COLORS)

pygame.init()

## screen setup
## (0,0) is upper left hand corner
screen = pygame.display.set_mode( (width, height), 0, 32 )

while True:
    screen.fill((255,255,255)) ## clear screen to background color (white)
    whatToDraw=random.choice([0,1,2])
    col=COLORS[whatToDraw]
    pygame.draw.rect( screen, col, (x,y,rect_width,rect_height), 0)

    f = pygame.font.SysFont("monospace",60)
    label = f.render(TEXT[whatToDraw], 1, (0,0,0))
    fs = f.size(TEXT[whatToDraw])
    dx = int(round((width / 2) - (fs[0]/2)))
    dy = int(round((height/2)-(fs[1]/2)))
    screen.blit(label, (dx,dy) ) 
    
    pygame.display.update()
    
    
    completed = False
    leftClick1 = None
    leftClick2 = None
    while completed==False:q
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                print("BUTTON:"+str(event.button))
                pos = pygame.mouse.get_pos()
                if event.button == 1: ## left
                    if whatToDraw == 1 and leftClick1 == None:
                        leftClick1 = time.clock()
                    elif whatToDraw == 1 and leftClick2 == None:
                        leftClick2 = time.clock()
                        print("DIFF:"+str(leftClick2 - leftClick1))
                        if (leftClick2 - leftClick1) <= 0.5:
                            completed = True
                        else:
                            leftClick1=None
                            leftClick2=None
                    if whatToDraw == 0:
                        completed=True
                elif event.button == 3: ## right
                    if leftClick1 != None or leftClick2 != None:
                        leftClick1=None
                        leftClick2=None
                    if whatToDraw == 2: ## wanted right click
                        completed = True
                else:
                    if leftClick1 != None or leftClick2 != None:
                        leftClick1=None
                        leftClick2=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit("Bye!")
    screen.fill((0,255,0)) ## clear screen to background color
    f = pygame.font.SysFont("arial bold",45)
    s = "Great!"
    d = f.size(s)
    label = f.render(s, 1, (255,255,0))
    screen.blit(label, (width/2 - d[0]/2,height/2 - d[1]/2))
    pygame.display.update()
    pygame.time.delay(1000)
    

    
