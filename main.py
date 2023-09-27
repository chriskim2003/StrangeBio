import sys
import pygame
from pygame.locals import *
import random
import math

FPS = 60
SIZE = 1000

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

TITLE = "Strange Bio   FPS:"

class Object:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velx = 0
        self.vely = 0
    def getPos(self)->tuple:
        return (self.x, self.y)
    def getColor(self)->tuple:
        return self.color
    def setPos(self, x, y):
        self.x = x
        self.y = y
    def getVel(self)->list:
        return (self.velx, self.vely)
    def setVel(self, velx, vely):
        self.velx = velx
        self.vely = vely

def main(setting):
    pygame.init()

    CLOCK = pygame.time.Clock()

    GameDisplay = pygame.display.set_mode((SIZE, SIZE))
    GameDisplay.fill(BLACK)
    pygame.display.set_caption(TITLE)

    setting.create()

    font = pygame.font.Font(None, 30)
    start = font.render("press a to start", True, WHITE)

    up = False
    flag = False
    
    while True:
        GameDisplay.fill(BLACK)

        if up:
            setting.update(GameDisplay)
        else:
            GameDisplay.blit(start, [SIZE/2, SIZE/2])
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                button = event.unicode
                flag=True
            if event.type == KEYUP:
                flag=False

        if flag==True:
            if button == 'a':
                up = True
                
        CLOCK.tick(FPS)

        pygame.display.flip()

def rule(objects, targets, force):
    for obj in objects:
            pos = obj.getPos()
            vel = obj.getVel()
            newpos = []

            fx = 0
            fy = 0
            for target in targets:
                tpos = target.getPos()
                dx = pos[0]-tpos[0]
                dy = pos[1]-tpos[1]
                d = math.sqrt(dx**2 + dy**2)
                if(d>0 and d<50):
                    F = force * 1/d
                    fx += (F * dx)
                    fy += (F * dy)
            vel = ((vel[0]+fx)*0.5, (vel[1]+fy)*0.5)

            
            if(0 > pos[0]+vel[0] or pos[0]+vel[0] > SIZE):
                newpos.append(pos[0]-vel[0])
                vel = (-vel[0], vel[1])
            else:
                newpos.append(pos[0]+vel[0])
            if(0 > pos[1]+vel[1] or pos[1]+vel[1] > SIZE):
                newpos.append(pos[1]-vel[1])
                vel = (vel[0], -vel[1])
            else:
                newpos.append(pos[1]+vel[1])

            obj.setPos(newpos[0], newpos[1])
            obj.setVel(vel[0], vel[1])

def create(color, li, num):
    for i in range(num):
        x = random.random() * SIZE
        y = random.random() * SIZE
        obj = Object(x, y, color)
        li.append(obj)

def draw(display, color, li):
    for obj in li:
        pygame.draw.rect(display, color, list(obj.getPos()) + [3, 3])


#this is example of red head, green wing stuff
class Example1:
    def __init__(self):
        self.whites = []
        self.reds = []
        self.greens = []
    
    def create(self):
        #create objects
        create(RED, self.reds, 200)
        create(WHITE, self.whites, 1000)
        create(GREEN, self.greens, 800)
    def update(self, display):
        #update objects
        rule(self.greens, self.greens, -0.3)
        rule(self.greens, self.reds, -0.17)
        rule(self.greens, self.whites, 1)
        rule(self.reds, self.reds, 0.3)
        rule(self.reds, self.greens, -0.34)
        rule(self.whites, self.whites, 0.15)
        rule(self.whites, self.greens, -0.2)

        #draw objects
        draw(display, WHITE, self.whites)
        draw(display, RED, self.reds)
        draw(display, GREEN, self.greens)


#Another example of unstable green object
class Example2:
    def __init__(self):
        self.whites = []
        self.reds = []
        self.greens = []
        self.blues = []
    
    def create(self):
        #create objects
        create(RED, self.reds, 400)
        create(WHITE, self.whites, 400)
        create(GREEN, self.greens, 400)
        create(BLUE, self.blues, 400)
    def update(self, display):
        #update objects
        rule(self.greens, self.greens, -1)
        rule(self.greens, self.reds, -4)
        rule(self.greens, self.whites, -1)
        rule(self.greens, self.blues, -1)
        
        rule(self.reds, self.greens, 2)
        rule(self.reds, self.reds, 2)
        rule(self.reds, self.whites, -1)
        rule(self.reds, self.blues, -1)

        rule(self.whites, self.greens, -2)
        rule(self.whites, self.reds, 1)
        rule(self.whites, self.whites, -4)
        rule(self.whites, self.blues, -1)

        rule(self.blues, self.greens, 0.6)
        rule(self.blues, self.reds, -1)
        rule(self.blues, self.whites, 1)
        rule(self.blues, self.blues, 2)

        #draw objects
        draw(display, WHITE, self.whites)
        draw(display, RED, self.reds)
        draw(display, GREEN, self.greens)
        draw(display, BLUE, self.blues)
        
if __name__ == "__main__":
    main(Example1())
    #main(Example2())
