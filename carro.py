import pygame
from pygame.locals import *
from cmath import *
import math
import sys
import time

#Inicialização de todos os módulos
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.music.load('tokyo.wav')
pygame.mixer.music.play(-1)
pygame.font.init()
my_font = pygame.font.get_default_font()
myfont = pygame.font.Font(my_font,60)
ALT = 900
LARG = 1800
FPS = 60

screen = pygame.display.set_mode((LARG,ALT))



def move():
	global x, y, curva, acelx, acely, momento_x, momento_y, curva_drift
	keys = pygame.key.get_pressed()
	tmp = math.radians(curva_drift)

	velx = acelx * math.cos(tmp)
	x += velx
	vely = acelx * math.sin(tmp)
	vely *= -1
	y += vely

def crossSreen():
	global x, y
	if x>LARG :
		x = LARG
	if x<0:
		x = 0
	if y>ALT:
		y = ALT
	if y<0:
		y = 0

def drawScreen():
	global x, y, velx, vely
	screen.fill((255,255,255))
	#Desenha um círculo
	#pygame.draw.circle(screen, (255, 0, 255), (x, y), 15)
	ufo = pygame.image.load("carro.png")
	rect = ufo.get_rect()
	ufo = pygame.transform.rotate(rect, curva-90)
	screen.blit(ufo, (x,y))
	
	#Atualiza tela
	pygame.display.flip()

def drawScreen2(pista):
	global x, y, velx, vely, rect, momento_x, momento_y, myfont, laps, checks
	screen.fill((255, 255, 255))

	new_image = pygame.transform.rotate(carro2, curva - 90)
	rect = new_image.get_rect()
	rect.center = (x, y)
	screen.blit(pistas[pista], (0, 0))
	screen.blit(new_image, rect)
	text = "Checkpoints: " + str(checks)
	text2 = "Laps: " + str(laps) + "/5"
	text3 = "Time: " + str(round((time.time() - tempo), 2))
	textsurface = myfont.render(text, False, (0, 0, 0))
	textsurface2 = myfont.render(text2, False, (0, 0, 0))
	textsurface3 = myfont.render(text3, False, (0, 0, 0))

	if(sel_pista == 0):
		screen.blit(textsurface, (380, 410))
		screen.blit(textsurface2, (380, 460))
		screen.blit(textsurface3, (380, 510))
	if (sel_pista == 1):
		screen.blit(textsurface, (285, 410))
		screen.blit(textsurface2, (285, 460))
		screen.blit(textsurface3, (285, 510))
	if (sel_pista == 2):
		screen.blit(textsurface, (622, 590))
		screen.blit(textsurface2, (622, 640))
		screen.blit(textsurface3, (622, 690))

	pygame.display.flip()

	if (laps == 5):
		pygame.time.wait(2000)
		reset()

def reset():
	global x,y,velx,vely,curva,acelx,acely, track_check, track2_check, laps, checks, tempo, curva_drift, track3_check
	x = 800
	y = 125
	velx = 0
	vely = 0
	curva = 0
	curva_drift = 0
	acelx = 0
	acely = 0
	laps = 0
	checks = 0
	tempo = time.time()
	for i in track_check:
		i.reset()
	for i in track2_check:
		i.reset()
	for i in track3_check:
		i.reset()

def handleInput():
	global x, y, velx, vely, curva, acelx, acely, count, curva_drift, DRIFT, DRIFT_2, sel_pista

	events = pygame.event.get()

	for e in events:
		if e.type == QUIT:
			sys.exit(1)

	keys = pygame.key.get_pressed()
	#for e in events:
	if keys[K_SPACE]:
		if (acelx > 0):
			acelx -= 0.25
	else:
		if(acelx < 0):
			acelx += 0.1

	if keys[K_w]:
		acelx+=0.5
	else:
		if(acelx > 0):
			acelx -= 0.1

	if keys[K_s]:
		if(acelx < 0):
			acelx -= 0.3
	else:
		if(acelx < 0):
			acelx += 0.1

	if keys[K_a]:
		curva+=6
		if (acelx > 0):
			curva_drift += DRIFT
		if (acelx > 0):
			acelx -= 0.1
	if keys[K_d]:
		curva-=6
		if (acelx > 0):
			curva_drift -= DRIFT
		if (acelx > 0):
			acelx -= 0.1

	if keys[K_RETURN]:
		reset()

	if keys[K_1]:
		pygame.event.clear()
		sel_pista = 1
		pygame.time.wait(100)
		reset()

	if keys[K_2]:
		pygame.event.clear()
		sel_pista = 0
		pygame.time.wait(100)
		reset()

	if keys[K_3]:
		pygame.event.clear()
		sel_pista = 2
		pygame.time.wait(100)
		reset()


	if(curva_drift > curva):
		curva_drift -= DRIFT_2
		if (curva_drift - curva > 50):
			curva_drift = curva + 50

	if(curva_drift < curva):
		curva_drift += DRIFT_2
		if(curva - curva_drift > 50):
			curva_drift = curva - 50

	if (acelx == 0):
		curva_drift = curva

	if(acelx > 15):
		acelx = 15
	if (acelx < -5):
		acelx =-5
	dif = curva - curva_drift

	if keys[K_c]:
		print("x")
		print (x)
		print("y")
		print(y)

class Checkpoint:
	def __init__(self, x_1, y_1, x_2, y_2, st):
		self.x1 = x_1
		self.y1 = y_1
		self.x2 = x_2
		self.y2 = y_2
		self.ok = 0
		self.start = st
	def distancia(self, x, y):
		if(x > self.x1 and x < self.x2):
			if (y > self.y1 and y < self.y2):
				print("############bingo################")
				self.ok = 1
	def ok_check(self):
		return self.ok
	def start_check(self):
		return self.start
	def reset(self):
		self.ok = 0


def checkpoints(pista):
	global track_check, x, y, laps, checks, tempo, tempo_f, track2_check, track3_check
	if pista == 0:
		total = len(track_check)
		for i in track_check:
			if(not i.ok_check() and not i.start_check()):
				i.distancia(x, y)
				if(i.ok_check()):
					checks += 1
			if(i.start_check() and checks == (total - 1)):
				i.distancia(x, y)
				if (i.ok_check()):
					checks += 1
		if (checks == total):
			laps += 1
			checks = 0
			for i in track_check:
				i.reset()

	if pista == 1:
		total = len(track2_check)
		for i in track2_check:
			if(not i.ok_check() and not i.start_check()):
				i.distancia(x, y)
				if(i.ok_check()):
					checks += 1
			if(i.start_check() and checks == (total - 1)):
				i.distancia(x, y)
				if (i.ok_check()):
					checks += 1
		if (checks == total):
			laps += 1
			checks = 0
			for i in track2_check:
				i.reset()

	if pista == 2:
		total = len(track3_check)
		for i in track3_check:
			if(not i.ok_check() and not i.start_check()):
				i.distancia(x, y)
				if(i.ok_check()):
					checks += 1
			if(i.start_check() and checks == (total - 1)):
				i.distancia(x, y)
				if (i.ok_check()):
					checks += 1
		if (checks == total):
			laps += 1
			checks = 0
			for i in track3_check:
				i.reset()






track_check = []

t_check_1 = Checkpoint(1460,11,1500,265,0)
t_check_2 = Checkpoint(1440,340,1480,551,0)
t_check_3 = Checkpoint(1110,270,1150,475,0)
t_check_4 = Checkpoint(1110,475,1150,665,0)
t_check_5 = Checkpoint(1285,504,1330,700,0)
t_check_6 = Checkpoint(1285,710,1330,900,0)
t_check_7 = Checkpoint(485,675,530,900,0)
t_check_8 = Checkpoint(86,450,275,500,0)
t_check_9 = Checkpoint(940,10,980,200,1)


track_check.append(t_check_1)
track_check.append(t_check_2)
track_check.append(t_check_3)
track_check.append(t_check_4)
track_check.append(t_check_5)
track_check.append(t_check_6)
track_check.append(t_check_7)
track_check.append(t_check_8)
track_check.append(t_check_9)

track2_check = []

t2_check_1 = Checkpoint(940,10,980,200,1)
t2_check_2 = Checkpoint(1440,11,1480,265,0)
t2_check_3 = Checkpoint(1450,350,1490,543,0)
t2_check_4 = Checkpoint(1100,300,1140,480,0)
t2_check_5 = Checkpoint(860,515,1050,600,0)
t2_check_6 = Checkpoint(670,725,710,900,0)
t2_check_7 = Checkpoint(320,700,360,900,0)
t2_check_8 = Checkpoint(0,450,190,600,0)
t2_check_9 = Checkpoint(225,20,350,240,0)

track2_check.append(t2_check_1)
track2_check.append(t2_check_2)
track2_check.append(t2_check_3)
track2_check.append(t2_check_4)
track2_check.append(t2_check_5)
track2_check.append(t2_check_6)
track2_check.append(t2_check_7)
track2_check.append(t2_check_8)
track2_check.append(t2_check_9)

track3_check = []

t3_check_1 = Checkpoint(940,10,980,200,1)
t3_check_2 = Checkpoint(1395,0,1450,240,0)
t3_check_3 = Checkpoint(1530,290,1725,363,0)
t3_check_4 = Checkpoint(1520,630,1750,680,0)
t3_check_5 = Checkpoint(1420,700,1490,800,0)
t3_check_6 = Checkpoint(1180,620,1390,690,0)
t3_check_7 = Checkpoint(1095,250,1181,465,0)
t3_check_8 = Checkpoint(530,260,620,460,0)
t3_check_9 = Checkpoint(320,450,540,510,0)
t3_check_10 = Checkpoint(330,630,510,675,0)
t3_check_11 = Checkpoint(235,700,280,900,0)
t3_check_12 = Checkpoint(0,620,185,666,0)
t3_check_13 = Checkpoint(0,285,200,365,0)
t3_check_14 = Checkpoint(250,0,320,255,0)

track3_check.append(t3_check_1)
track3_check.append(t3_check_2)
track3_check.append(t3_check_3)
track3_check.append(t3_check_4)
track3_check.append(t3_check_5)
track3_check.append(t3_check_6)
track3_check.append(t3_check_7)
track3_check.append(t3_check_8)
track3_check.append(t3_check_9)
track3_check.append(t3_check_10)
track3_check.append(t3_check_11)
track3_check.append(t3_check_12)
track3_check.append(t3_check_13)
track3_check.append(t3_check_14)


DRIFT = 3
DRIFT_2 = 1
laps = 0
checks = 0
count = 0
curva_drift = 0
x = 800
y = 125
velx=0
vely=0
curva=0
acelx = 0
acely = 0
momento_x = 0
momento_y = 0
clock = pygame.time.Clock()
carro = pygame.image.load("carro35.png")
track = pygame.image.load("track.png")
track2 = pygame.image.load("track2.png")
track3 = pygame.image.load("track3.png")
pistas = [track, track2, track3]
carro2 = carro.copy()
rect = carro2.get_rect()
rect.center = (100, 100)
sel_pista = 1
tempo = 0
tempo_f = 0

reset()

while True:
	clock.tick(FPS)
	handleInput()
	drawScreen2(sel_pista)
	move()
	checkpoints(sel_pista)
	crossSreen()

	#clock.tick(50)
