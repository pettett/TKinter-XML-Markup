#!/usr/bin/python
from sys import argv
import pygame
from pygame.locals import *
from random import shuffle

"""Contains the Maze class which is the array-represented maze."""


class Maze:

    def __init__(self, rows=30, cols=40):

        self.rows = rows
        self.cols = cols
        self.keep_going = 1

        self.maze = {}
        for y in range(rows):
            for x in range(cols):
                cell = {'south': 1, 'east': 1, 'visited': 0}
                self.maze[(x, y)] = cell

    def generate(self, start_cell=None, stack=[]):
        """Generates a random maze using a magical simple recursive function."""

        if start_cell is None:
            start_cell = self.maze[(self.cols-1, self.rows-1)]

        if not self.keep_going:
            return

        self.check_finished()
        neighbors = []

        # if the stack is empty, add the start cell
        if len(stack) == 0:
            stack.append(start_cell)

        # set current cell to last cell
        curr_cell = stack[-1]

        # get neighbors and shuffle 'em up a bit
        neighbors = self.get_neighbors(curr_cell)
        shuffle(neighbors)

        for neighbor in neighbors:
            if neighbor['visited'] == 0:
                neighbor['visited'] = 1
                stack.append(neighbor)
                self.knock_wall(curr_cell, neighbor)

                self.generate(start_cell, stack)

    def get_coords(self, cell):
        # grabs coords of a given cell
        coords = (-1, -1)
        for k in self.maze:
            if self.maze[k] is cell:
                coords = (k[0], k[1])
                break
        return coords

    def get_neighbors(self, cell):
        # obvious
        neighbors = []

        (x, y) = self.get_coords(cell)
        if (x, y) == (-1, -1):
            return neighbors

        north = (x, y-1)
        south = (x, y+1)
        east = (x+1, y)
        west = (x-1, y)

        if north in self.maze:
            neighbors.append(self.maze[north])
        if south in self.maze:
            neighbors.append(self.maze[south])
        if east in self.maze:
            neighbors.append(self.maze[east])
        if west in self.maze:
            neighbors.append(self.maze[west])

        return neighbors

    def knock_wall(self, cell, neighbor):
        # knocks down wall between cell and neighbor.
        xc, yc = self.get_coords(cell)
        xn, yn = self.get_coords(neighbor)

        # Which neighbor?
        if xc == xn and yc == yn + 1:
            # neighbor's above, knock out south wall of neighbor
            neighbor['south'] = 0
        elif xc == xn and yc == yn - 1:
            # neighbor's below, knock out south wall of cell
            cell['south'] = 0
        elif xc == xn + 1 and yc == yn:
            # neighbor's left, knock out east wall of neighbor
            neighbor['east'] = 0
        elif xc == xn - 1 and yc == yn:
            # neighbor's right, knock down east wall of cell
            cell['east'] = 0

    def check_finished(self):
        # Checks if we're done generating
        done = 1
        for k in self.maze:
            if self.maze[k]['visited'] == 0:
                done = 0
                break
        if done:
            self.keep_going = 0


class Game:

    def __init__(self, frame, diff, dim, path):
        self.size = (800, 600)
        self.screen = frame.screen
        self.frame = frame
        font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
        text = font.render("Loading...", 1, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.size[0]/2, self.size[1]/2
        self.screen.blit(text, rect)
        pygame.display.update(rect)

        self.diff = diff
        self.dim = map(int, dim.split('x'))
        self.path = path

    def start(self):
        # pass args to change maze size: Maze(10, 10)
        self.maze_obj = Maze(*self.dim)
        if self.diff == 0:
            self.maze_obj.generate(self.maze_obj.maze[(0, 0)])
        else:
            self.maze_obj.generate()

        self.draw_maze()
        self.reset_player()
        self.keep_going = 1

    def reset_player(self):
        # Make the sprites for the player.
        w, h = self.cell_width - 3, self.cell_height - 3
        rect = 0, 0, w, h
        base = pygame.Surface((w, h))
        base.fill((255, 255, 255))
        self.red_p = base.copy()
        self.green_p = base.copy()
        self.blue_p = base.copy()
        self.goldy = base.copy()
        if self.path == 1:
            r = (255, 0, 0)
            g = (0, 255, 0)
        else:
            r = g = (255, 255, 255)
        b = (0, 0, 255)
        gold = (0xc5, 0x93, 0x48)
        pygame.draw.ellipse(self.red_p, r, rect)
        pygame.draw.ellipse(self.green_p, g, rect)
        pygame.draw.ellipse(self.blue_p, b, rect)
        pygame.draw.ellipse(self.goldy, gold, rect)

        # Make a same-size matrix for the player.
        self.player_maze = {}
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                cell = {'visited': 0}  # if 1, draws green. if >= 2, draws red.
                self.player_maze[(x, y)] = cell
                self.screen.blit(
                    base, (x*self.cell_width+2, y*self.cell_height+2))

        self.screen.blit(
            self.goldy, (x*self.cell_width+2, y*self.cell_height+2))
        self.cx = self.cy = 0
        self.curr_cell = self.player_maze[(
            self.cx, self.cy)]  # starts at origin

        self.last_move = None  # For last move fun

    def draw_maze(self):
        self.screen.fill((255, 255, 255))

        self.cell_width = self.size[0]/self.maze_obj.cols
        self.cell_height = self.size[1]/self.maze_obj.rows

        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.maze_obj.maze[(x, y)]['south']:  # draw south wall
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (x*self.cell_width, y *
                                      self.cell_height + self.cell_height),
                                     (x*self.cell_width + self.cell_width,
                                      y*self.cell_height + self.cell_height))
                if self.maze_obj.maze[(x, y)]['east']:  # draw east wall
                    pygame.draw.line(self.screen, (0, 0, 0),
                                     (x*self.cell_width + self.cell_width,
                                      y*self.cell_height),
                                     (x*self.cell_width + self.cell_width, y*self.cell_height +
                                      self.cell_height))
        # Screen border
        pygame.draw.rect(self.screen, (100, 0, 0),
                         (0, 0, self.size[0], self.size[1]), 1)

    def loop(self):

        moved = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = 0
                if event.key == K_r:
                    self.reset_player()
                if event.key == K_DOWN:
                    self.move_player('d')
                    moved = 1
                if event.key == K_UP:
                    self.move_player('u')
                    moved = 1
                if event.key == K_LEFT:
                    self.move_player('l')
                    moved = 1
                if event.key == K_RIGHT:
                    self.move_player('r')
                    moved = 1
        keys = pygame.key.get_pressed()
        if not moved:
            if keys[K_DOWN]:
                self.move_player('d')
            if keys[K_UP]:
                self.move_player('u')
            if keys[K_LEFT]:
                self.move_player('l')
            if keys[K_RIGHT]:
                self.move_player('r')

    def move_player(self, dir):
        no_move = 0
        try:
            if dir == 'u':
                if not self.maze_obj.maze[(self.cx, self.cy-1)]['south']:
                    self.cy -= 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif dir == 'd':
                if not self.maze_obj.maze[(self.cx, self.cy)]['south']:
                    self.cy += 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif dir == 'l':
                if not self.maze_obj.maze[(self.cx-1, self.cy)]['east']:
                    self.cx -= 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            elif dir == 'r':
                if not self.maze_obj.maze[(self.cx, self.cy)]['east']:
                    self.cx += 1
                    self.curr_cell['visited'] += 1
                else:
                    no_move = 1
            else:
                no_move = 1
        except KeyError:  # Tried to move outside screen
            no_move = 1

        # Handle last move...
        if ((dir == 'u' and self.last_move == 'd') or
                (dir == 'd' and self.last_move == 'u') or
                (dir == 'l' and self.last_move == 'r') or
                (dir == 'r' and self.last_move == 'l')) and \
                not no_move:
            self.curr_cell['visited'] += 1

        if not no_move:
            self.last_move = dir
            self.curr_cell = self.player_maze[(self.cx, self.cy)]

        # Check for victory.
        if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
            print('Congratumalations, you beat this maze.')
            self.keep_going = 0

    def draw_player(self):
        for y in range(self.maze_obj.rows):
            for x in range(self.maze_obj.cols):
                if self.player_maze[(x, y)]['visited'] > 0:
                    if self.player_maze[(x, y)]['visited'] == 1:
                        circ = self.green_p
                    else:
                        circ = self.red_p
                    # draw green circles
                    self.screen.blit(
                        circ, (x*self.cell_width+2, y*self.cell_height+2))
        self.screen.blit(self.blue_p, (self.cx*self.cell_width+2,
                                       self.cy*self.cell_height+2))
