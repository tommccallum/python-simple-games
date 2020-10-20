## little game where random letters in words
## are greyed out and the child has to
## write in the correct letter
## easiest levels are only lowercase
## harder letters use capitals 

import sys
import pygame
import random

score=0
level=0
width=640
height=480
lettersToGreyOutCount=1
greyed=[]       ## array with 1 where the letter is greyed out, 2 for leave out
letterAction=1  ## greyout  = 1 , leave out = 2
letterSpacing=10
wordList = []
fontsize=200 ## largest font size
useCapitals=True
lastWordFileLoaded=0
exitButton=[]   ## exit button rectangle bounds



def readWordFile(letterCount):
    filename=str(letterCount)+"_letter.txt"
    with open(filename) as f:
        content = f.readlines()
    content = [ x.strip('\n') for x in content ]
    return content

def draw( screen, word, greyedOut, score, level ):
    screen.fill((255,255,255)) ## clear screen to background color (white)
    ## display score text using a given font
    f = pygame.font.SysFont("monospace",15)
    label = f.render("Level: "+str(level)+" Score: "+str(score), 1, (0,0,0))
    screen.blit(label, (10,10))
    ## display word
    drawWord(screen, word, greyedOut )
    drawButtons(screen)
    pygame.display.update()

## check if all letters are showing
def checkToSeeIfCompleted(greyed):
    return all([ v==0 for v in greyed])

## yuck function which takes to a new level
### sets up our new word to look for
def nextLevel():
    global wordList
    global word
    global greyed
    global lettersToGreyOutCount
    global level
    global letterAction
    global lastWordFileLoaded
    global useCapitals
    
    level = level + 1
    if level == 1:
        ## read in 1-3 letter words
        wordList = wordList + readWordFile(1)
        wordList = wordList + readWordFile(2)
        wordList = wordList + readWordFile(3)
        lastWordFileLoaded = 3
    elif level % 10 == 0 and lastWordFileLoaded < 10:
        lastWordFileLoaded = lastWordFileLoaded + 1
        print("Reading file "+str(lastWordFileLoaded))
        wordList = wordList + readWordFile(lastWordFileLoaded)

    if level % 10 == 0:
        lettersToGreyOutCount = lettersToGreyOutCount + 1

    if level > 30 and level < 60:
        useCapitals = False

    if level >= 60:
        useCapitals = True

    ## after 60 then we random choose what they have to recognize
    if level >= 60:
        useCapitals = random.choice([True,False])
    
    word = random.choice(wordList)
    if useCapitals:
        word = word.upper()
    else:
        word = word.lower()
        
    greyed = [0] * len(word)
    for ii in range(0,min(len(word),lettersToGreyOutCount)):
        ch=random.randint(0,len(word)-1)
        greyed[ch]=letterAction

## check to see if the key pressed was in word
## only changes the first UNCHANGED matching character
## returns -1 if not found, or the character matched if True
def checkToSeeIfKeyIsInWord( word, key ):
    global greyed
    for ii in range(0,len(word)):
        if greyed[ii] > 0:
            if useCapitals:
                word = word.lower()
            #if pygame.key.get_mods() & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
            #    key = ord(chr(key).upper())
            if ord(word[ii]) == key:
                greyed[ii] = 0
                return ii
    return -1

def incrementScore( amt ):
    global score
    score = score + amt

## quick and nasty resize so that word fits on, starts at the maximum size we want
## a short word to appear at
## returns 12 as a minimum
def fitWord( fontname, word, fontsize, availWidth ):
    f = pygame.font.SysFont(fontname, fontsize)
    while f.size(word)[0] > availWidth:
        fontsize = int(round(fontsize * 0.9))+1
        if fontsize < 12:
            fontsize = 12
            break
        f = pygame.font.SysFont(fontname,fontsize)
    return fontsize

## draw the word in the middle of the window
def drawWord(screen, word, greyedOut):
    global width
    global height
    global letterSpacing
    global fontsize
    letterCount = len(greyedOut)
    ## 1 letter word has 2 spacing
    ## 2 letter word as 3 spacing etc
    availWidth = width - ((letterCount+1) * letterSpacing)
    fittedFontSize = fitWord( "monospace", word, fontsize, availWidth )
    f = pygame.font.SysFont("monospace",fittedFontSize)
    w = f.size(word)
    wx = w[0] + (letterSpacing * letterCount)
    x = (width / 2) - (wx/2)
    y = (height / 2) - (w[1]/2)
    for ii in range(0,len(greyedOut)):
        ## set colour for letter
        if greyedOut[ii] == 0:
            col = (0,0,0)
        elif greyedOut[ii] == 1:
            col = (150,150,150)
        elif greyOut[ii] == 2:
            col = (255,255,255)
        
        label = f.render(word[ii], 1, col)
        screen.blit(label, (x,y))
        x = x + f.size(word[ii])[0] + letterSpacing


## draw a button to quit the game, or to start again
def drawButtons(screen):
    global width
    global height
    global exitButton
    x = int(round(0.75 * width))
    y = int(round(0.75 * height))
    pygame.draw.rect( screen, (150,150,150), (x,y,100,50), 0)
    f = pygame.font.SysFont("monospace",16)
    label = f.render("Exit", 1, (0,0,0))
    screen.blit(label, (x+50-f.size("Exit")[0]/2,y+25-f.size("Exit")[1]/2))
    exitButton=(x,y,100,50)

## skip to level
#for ii in range(1,9):
#    wordList = wordList + readWordFile(ii)
#level=80

pygame.init()

## screen setup
## (0,0) is upper left hand corner
screen = pygame.display.set_mode( (width, height), 0, 32 )


nextLevel()
draw( screen, word, greyed, score, level )
mode=0

## game loop
while True:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pos[0] >= exitButton[0] and pos[0] <= exitButton[0] + exitButton[2]:
                if pos[1] >= exitButton[1] and pos[1] <= exitButton[1] + exitButton[3]:
                    pygame.quit()
                    sys.exit("Bye!")
        if event.type == pygame.KEYDOWN:
            if checkToSeeIfKeyIsInWord( word, event.key ) > -1:
                incrementScore( 1 )
            if checkToSeeIfCompleted(greyed):
                nextLevel()
            draw( screen, word, greyed, score, level )
                    
