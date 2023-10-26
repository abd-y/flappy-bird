import pygame
import os
import random
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
#Images
ICON = pygame.image.load(os.path.join("res", "icon.ico"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("res", "background.png")), (WIDTH, HEIGHT))
BASE = pygame.image.load(os.path.join("res", "base.png"))
STARTING_MESSAGE = pygame.image.load(os.path.join("res", "message.png"))
#Bird frames
BIRD_STAND = pygame.image.load(os.path.join("res", "bird1.png"))
BIRD_FLY1 = pygame.image.load(os.path.join("res", "bird2.png"))
BIRD_FLY2 = pygame.image.load(os.path.join("res", "bird3.png"))
#Pipes
UP_PIPE = pygame.image.load(os.path.join("res", "pipe-green.png"))
DOWN_PIPE = pygame.transform.flip(UP_PIPE, False, True)
#Game over frames
GAMEOVER0 = pygame.image.load(os.path.join("res", "gameover0.png"))
GAMEOVER1 = pygame.image.load(os.path.join("res", "gameover1.png"))
GAMEOVER2 = pygame.image.load(os.path.join("res", "gameover2.png"))
GAMEOVER3 = pygame.image.load(os.path.join("res", "gameover3.png"))
GAMEOVER4 = pygame.image.load(os.path.join("res", "gameover4.png"))
GAMEOVER5 = pygame.image.load(os.path.join("res", "gameover5.png"))
GAMEOVER6 = pygame.image.load(os.path.join("res", "gameover6.png"))
#Button frames
BUTTON0 = pygame.image.load(os.path.join("res", "button0.png"))
BUTTON1 = pygame.image.load(os.path.join("res", "button1.png"))
BUTTON2 = pygame.image.load(os.path.join("res", "button2.png"))
BUTTON3 = pygame.image.load(os.path.join("res", "button3.png"))
BUTTON4 = pygame.image.load(os.path.join("res", "button4.png"))
BUTTON5 = pygame.image.load(os.path.join("res", "button5.png"))
BUTTON6 = pygame.image.load(os.path.join("res", "button6.png"))
BUTTON7 = pygame.image.load(os.path.join("res", "button7.png"))
BUTTON8 = pygame.image.load(os.path.join("res", "button8.png"))
#Shadow buttons frame
SHADOWBUTTON0 = pygame.image.load(os.path.join("res", "mouseOnTheButton0.png"))
SHADOWBUTTON1 = pygame.image.load(os.path.join("res", "mouseOnTheButton1.png"))
#Sounds
gameover_sound = pygame.mixer.Sound(os.path.join("res", "shemal.mp3"))


class Bird:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.birds = {0:BIRD_FLY1, 1:BIRD_STAND, 2:BIRD_FLY2}
		self.frame = 0
		self.gravity = 0.35
		self.movement = 0
		self.angle = 0
		self.mask = pygame.mask.from_surface(self.birds[self.frame])

	def draw(self, bird, rotateup = False, rotatedown = False):
		if rotateup or rotatedown:
			win.blit(pygame.transform.rotate(self.birds[bird], self.angle), (self.x, self.y))
		elif not rotateup or not rotatedown:
			win.blit(self.birds[bird], (self.x, self.y))

	def jump(self):
		if self.y > 0:
			self.movement = 0
			self.movement -= 5
		if self.angle >= -15:
			self.angle += 40
		if self.angle < -15:
			self.angle += 80
		if self.angle >= 40:
			self.angle = 40

	def fall(self):
		if self.y <= 385:
			self.movement += self.gravity
			self.y += self.movement
		if self.y <= 385 + self.angle / 2:
			self.angle -= 2
		if self.angle <= -90:
			self.angle = -90

	def flying(self, frameSpeed, rotateup = False, rotatedown = False):
		self.draw(int(self.frame), rotateup, rotatedown)
		self.frame += frameSpeed
		if self.frame >= 3:
			self.frame = 0

	def get_width(self):
		return self.birds[int(self.frame)].get_width()

	def get_height(self):
		return self.birds[int(self.frame)].get_height()

class Pipe:
	def __init__(self, x, y, pipe):
		self.x = x
		self.y = y
		self.pipe = pipe
		self.pipe_mask = pygame.mask.from_surface(self.pipe)

	def draw_pipe(self):
		win.blit(self.pipe, (self.x, self.y))

	def move(self):
		self.x -= 4

	def stop(self):
		return self.draw_pipe()

class Floor:
	def __init__(self, x):
		self.x = x
	def draw(self):
		win.blit(BASE, (self.x, 410))

class Button:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.frame = 0
		self.frame1 = 0
		self.buttons = [BUTTON0, BUTTON1, BUTTON2, BUTTON3, BUTTON4, BUTTON5, BUTTON6, BUTTON7, BUTTON8]
		self.shadow_buttons = [SHADOWBUTTON0, SHADOWBUTTON1]

	def draw(self, buttons):
		win.blit(buttons, (self.x, self.y))

	def start_animation(self, frameSpeed):
		self.draw(self.buttons[int(self.frame)])
		if self.frame <= 8 :
			self.frame += frameSpeed

	def start_shadow_animation(self, frameSpeed):
		self.draw(self.shadow_buttons[int(self.frame1)])
		if self.frame1 <= 1:
			self.frame1 += frameSpeed

	def get_width(self):
		return self.buttons[int(self.frame)].get_width()

	def get_height(self):
		return self.buttons[int(self.frame)].get_height()

class GameOverImage:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.frame = 0
		self.images = [GAMEOVER0, GAMEOVER1, GAMEOVER2, GAMEOVER3, GAMEOVER4, GAMEOVER5, GAMEOVER6]

	def draw(self, img):
		win.blit(self.images[img], (self.x, self.y))

	def start_animation(self, frameSpeed):
		self.draw(int(self.frame))
		if self.frame <= 6:
			self.frame += frameSpeed

bird = Bird(WIDTH / 2 - BIRD_STAND.get_width() / 2 - 120, HEIGHT / 2 - BIRD_STAND.get_height() / 2 + 48)
pipes = []
floor = Floor(0)
gameOverImage = GameOverImage(WIDTH / 2 - GAMEOVER0.get_width() / 2, HEIGHT / 2 - GAMEOVER0.get_height() / 2 - 20)
button = Button(WIDTH / 2 - BUTTON0.get_width() / 2, HEIGHT / 2 - BUTTON0.get_height() / 2 + 50)
button_start_x_pos = WIDTH / 2 - button.get_width() / 2
button_start_y_pos = HEIGHT / 2 - button.get_height() / 2 + 50
button_end_x_pos = WIDTH / 2 - button.get_width() / 2 + button.get_width() - 3.5
button_end_y_pos = HEIGHT / 2 - button.get_height() / 2 + 50 + button.get_height() - 3.5
normal_font = pygame.font.Font(os.path.join("res", "04B_19.ttf"), 40)
shadow_font = pygame.font.Font(os.path.join("res", "04B_19.ttf"), 44)
score = 0
movement = 0
jump, fall = False, False
gameOver = False
mainMenu = True

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.pipe_mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def redraw():
	global jump
	global fall
	global gameOver
	global bird
	global pipes
	global pipe
	global button
	global button_start_x_pos
	global button_start_y_pos
	global button_end_x_pos
	global button_end_y_pos
	global score
	mouse_pos = pygame.mouse.get_pos()
	#Start drawing
	#Background
	win.blit(BG ,(0, 0))
	#Pipes
	if not mainMenu:
		for pipe in pipes:
			if not gameOver:
				pipe.draw_pipe()
				pipe.move()
				if pipe.x < -300 :
					pipes.remove(pipe)
			if collide(pipe, bird):
					gameOver = True
	if gameOver:
		for pipe in pipes:
			pipe.draw_pipe()
	#Floor
	floor.draw()
	#Bird
	if mainMenu:
		bird.flying(0.15, False, False)
	if jump:
		bird.jump()
		bird.flying(0.15, True, False)
		fall = True
		jump = False
		# shemalmaly sound pygame.mixer.Sound.play(gameover_sound)
	if fall:
		bird.fall()
		bird.flying(0.15, False, True)
		jump = False
		fall = True
	if bird.y >= 385 + bird.angle / 2:
		if bird.angle <= -55:
			bird.y = 385 - bird.angle / 2 - 60
		else:
			bird.y = 385 + bird.angle / 2
		bird.gravity = 0
		gameOver = True
	if bird.y <= 0:
		bird.y = 0
	#Main menu
	if mainMenu:
		score = 0
		win.blit(STARTING_MESSAGE, (WIDTH / 2 - STARTING_MESSAGE.get_width() / 2, HEIGHT / 2 - STARTING_MESSAGE.get_height() / 2))
	#Button
	if gameOver:
		gameOverImage.start_animation(0.4)
		button.start_animation(0.4)
		if button_start_x_pos <= mouse_pos[0] <= button_end_x_pos and button_start_y_pos <= mouse_pos[1] <= button_end_y_pos:
			button.start_shadow_animation(0.24)
		else:
			button.frame1 = 0
	#score
	shadow_score = shadow_font.render(f"{int(score / 2)}", True, (0, 0, 0))
	normal_score = normal_font.render(f"{int(score / 2)}", True, (255, 255, 255))
	win.blit(shadow_score, (WIDTH / 2 - shadow_score.get_width() / 2, 40))
	win.blit(normal_score, (WIDTH / 2 - normal_score.get_width() / 2, 40))
	for pipe in pipes:
		if pipe.x == 180 and not gameOver:
			score += 1

	pygame.display.update()

def restartGame():
	global bird
	global jump
	global fall
	global pipes
	global gameOverImage
	global button
	global gameOver
	global mainMenu
	bird = Bird(WIDTH / 2 - BIRD_STAND.get_width() / 2 - 120, HEIGHT / 2 - BIRD_STAND.get_height() / 2 + 48)
	gameOverImage = GameOverImage(WIDTH / 2 - GAMEOVER0.get_width() / 2, HEIGHT / 2 - GAMEOVER0.get_height() / 2 - 20)
	button = Button(WIDTH / 2 - BUTTON0.get_width() / 2, HEIGHT / 2 - BUTTON0.get_height() / 2 + 50)
	jump, fall = False, False
	pipes = []
	gameOver = False
	mainMenu = True

def main():
	global jump
	global fall
	global gameOver
	global mainMenu
	global pipes
	global button
	global button_start_x_pos
	global button_start_y_pos
	global button_end_x_pos
	global button_end_y_pos
	run = True
	FPS = 60
	clock = pygame.time.Clock()
	SPAWNPIPE = pygame.USEREVENT
	pygame.time.set_timer(SPAWNPIPE, 805)
	pygame.display.set_caption("Flappy bird")
	pygame.display.set_icon(ICON)
	pygame.mixer.music.load(os.path.join("res", "sound.mp3"))
	pygame.mixer.music.play(-1)

	while run:
		keys = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		clock.tick(FPS)
		redraw()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == SPAWNPIPE:
				if not mainMenu:
					if not gameOver:
						rand = random.randrange(155, 330)
						pipeUp = Pipe(WIDTH + UP_PIPE.get_width(), rand, UP_PIPE)
						pipeDown = Pipe(WIDTH + DOWN_PIPE.get_width(), rand - DOWN_PIPE.get_height() - 97, DOWN_PIPE)
						pipes.append(pipeUp)
						pipes.append(pipeDown)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if gameOver:
						if button_start_x_pos <= mouse_pos[0] <= button_end_x_pos and button_start_y_pos <= mouse_pos[1] <= button_end_y_pos and int(button.frame1) == 1:
							restartGame()
					else:
						mainMenu = False
						jump = True
						fall = False
main()