#!/usr/bin/python

## python script for a simple game
## where the person has to click on a round circle
## when they do their score goes up
## every n points the speed of movement increases

import pygame
import sys
import math
import random
import time

timeAllowed=10 ## seconds
level=1
width=640
height=480
initialRadius=20
radius = initialRadius
thickness = 0 ## fills if thickness is zero
color = ( 255, 0, 0 )
startx = int(round(width / 2))
starty = int(round(height / 2))
score = 0
win_points = 1
step = 5        # how many points before we change speed
speed = 1        # how fast do we move
direction_x = random.choice([-1,1])
direction_y = random.choice([-1,1])
initialSleep=50000
sleep=initialSleep
cnt=0
startTime=time.clock()
state=True

COLORS = [(139, 0, 0), 
          (0, 100, 0),
          (0, 0, 139)]


## initalise location
x = startx
y = starty

def random_color():
    return random.choice(COLORS)


def onClick( pos, x, y, radius ):
    "This function detects in pos is in the circle (x,y,r)"
    d = pow(radius,2)
    n = math.pow(pos[0] - x,2) + math.pow(pos[1] - y,2)
    if n <= 0:
        return False
    if n >= 0 and n <= d:
        return True
    return False
    

def draw( screen, color, x, y, radius, thickness, score, level, timeLeft ):
    screen.fill((255,255,255)) ## clear screen to background color
    ## draw shapes
    pygame.draw.circle( screen, color, (x,y), radius, thickness )
    ## display score text using a given font
    f = pygame.font.SysFont("monospace",15)
    label = f.render("Level: "+str(level)+" Score: "+str(score)+" Time Left: "+str(timeLeft), 1, (0,0,0))
    screen.blit(label, (10,10))
    pygame.display.update()


    
pygame.init()

## screen setup
## (0,0) is upper left hand corner
screen = pygame.display.set_mode( (width, height), 0, 32 )

## draw starting position
timeLeft = timeAllowed - int(round(time.clock() - startTime))
draw( screen, color, x, y, radius, thickness, score, level, timeLeft )

## enter our event loop looking for the user to click the circle
while True:
    if state == True:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                hit = onClick( pos, x, y, radius )
                if hit == True:
                    print("HIT!")
                    score += win_points
                    color = random_color()
                    direction_x = random.choice([-1,1])
                    direction_y = random.choice([-1,1])
                    x = random.randint(radius,width-radius)
                    y = random.randint(radius,height-radius)
                    radius=random.randint(20,50)
                    if score % step == 0:
                        sleep = int(round(sleep * 0.8))
                        level = level + 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit("Bye!")
                if event.key == pygame.K_n:
                    ## quickly skip to next level
                    sleep = int(round(sleep * 0.8))
                    level = level + 1
        
        if cnt % sleep == 0:                
            x = x + ( speed * direction_x )
            y = y + ( speed * direction_y )
            if x > width-radius:
                direction_x = -1 * direction_x
            if x < radius:
                direction_x = -1 * direction_x
            if y > height-radius:
                direction_y = -1 * direction_y
            if y < radius:
                direction_y = -1 * direction_y

            timeLeft = timeAllowed - int(round(time.clock() - startTime))
            draw( screen, color, x, y, radius, thickness, score, level, timeLeft )
        cnt=cnt+1

        if time.clock() - startTime > timeAllowed:
            screen.fill((0,255,0)) ## clear screen to background color
            f = pygame.font.SysFont("arial bold",45)
            s = "Well Done! You scored "+str(score)
            d = f.size(s)
            label = f.render(s, 1, (255,255,0))
            screen.blit(label, (width/2 - d[0]/2,height/2 - d[1]/2))
            pygame.display.update()
            state=False
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

