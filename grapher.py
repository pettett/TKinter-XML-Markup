#!/usr/bin/python
import sys
import pygame
from pygame.locals import *
from pygame.constants import *
import math
import tkml
# grapher will take in a user input from the base bar and plot the graph on a pygame generated window


if __name__ == '__main__':

    def DrawGrid(screen, gap, width, color):
        screenRect = Rect(0, 0, screen.get_width(), screen.get_height())

        for x in range(xOffset % gap, screenRect.width, gap):
            # draw a grid line every gap units in width width and colour color
            pygame.draw.line(screen, color, (x, 0),
                             (x, screenRect.height), width)

        for y in range(yOffset % gap, screenRect.height, gap):
            # draw line from bottom of the screen to the top
            pygame.draw.line(screen, color, (0, y),
                             (screenRect.width, y), width)

    def DrawAxis(screen, width, color):
        screenRect = Rect(0, 0, screen.get_width(), screen.get_height())
        # draw the x axis on x=0
        pygame.draw.line(screen, color, (0, yOffset),
                         (screenRect.width, yOffset), width)

        pygame.draw.line(screen, color, (xOffset, 0),
                         (xOffset, screenRect.height), width)

    def DrawEquationLineStrip(equation, screen, stepSize, width, color, scale):
        screenRect = Rect(0, 0, screen.get_width(), screen.get_height())
        lineVertices = []

        # create a list of vertices for the graph
        for x in range(0, screenRect.width, 10):
            y = equation((x-xOffset)/scale)*scale+yOffset
            lineVertices.append(x)
            lineVertices.append(y)
            lineVertices.append(0)

        glColor(color[0], color[1], color[2], 1)
        glLineWidth(width)
        glVertexPointer(3, GL_FLOAT, 0, lineVertices)
        # Draw the line
        glDrawArrays(GL_LINE_STRIP, 0, len(lineVertices)//3)

    def DrawEquations(equations):

        # setup drawing for the multiple equation lines
        glEnableClientState(GL_VERTEX_ARRAY)
        for i, equation in enumerate(equations):
            DrawEquationLineStrip(equation, pygameFrame.screen, 10,
                                  3, lineColors[i], 50)

        # disable previous instructions
        glDisableClientState(GL_VERTEX_ARRAY)

    def DrawGraph():
        # draw thick grid lines
        DrawGrid(pygameFrame.screen, 50, 2, Color(40, 40, 40))
        # draw thin grid lines
        DrawGrid(pygameFrame.screen, 10, 1, Color(80, 80, 80))

        # draw the x and y axis
        DrawAxis(pygameFrame.screen, 3, Color(0, 0, 0))

        DrawEquations(equations)

        pygameFrame.Flip()

    def Update():
        global xOffset, yOffset

        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                if event.buttons[0]:
                    xOffset += event.rel[0]
                    yOffset += event.rel[1]

        DrawGraph()

    def GenerateGraph():
        global equations
        equations = []
        for i in range(lineCount):
            equationString = window.values['input{0}'.format(i)].get()
            equations.append(eval('lambda x:'+equationString, math.__dict__))

    def AddLine():
        global lineCount
        markup = equationField.format(lineCount)
        if lineCount != 0:
            window.AppendElements(
                '<body><seperator pady=3/></body>', window.elements['equationholder'])

        window.AppendElements(markup, window.elements['equationholder'])
        x = lineCount  # save the current index into its own variable so it stays constant after new lines are made
        window.callbacks['remove{0}'.format(lineCount)] = lambda: RemoveLine(x)

        lineCount += 1

    def RemoveLine(index):
        pass

    startSize = (800, 600)

    markup = '''
    <body>
    <title>Grapher!</title>
    <vertical>
        <pygameframe weight=1 ref="pygameframe" width={0} height={1}>OPENGL</pygameframe>
        <horizontal sticky="ews">
        <vertical ref="equationholder">
        </vertical>
        <vertical weight=0>
            <button pady=15 weight=1 callback="generategraph">Generate Graph</button>
            <button pady=15 weight=1 callback="addline">Add Line</button>
        </vertical>
        </horizontal>
    </vertical>
    </body>
    '''.format(*startSize)

    lineCount = 0

    equationField = """<horizontal>
            <p weight=0>Enter Equation:</p>
            <field padx=5 varname="input{0}"/>
            <button weight=0 callback="remove{0}">x</button>
            </horizontal>"""

    xOffset = 400
    yOffset = 300

    window = tkml.Window(markup)
    window.callbacks = {"generategraph": GenerateGraph,
                        "addline": AddLine}

    pygameFrame = window.elements['pygameframe']
    pygameFrame.OnUpdate = Update

    screenRect = Rect(0, 0, 800,
                      pygameFrame.screen.get_height())
    # pygame.init()
    refresh2d(*startSize)

    def StartFunction(x): return x**2

    equations = [StartFunction]
    lineColors = [
        (255, 40, 40),
        (40, 255, 40),
        (40, 40, 255),
        (255, 255, 40),
        (255, 40, 255),
        (40, 255, 255)
    ]
    # this is a cry for help

    window.root.after(0, pygameFrame.MainLoop)

    window.mainloop()
