# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys
import pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from objloader import *

import os


def OnResizeEvent(event):
    viewport = (event.width, event.height)
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    # refresh2d(*viewport)


viewport = (800, 600)

pygame.init()

hx = viewport[0]/2
hy = viewport[1]/2


'''glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
glClearColor(1, 1, 0, 1)'''
# LOAD OBJECT AFTER PYGAME INIT
#obj = OBJ("testobject2.obj")

clock = pygame.time.Clock()

'''glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
'''


def refresh2d(width, height):
    global srf
    srf = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1, 1, 1, 1)


refresh2d(*viewport)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
rotate = move = False


def DrawGrid(width, gap):
    # setup opengl to accept and array of vertexes
    glEnableClientState(GL_VERTEX_ARRAY)
    glColor(0.1, 0.1, 0.1)
    # draw many lines while opengl is setup for it
    for x in range(0, viewport[0], gap):
        # define the vertexes of the line
        lineVertices = [x, 0, 0.0, x, viewport[1], 0.0]

        glLineWidth(width)
        # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
        glVertexPointer(3, GL_FLOAT, 0, lineVertices)
        # Draw the line
        glDrawArrays(GL_LINES, 0, 2)

    for y in range(0, viewport[1], gap):
        # define the vertexes of the line
        lineVertices = [0, y, 0.0, viewport[0], y, 0.0]

        glLineWidth(width)
        # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
        glVertexPointer(3, GL_FLOAT, 0, lineVertices)
        # Draw the line
        glDrawArrays(GL_LINES, 0, 2)

    # disable previous instructions
    glDisableClientState(GL_VERTEX_ARRAY)


while 1:
    clock.tick(144)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos = max(1, zpos-1)
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    #glTranslate(tx/20., ty/20., - zpos)
    #glRotate(ry, 1, 0, 0)
    #glRotate(rx, 0, 1, 0)
    # glCallList(obj.gl_list)

    DrawGrid(1, 50)

    pygame.display.flip()
