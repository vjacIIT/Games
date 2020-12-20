import pygame
import numpy as np
import copy
from settings import *
vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.starting_position = copy.copy(pos)
        self.grid_pos = pos                             # starting_position of enemy
        self.pix_pos = self.grid_to_pixel(self.grid_pos)+vec(self.app.cell_width//2, self.app.cell_height//2)
        self.number = number                            # which number enemy you are
        #self.color = self.set_color()
        self.personality = self.set_personality()
        self.image = self.set_image()                   # image of enemy
        self.direction = vec(0,0)
        self.target = None
        self.speed = self.set_speed()

    ### Converts grid indices to pixel indices ###
    def grid_to_pixel(self, position):
        return vec((position[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2,(position[1]*self.app.cell_height)+TOP_BOTTOM_BUFFER//2)

    ### Converts pixel indices to grid indices ###
    def pixel_to_grid(self,position):
        return vec((position[0]-TOP_BOTTOM_BUFFER)//self.app.cell_width+1,(position[1]-TOP_BOTTOM_BUFFER)//self.app.cell_height+1)

    def scared_direction(self):
        if (self.app.player.grid_pos.x > COLS//2) and (self.app.player.grid_pos.y > ROWS//2):
            return vec(1,1)
        elif (self.app.player.grid_pos.x > COLS//2) and (self.app.player.grid_pos.y < ROWS//2):
            return vec(1,ROWS-2)
        elif (self.app.player.grid_pos.x < COLS//2) and (self.app.player.grid_pos.y > ROWS//2):
            return vec(COLS-2,1)
        elif (self.app.player.grid_pos.x < COLS//2) and (self.app.player.grid_pos.y < ROWS//2):
            return vec(COLS-2,ROWS-2)
        else:
            return vec(COLS//2,ROWS//2)

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction*self.speed
            if self.time_to_move():
                self.move()
        self.grid_pos = self.pixel_to_grid(self.pix_pos+vec(self.app.cell_width//2, self.app.cell_height//2))

    def set_speed(self):
        if self.personality == 'scared':
            return 2
        elif self.personality == 'speedy':
            return 2.5
        else:
            return 1

    def set_target(self):
        if self.personality == 'speedy' or self.personality == 'slow':
            return self.app.player.grid_pos
        elif self.personality == 'saving':
            return self.scared_direction()
        else:
            return self.scared_direction()

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()
        if self.personality == 'saving':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'slow':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'speedy':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'scared':
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        ### path gives the shortest path from enemy to player ###
        path = self.BFS(self.grid_pos, target)
        #print(path[1],self.grid_pos,path[1]-self.grid_pos)
        return path[1]-self.grid_pos                        # we need the 2nd cell in the path

    #### Start position and ending position are vectors ###
    def BFS(self, start_pos, end_pos):
        ### 2-D array on which we will work up on BFS ###
        grid = [[0 for x in range(ROWS+1)] for y in range(COLS)]
        #print(np.shape(grid))
        for cell in self.app.walls:
            #print(cell)
            grid[int(cell[0])][int(cell[1])] = 1                      # putting walls in grid
        queue = [start_pos]
        path = []                                           # path is a dictionary
        visited = []
        while len(queue)!= 0:                               # while queue not empty
            cell = queue[0]                                 # take top element out (element is a vector)
            queue.remove(queue[0])
            visited.append(cell)                            # inserting the top element in visited array
            if cell == end_pos:                             # we reached target
                break

            neighbours = [[0,1],[0,-1],[1,0],[-1,0]]
            for neighbour in neighbours:
                new_cell = vec(cell[0]+neighbour[0], cell[1]+neighbour[1])
                ### if grid is not blocked and not visited earlier insert into queue
                if (grid[int(new_cell[0])][int(new_cell[1])]!=1) and (new_cell not in visited):
                    queue.append(new_cell)
                    path.append({"Current":cell, "Next":new_cell})
        shortest = [end_pos]
        while end_pos != start_pos:
            for step in path:
                if step["Next"] == end_pos:
                    end_pos = step["Current"]
                    shortest.insert(0,step["Current"])
        return shortest

    def get_random_direction(self):
        ### Loop because we need to try again if we hit a wall (unlike player) ###
        while True:
            dir = np.random.choice(4)
            #print(dir)
            if dir == 0:
                mov_dir = vec(1,0)
            elif dir == 1:
                mov_dir = vec(-1,0)
            elif dir == 2:
                mov_dir = vec(0,1)
            elif dir == 3:
                mov_dir = vec(0,-1)
            ### if we don't have a wall in that direction ###
            if (self.grid_pos+mov_dir) not in self.app.walls:
                return mov_dir

    ### Ensures that enemy is in the grid ###
    def time_to_move(self):
        if (self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True
        if (self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 or self.direction == vec(0,0):
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True
        return False

    def draw(self):
        #pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.app.cell_width//2-2)
        self.app.draw_image(self.app.screen, self.image, [self.pix_pos[0]-self.app.cell_width//2,self.pix_pos[1]-self.app.cell_height//2])

    def set_color(self):
        if self.number == 0:
             return BLUE
        elif self.number == 1:
             return RED
        elif self.number == 2:
            return WHITE
        elif self.number == 3:
            return PINK

    def set_image(self):
        if self.number == 0:
             return self.app.inky
        elif self.number == 1:
             return self.app.blinky
        elif self.number == 2:
            return self.app.clyde
        elif self.number == 3:
            return self.app.pinky

    def set_personality(self):
        if self.number == 0:
             return 'speedy'
        elif self.number == 1:
             return 'slow'
        elif self.number == 2:
            return 'random'
        elif self.number == 3:
            return 'scared'
