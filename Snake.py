import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500 #width of the board
    def __init__(self, start, dirnx=1, color=(5,56,140)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))  

        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0    #(-1 . 0 . 1)
        self.dirnx = 1    #(-1 . 0 . 1)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for index, c_ube in enumerate(self.body):  #parcurg fiecare element din corpul sarpelui
            position = c_ube.pos[:]    #retin pozitia fiecarui element pe grid

            if position in self.turns: #daca pozitia este una in care am modificat directia
                turn = self.turns[position] #retin directia de deplasare
                c_ube.move(turn[0], turn[1]) #mut elemtul in acea directie
                if index == len(self.body) - 1: #daca este ultimul elemnt din corp
                    self.turns.pop(position) #scot schimbarea de directie din calcul
            else:                                                                                           #Daca nu se schimba directia de deplasare 
                if c_ube.dirnx == -1 and c_ube.pos[0] <= 0: c_ube.pos = (c_ube.rows-1, c_ube.pos[1])        #st Daca sarpele ajunge la marginea ecranului il fac sa apara pe partea cealalata
                elif c_ube.dirnx == 1 and c_ube.pos[0] >= c_ube.rows-1: c_ube.pos = (0, c_ube.pos[1])       #dr
                elif c_ube.dirny == 1 and c_ube.pos[1] >= c_ube.rows-1: c_ube.pos = (c_ube.pos[0], 0)       #jos
                elif c_ube.dirny == -1 and c_ube.pos[1] <= 0: c_ube.pos = (c_ube.pos[0], c_ube.rows - 1)    #sus

                else: c_ube.move(c_ube.dirnx, c_ube.dirny) #daca nu am ajuns la margine doar mut elementul in directia curenta

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))  #verif directia de deplasare si pun cubul in partea opusa
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx #dau direcrtia cubului adaugat cu directia sarpelui
        self.body[-1].dirny = dy

    def draw(self, surface):
        for index, c_ube in enumerate(self.body):
            if index == 0:
                c_ube.draw(surface, True) #pentru primul elemet din lista vreau da desez ochii
            else:
                c_ube.draw(surface) #altfel desenez numai elelementul

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) 
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: # verific daca pozitia este ocupata de sarpe
            continue
        else:
            break

    return (x,y)
            

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    pygame.init()
    win = pygame.display.set_mode((width, width))
    s = snake((5,56,140), (10,10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(120)
        clock.tick(10)              #viteza jocului
        s.move()
        if s.body[0].pos == snack.pos: # verific daca pozitia capului sarpelui coincide cu pozitia marului 
            s.addCube() #daca da mai adug un element la sarpe   
            snack = cube(randomSnack(rows, s), color=(0, 255, 0)) # generez alt mar
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])): #verific daca se suprapun pozitile corpului
                print('Score: ', len(s.body)) #afisez scorul   
                message_box('You lost!', 'Play again') 
                s.reset((10, 10))
                break
        redrawWindow(win)

main()
