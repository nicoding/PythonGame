# -*- coding: cp936 -*-
import pygame
from pygame.locals import *

from sys import exit

class Tortoise:
    def __init__(self,num):
        self.x = 250
        self.y = 100 -10 *num
        self.zoomdx = (0.2*num+0.2)*0.5
        self.zoomdy = (0.05*num+0.05)*0.5
        #0:big   1:small   -1:end
        self.zoomFlag = 1
        #0: not start    1: moving   -1:end
        self.moveFlag = 0
        self.visible = False
        self.width = 400
        self.height = 100
        self.maxWidth = self.width
        self.maxHeight = self.height
        self.minWidth = self.maxWidth/4
        self.minHeight = self.maxHeight/4
        self.rec = [self.x - self.width/2, self.y - self.height/2, self.width, self.height]
        self.col = [(num%3==0)*255,(num%3==1)*255,(num%3==2)*255]

    def move(self, button):
        if self.moveFlag == 1:
            self.rec[1] += 3
            if self.rec[1]+self.height > button:
                self.rec[1] = button-self.height
                self.moveFlag = -1

    def zoom(self):
        if self.zoomFlag == 0:
            self.height += self.zoomdy
            self.width += self.zoomdx
            if self.height >= self.maxHeight:
                self.height = self.maxHeight
                self.width = self.maxWidth
                self.zoomFlag = 1
        if self.zoomFlag == 1:
            self.height -= self.zoomdy
            self.width -= self.zoomdx
            if self.height <= self.minHeight:
                self.height = self.minHeight
                self.width = self.minWidth
                self.zoomFlag = 0
        self.rec = [self.x - self.width/2, self.y - self.height/2, self.width, self.height]
        
pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)

pygame.display.set_caption("Hello, World!")

#surface
#bland_surface = pygame.Surface((100,100))
sur = pygame.surface.Surface((200, 200))

f_score = file('./res/scoreForWugui.txt')
scoreLines = f_score.readlines()
f_score.close()

playersInform = {}

for line in scoreLines:
    data =  line.split('\t') 
    playersInform[data[0]] = [data[1],data[2].strip('\n')]

background = pygame.image.load('./img/white.png').convert()
once_more = pygame.image.load("./img/once_more.png").convert()
scoreInformPic = pygame.image.load('./img/scoreInform.png').convert()
wYNPic = pygame.image.load('./img/wYN.png').convert()
newGamePic = pygame.image.load('./img/newGame.png').convert()
goBackPic = pygame.image.load('./img/goBack.png').convert()

#parameter
result="playing"
Fullscreen = False
gameStart = True
scoreInformRect = Rect(150,250,200,50)
goBackRect = Rect((150,400),(200,50))
newGameRect = Rect(150,150,200,50)
onceMoreRect = Rect(200,200,100,100)
font = pygame.font.Font(None, 32)
showModes = {'menuStart', 'menuScore', 'gaming', 'menuEnd'}
mode = 'menuStart'

#num of tortoise
button = 500
widthRange = 500
num = 5
t=[]
for i in range(num):
    t.append(Tortoise(i))
tIndex = 0
t[0].visible = True


while True:
    #handle the event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if mode == "gaming":
                if result == "Failed" or result =="You win~":
                    if onceMoreRect.collidepoint((x,y))==True:
                        for i in range(num):
                            t[i]=Tortoise(i)
                        tIndex = 0
                        result = "playing"
                        button = 500
                        widthRange = 500
                        t[0].visible = True
                    elif goBackRect.collidepoint((x,y))==True:
                        for i in range(num):
                            t[i]=Tortoise(i)
                        tIndex = 0
                        result = "playing"
                        button = 500
                        widthRange = 500
                        t[0].visible = True
                        mode = 'menuStart'
                else:
                    t[tIndex].zoomFlag = -1
                    t[tIndex].moveFlag = 1
            elif mode == 'menuStart':
                if scoreInformRect.collidepoint((x,y))==True:
                    mode = 'menuScore'
                if newGameRect.collidepoint((x,y))==True:
                    mode = 'gaming'
            elif mode == 'menuScore':
                if goBackRect.collidepoint((x,y))==True:
                    mode = 'menuStart'


        if event.type == KEYDOWN:
            if mode == "gaming":
                if event.key == K_SPACE:
                    t[tIndex].zoomFlag = -1 
                    t[tIndex].moveFlag = 1
                if event.key == K_f:#press 'f': fullscreen
                    Fullscreen = not Fullscreen
                    if Fullscreen:
                        screen = pygame.display.set_mode((500, 500), FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode((500, 500), 0, 32)
        
    
    #draw the background
    screen.blit(background, (0,0))
    
    #game flow
    if mode == 'menuStart':        
        screen.blit(newGamePic,newGameRect[0:2])
        screen.blit(scoreInformPic,scoreInformRect[0:2])
    elif mode == 'menuScore':
        text1 = font.render("Name", 1, (0, 0, 0))
        screen.blit(text1, (75,50))
        text1 = font.render("Count", 1, (0, 0, 0))
        screen.blit(text1, (200,50))
        text1 = font.render("Score", 1, (0, 0, 0))
        screen.blit(text1, (320,50))
        i = 1
        for playerName in playersInform:
            playerInform = playersInform[playerName]
            text1 = font.render(playerName, 1, (0, 0, 0))
            screen.blit(text1, (75,50+i*50))
            text1 = font.render(playerInform[0], 1, (0, 0, 0))
            screen.blit(text1, (200,50+i*50))
            text1 = font.render(playerInform[1], 1, (0, 0, 0))
            screen.blit(text1, (320,50+i*50))
            i += 1
        screen.blit(goBackPic,goBackRect[0:2])
    elif mode == 'gaming':
        text2 = font.render("result:" +result, 1, (0, 0, 0))

        screen.blit(text2, (0, 20))

        if t[tIndex].zoomFlag !=-1:
            t[tIndex].zoom()

        if t[tIndex].moveFlag == 1:
            t[tIndex].move(button)
        elif t[tIndex].moveFlag == -1:
            button -= t[tIndex].height
            if widthRange <= t[tIndex].width:
                result = "Failed"
            else:
                if tIndex ==4:
                    result = "You win~"
                else:
                    widthRange = t[tIndex].width
                    tIndex +=1
                    tIndex = tIndex %5
                    t[tIndex].visible = True

        for i in range(num):
            if t[i].visible == True:
                pygame.draw.rect(screen,t[i].col,t[i].rec)

        if result == "Failed" or result =="You win~":
            screen.blit(once_more,onceMoreRect[0:2])
            screen.blit(goBackPic,goBackRect[0:2])
    else:
        screen.blit(newGamePic,(150,150))
        screen.blit(scoreInformPic,(150,250))
    
    
    pygame.display.update()
    
