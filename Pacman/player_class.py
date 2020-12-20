from pygame.math import Vector2 as vec
import pygame, sys
from settings import *

class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.grid_to_pixel(self.grid_pos)+vec(self.app.cell_width//2, self.app.cell_height//2)
        self.direction = vec(1,0)                       # direction in which we are moving
        self.stored_direction = None                    # direction we want to move (not necessary we can move always)
        self.able_to_move = True                        # initially we can move
        self.current_score = 0
        self.speed = 2
        self.lives = 3
        #print(self.grid_pos, self.pix_pos)

    ### Converts grid indices to pixel indices ###
    def grid_to_pixel(self, position):
        return vec((position[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2,(position[1]*self.app.cell_height)+TOP_BOTTOM_BUFFER//2)

    ### Converts pixel indices to grid indices ###
    def pixel_to_grid(self,position):
        return vec((position[0]-TOP_BOTTOM_BUFFER)//self.app.cell_width+1,(position[1]-TOP_BOTTOM_BUFFER)//self.app.cell_height+1)

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
            #self.pix_pos[0] += int(self.direction[0]*self.speed)
            #self.pix_pos[1] += int(self.direction[1]*self.speed)
        if self.time_to_move():                                                             # can move in direction
            if (self.stored_direction!=None) & (self.can_move(self.stored_direction)):      # if you have pressed a direction button & also can move in that direction
                self.direction = self.stored_direction
            self.able_to_move = self.can_move(self.direction)

        self.grid_pos = self.pixel_to_grid(self.pix_pos+vec(self.app.cell_width//2, self.app.cell_height//2))
        if self.on_coin():
            self.eat_coin()
        if self.on_gem():
            self.eat_gem()

    ### checks if player is on a coin ###
    def on_coin(self):
        if self.grid_pos in self.app.coins:
            ### Ensures that there is no lag in taking the coin and player ###
            if self.time_to_move():
                return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score +=1
        if(self.current_score>self.app.high_score):
            self.app.high_score=self.current_score

    def on_gem(self):
        if self.grid_pos in self.app.gems:
            ### Ensures that there is no lag in taking the coin and player ###
            if self.time_to_move():
                return True
        return False

    def eat_gem(self):
        self.app.gems.remove(self.grid_pos)
        for enemy in self.app.enemies:
            enemy.personality = 'saving'                # all ghosts want to save themselves
            self.app.timer = 1                          # timer starts here
            enemy.image = self.app.saving               # image of each ghost changed

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (self.pix_pos.x, self.pix_pos.y), self.app.cell_width//2-2)           ## Last argument is radius of circle
        #pygame.draw.rect(self.app.screen, RED, (self.grid_to_pixel(self.grid_pos)[0],self.grid_to_pixel(self.grid_pos)[1], self.app.cell_width, self.app.cell_height), 5)    ## Last 2 arguments are width and height of rectangle
        self.app.draw_text('Lives', self.app.screen, vec(30,HEIGHT-10),(3*START_TEXT_SIZE)//2, WHITE, START_FONT, True)
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (70+20*x,HEIGHT-10), 5)

    def move(self, direction):
        self.stored_direction = direction

    ### Ensures that player is in the grid ###
    def time_to_move(self):
        if (self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if (self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True
        return False

    def can_move(self, direction):
        if direction == None:
            return False
        #print(direction)
        for wall in self.app.walls:
            if vec(self.grid_pos+direction) == wall:
                return False
        return True
