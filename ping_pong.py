import pygame
import time
import random
import sys


display_width = 800
display_height = 600


pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,100,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

bounce_sound = pygame.mixer.Sound("ballsound.wav")


clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Bing Ball')


ballImage = pygame.image.load('ball.png')
rodImage1 = pygame.image.load('rod.png')
rodImage2 = pygame.image.load('rod.png')

ballw = 25
ballh = 25
rodw = 150
rodh = 14

pause = False
score = 3
msc = 3
hsc = 0

def quitgame():
	pygame.quit()
	sys.exit()

def bounce_count():
	global score
	font = pygame.font.SysFont(None, 25)
	text = font.render("Life2: "+str(score), True, black)
	gameDisplay.blit(text,(0,0))

def missed_count():
	global msc
	font = pygame.font.SysFont(None, 25)
	text = font.render("Life1: "+str(msc), True, black)
	gameDisplay.blit(text,(0,30))

def high_score():
	global hsc
	font = pygame.font.SysFont(None, 25)
	text = font.render("Highest Score: "+str(hsc), True, black)
	gameDisplay.blit(text,(0,60))

def rod1(x,y):
	gameDisplay.blit(rodImage1, (x,y))

def ball(x,y):
	gameDisplay.blit(ballImage, (x,y))

def rod2(x,y):
	gameDisplay.blit(rodImage2,(x,y))

def text_objects(text, font):
	textSurface = font.render(text,True,black)
	return textSurface, textSurface.get_rect()

def messege_display(text,size,x,y):
	largeText = pygame.font.Font('freesansbold.ttf',size)
	TextSurf, TextRect = text_objects(text,largeText)
	TextRect.center = ((x),(y))
	gameDisplay.blit(TextSurf,TextRect)
	pygame.display.update()	
	if text == 'Player 1 missed' or text == 'Player 2 missed':
		pygame.display.update()
		time.sleep(2)
		gameloop()

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x< mouse[0] < x + w and y< mouse[1] < y+h:
		pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

	messege_display(msg,20,x+w/2,y+h/2)

def missed(text):
	
	#pygame.mixer.music.stop()
	messege_display(text,80,display_width/2,display_height/2)

def game_intro():

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()

		gameDisplay.fill(white)
		messege_display("Bing Ball",90,display_width/2,70)

		button('Play',150,450,100,50,green,bright_green,gameloop)
		button('Exit',550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

def unpause():
	#pygame.mixer.music.unpause()
	global pause
	pause = False

def paused():

	pygame.mixer.music.pause()

	messege_display("Paused",70,display_width/2,70)
	global pause
	while pause:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quitgame()

		button("Continue",150,450,100,50,green,bright_green,unpause)
		button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

def over(text):

	global score
	global msc
	msc = 3
	score = 3
	messege_display(text,70,display_width/2,70)
	global pause
	while pause:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quitgame()

		button("Try Again",150,450,100,50,green,bright_green,unpause)
		button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

def speed_up(a,b):
	if a<0:
		a-=.1
	else:
		a+=.1
	if b<0:
		b-=.1
	else:
		b+=.1
	return a,b

def gameloop():
	x = (display_width * .45)
	y = (display_height * .95)
	p = (display_width * .45)
	q = (display_height * .04)

	bx = random.randrange(1,display_width-1)
	by = 40
	global score
	global hsc
	global msc

	bx_change = 5
	by_change = 5

	x_change = 0
	p_change = 0
	global pause

	#print("in the loop")
	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if x>0:
						x_change = - 10
				elif event.key == pygame.K_RIGHT:
					if x<display_width-rodw:
						x_change = 10
				if event.key == pygame.K_a:
					if p>0:
						p_change = -10
				elif event.key == pygame.K_d:
					if p<display_width-rodw:
						p_change = 10
				if event.key == pygame.K_SPACE:
					pause = True
					paused()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					p_change = 0

		br = bx + ballw
		bd = by + ballh
		if br >= display_width or bx <= 0:
			bx_change = -bx_change

		gameDisplay.fill((14, 49, 104))
		x = x + x_change
		p = p + p_change

		if bx>=x-20 and br <= x + rodw+20:
			if y<= bd <= y + by_change:
				by_change = -by_change
				if -10<by_change<10:
					bx_change, by_change = speed_up(bx_change,by_change)
				pygame.mixer.Sound.play(bounce_sound)

		if br>=p-20 and bx<= p + rodw+20:
			if q+rodh+by_change<= by <= q+rodh:
				by_change = -by_change
				if -10<by_change<10:
					bx_change, by_change = speed_up(bx_change,by_change)
				pygame.mixer.Sound.play(bounce_sound)				

		bx = bx + bx_change
		by = by + by_change
		if x<=0 or x>=display_width-rodw:
			x_change = 0
		if p<=0 or p>=display_width-rodw:
			p_change = 0

		ball(bx,by)
		rod1(x,y)
		rod2(p,q)
		
		if bd >= display_height:
			msc-=1
			missed("Player 1 missed")
		elif bd <=0:
			score-=1
			missed("Player 2 missed")

		if msc == 0:
			pause = True
			over("Player 2 wins")
		if score == 0:
			pause = True
			over("Player 1 wins")

		bounce_count()
		missed_count()

		if hsc<score:
			hsc = score
		#high_score()

		pygame.display.update()
		clock.tick(60)
		


game_intro()
pygame.quit()
quit()

