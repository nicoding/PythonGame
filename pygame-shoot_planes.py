# -*- coding: utf-8 -*-
import pygame
from sys import exit
import random

class Plane:
    def restart(self):
        self.x = 200
        self.y = 600
        
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('./img/plane.jpg').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x-= self.image.get_width() / 2
        y-= self.image.get_height() / 2
        self.x = x
        self.y = y

class Bullet:
    def __init__(self):
        #初始化成员变量，x，y，image
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('./img/bullet.png').convert_alpha()
        self.active=False

    def move(self):
        if self.active:
            self.y-=1
        if self.y < 0:
            self.active=False
    def restart(self):
        #处理子弹的运动
        mouseX,mouseY= pygame.mouse.get_pos()        
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        self.active=True
       


class Enemy:
    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('./img/enemy.png').convert_alpha()

    def move(self):
        if self.y < 500:
            self.y += self.speed
        else:
            self.restart()

def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False  
        return True
    return False  

def checkCrash(enemy, plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((450, 500), 0, 32)
pygame.display.set_caption("Hello, World!")
background = pygame.image.load('./img/shoot_the_plane_bg.jpg').convert()

plane=Plane()
bullets=[]
for i in range(5):
    bullets.append(Bullet())
count_b=len(bullets)
index_b=0
interval_b=0

enemies = []
for i in range(5):
    enemies.append(Enemy())
    
gameover = False
score =0
font = pygame.font.Font(None, 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameover and event.type == pygame.MOUSEBUTTONUP:
#重置游戏
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    screen.blit(background, (0,0))
    interval_b-=1
    if interval_b < 0:
        bullets[index_b].restart()
        #重置间隔时间
        interval_b = 100
        #子弹序号周期性递增
        index_b = (index_b + 1) % count_b
    #判断每个子弹的状态
    for b in bullets:
        #处于激活状态的子弹，移动位置并绘制
        if b.active:
            for e in enemies:
                if checkHit(e, b):
                    score+=100
            b.move()
            screen.blit(b.image, (b.x, b.y))
    #把子弹画到屏幕上
    if not gameover:
        for e in enemies:
            if checkCrash(e, plane):
                gameover = True
            e.move()
            screen.blit(e.image, (e.x, e.y))
        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))
        text = font.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))
    else:
        text = font.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (190, 400))
    pygame.display.update()
