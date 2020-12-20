import pygame, sys
from settings import *
import copy
from player_class import *
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2

class App:
	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		self.state = 'start'
		self.cell_width = MAZE_WIDTH//COLS
		self.cell_height = MAZE_HEIGHT//ROWS
		self.walls = []
		self.coins = []
		self.gems = []
		self.timer = 0											# starts when player takes gem
		self.enemies = []
		self.chased_enemies = []								# enemies chased after taking gem
		self.p_pos = None										# player starting position
		self.e_pos = []											# enemies positions
		self.load()
		self.player = Player(self, copy.copy(self.p_pos))		# copy because that copy is being changed in enemy class
		self.make_enemies()
		self.high_score=0

	def run(self):
		while self.running:
			pygame.display.set_caption('Pacman')
			if self.state == 'start':
				self.start_events()
				self.start_update()
				self.start_draw()
			elif self.state == 'playing':
				self.playing_events()
				self.playing_update()
				self.playing_draw()
			elif self.state == 'game over':
				self.game_over_events()
				self.game_over_update()
				self.game_over_draw()
			elif self.state == 'win':
				self.game_over_events()
				self.game_over_update()
				self.win_draw()
			else:
				self.running = False
			self.clock.tick(FPS)
		pygame.quit()
		sys.exit()

#################################### HELPER FUNCTIONS ##########################

	############### Drawing the words on the screen ##########
	def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
		font = pygame.font.SysFont(font_name, size)
		text = font.render(words, False, color)
		text_size = text.get_size()
		if centered:
			pos[0] = pos[0]-text_size[0]//2			## // is for integer division
			pos[1] = pos[1]-text_size[1]//2
		screen.blit(text, pos)

	def draw_image(self, screen, image, pos):
		rect = image.get_rect()
		#pos[0] = pos[0]-rect[2]//2
		#pos[1] = pos[1]-rect[3]//2
		screen.blit(image, pos)

	def load_images(self):
		self.background = pygame.image.load(r'maze.png')
		self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
		image = pygame.image.load(r'pachead.png')
		self.image_left = pygame.transform.scale(image, (WIDTH//3, HEIGHT//3))
		self.image_right = pygame.transform.flip(self.image_left, True, False) # horizontal or vertical flip - True or False
		image = pygame.image.load(r'pacman-intro.png')
		self.image = pygame.transform.scale(image,(WIDTH//2, HEIGHT//3))
		image = pygame.image.load(r'blinky.jpg')
		self.blinky = pygame.transform.scale(image, (self.cell_width, self.cell_height))
		image = pygame.image.load(r'pinky.jpg')
		self.pinky = pygame.transform.scale(image,(self.cell_width, self.cell_height))
		image = pygame.image.load(r'inky.jpg')
		self.inky = pygame.transform.scale(image,(self.cell_width, self.cell_height))
		image = pygame.image.load(r'clyde.jpg')
		self.clyde = pygame.transform.scale(image,(self.cell_width, self.cell_height))
		image = pygame.image.load(r'chased.png')
		self.saving = pygame.transform.scale(image,(self.cell_width, self.cell_height))

	def load(self):
		self.load_images()
		# Creating walls, walls contains co-ordinates of walls only
		with open("walls.txt",'r') as file:
			for yidx, line in enumerate(file):
				for xidx, c in enumerate(line):
					if c=='1':												# walls
						self.walls.append(vec(xidx,yidx))
					elif c=='C':											# coins
						self.coins.append(vec(xidx,yidx))
					elif c=='P':											# player_starting_pos
						self.p_pos = vec(xidx,yidx)
					elif c in ['2','3','4','5']:							# enemies
						self.e_pos.append([xidx, yidx])
					elif c=='B':											# entrance for enemies
						pygame.draw.line(self.background, WHITE, (xidx*self.cell_width, yidx*self.cell_height + self.cell_height//2), (xidx*self.cell_width + self.cell_width-1, yidx*self.cell_height + self.cell_height//2), self.cell_height//4)
						#pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))
					elif c=='G':											# power ball/ gem
						self.gems.append(vec(xidx,yidx))
			#print(self.walls)

	def make_enemies(self):
		for idx, enemy in enumerate(self.e_pos):
			#print(enemy)
			self.enemies.append(Enemy(self,vec(enemy),idx))

	def draw_grid(self):
		## There are 28 cells accross the screen ##
		for x in range(MAZE_WIDTH//self.cell_width):
			pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
		for y in range(MAZE_HEIGHT//self.cell_height):
			pygame.draw.line(self.background, GREY, (0, y*self.cell_height), (WIDTH, y*self.cell_height))
		#for wall in self.walls:
			#pygame.draw.rect(self.background, (112, 55, 163), (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))
		for coin in self.coins:
			pygame.draw.rect(self.background, RED, (coin.x*self.cell_width, coin.y*self.cell_height, self.cell_width, self.cell_height))

	def enemy_reset(self, enemy, timer_end):
		if timer_end != True:
			enemy.grid_pos = enemy.starting_position
			enemy.pix_pos = self.grid_to_pixel(enemy.grid_pos)+vec(self.cell_width//2, self.cell_height//2)
			enemy.direction *= 0
		enemy.image = enemy.set_image()
		enemy.personality = enemy.set_personality()

	### reset the player and enemy starting position
	def reset(self):
		self.player.direction = vec(1,0)
		self.player.grid_pos = self.p_pos
		self.player.pix_pos = self.grid_to_pixel(self.player.grid_pos)+vec(self.cell_width//2, self.cell_height//2)
		### setting each enemy at starting position at the time of collison ###
		for enemy in self.enemies:
			self.enemy_reset(enemy, False)

	def reset_game(self):
		self.player.current_score=0
		self.player.lives = 3
		self.coins = []
		self.gems = []
		self.state = 'playing'
		with open("walls.txt",'r') as file:
			for yidx, line in enumerate(file):
				for xidx, c in enumerate(line):
					if c=='C':											# new coins
						self.coins.append(vec(xidx,yidx))
					elif c=='G':
						self.gems.append(vec(xidx,yidx))				# new gems
		self.reset()


#################################### INTRO FUNCTIONS ###########################

	def start_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.state = 'playing'

	def start_update(self):
		pass

	def start_draw(self):
		self.screen.fill(BLACK)
		self.draw_image(self.screen, self.image, [WIDTH//4, HEIGHT//6])
		self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2 + HEIGHT//4], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)	# Scree, Color scheme
		self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2 + HEIGHT//4 + 50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
		self.draw_text('HIGH SCORE', self.screen, [4,0], START_TEXT_SIZE, (255,255,255), START_FONT)
		pygame.display.update()


#################################### PLAYING_FUNCTIONS #########################

	def playing_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.move(vec(-1,0))
				if event.key == pygame.K_RIGHT:
					self.player.move(vec(1,0))
				if event.key == pygame.K_UP:
					self.player.move(vec(0,-1))
				if event.key == pygame.K_DOWN:
					self.player.move(vec(0,1))

	def playing_update(self):
		# if timer is on #
		if self.timer > 0:
			self.timer += 1
			# timer ended #
			if self.timer % TIMER == 0:
				self.timer = 0
				for enemy in self.enemies:
					self.enemy_reset(enemy, True)

		self.player.update()
		for enemy in self.enemies:
			enemy.update()
		for enemy in self.enemies:
			if enemy.grid_pos == self.player.grid_pos:					# if ghost reaches player
				if enemy.personality != 'saving':						# gem not taken, we lost one life
					self.remove_life()
					self.chased_enemies = []
				else:													# player touches ghost after taking gem
					self.player.current_score += 50
					if self.player.current_score>self.high_score:
						self.high_score = self.player.current_score
					self.chased_enemies.append(enemy)
					# when a ghost have been chased it's personality again becomes normal
					self.enemy_reset(enemy, False)

		if self.coins == [] and self.player.current_score>0:
			self.state = 'win'

	def playing_draw(self):
		self.screen.fill(BLACK)
		self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
		self.draw_coins()
		self.draw_gems()
		#self.draw_grid()
		self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60,5], START_TEXT_SIZE, WHITE, START_FONT)
		self.draw_text('HIGH SCORE: {}'.format(self.high_score), self.screen, [WIDTH//2,10], START_TEXT_SIZE, WHITE, START_FONT, True)
		self.draw_text('vjac@noble', self.screen, [WIDTH-60,10], START_TEXT_SIZE, WHITE, START_FONT, True)
		self.player.draw()
		for enemy in self.enemies:
			enemy.draw()
		pygame.display.update()
		#self.coins.pop()

	def remove_life(self):
		self.player.lives -= 1
		if self.player.lives == 0:
			self.state = 'game over'
		else:
			self.reset()

	def draw_coins(self):
		for coin in self.coins:
			pygame.draw.circle(self.screen, COIN_COLOR, (coin.x*self.cell_width + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,coin.y*self.cell_height + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 3)

	def draw_gems(self):
		for gem in self.gems:
			pygame.draw.circle(self.screen, BLUE, (gem.x*self.cell_width + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,gem.y*self.cell_height + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), self.cell_width//2)

	### Converts grid indices to pixel indices ###
	def grid_to_pixel(self, position):
		return vec((position[0]*self.cell_width)+TOP_BOTTOM_BUFFER//2,(position[1]*self.cell_height)+TOP_BOTTOM_BUFFER//2)

    ### Converts pixel indices to grid indices ###
	def pixel_to_grid(self,position):
		return vec((position[0]-TOP_BOTTOM_BUFFER)//self.cell_width+1,(position[1]-TOP_BOTTOM_BUFFER)//self.cell_height+1)


 ###################################### GAME_OVER FUNCTIONS #########################
	def game_over_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.reset_game()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.running = False

	def game_over_update(self):
		pass

	def game_over_draw(self):
		self.screen.fill(BLACK)
		self.draw_image(self.screen, self.image_left, [WIDTH//6 + 200, HEIGHT//6])
		self.draw_image(self.screen, self.image_right, [WIDTH//6, HEIGHT//6])
		self.draw_text("GAME OVER", self.screen, vec(WIDTH//2,HEIGHT//2), 40, RED, 'arial', True)
		self.draw_text("Press SPACE to RESTART", self.screen, vec(WIDTH//4,HEIGHT//4 + HEIGHT//2), 20, WHITE, 'arial', True)
		self.draw_text("Press ESC to QUIT", self.screen, vec(WIDTH//4 + WIDTH//2,HEIGHT//4 + HEIGHT//2), 20, WHITE, 'arial', True)
		pygame.display.update()

	def win_draw(self):
		self.screen.fill(BLACK)
		self.draw_image(self.screen, self.image_left, [WIDTH//6 + 200, HEIGHT//6])
		self.draw_image(self.screen, self.image_right, [WIDTH//6, HEIGHT//6])
		self.draw_text("YOU WON", self.screen, vec(WIDTH//2,HEIGHT//2), 40, RED, 'arial', True)
		self.draw_text("Press SPACE to RESTART", self.screen, vec(WIDTH//4,HEIGHT//4 + HEIGHT//2), 20, WHITE, 'arial', True)
		self.draw_text("Press ESC to QUIT", self.screen, vec(WIDTH//4 + WIDTH//2,HEIGHT//4 + HEIGHT//2), 20, WHITE, 'arial', True)
		pygame.display.update()
