import sys
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *  # <-----owo what is this
import math
import tkml
import tkviewport
from tkinter import *
import random

lastMousePos = None
viewport = (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2

xOffset = int(hx)
yOffset = -int(hy)
yPixelsPerUnit = 100
xPixelsPerUnit = 100
xInverseMultiplier = 1/xPixelsPerUnit

markup = '''
    <body>
    <title>Grapher!</title>
    <vertical>
        <GraphFrame weight="1" ref="graphframe" frameTime="4" width="{0}" height="{1}"/>
        <seperator pady="15"/>
        <horizontal sticky="ews">

            <vertical ref="equationholder">
            </vertical>

            <vertical weight="0">
                <button weight="1" callback="GenerateGraph">Generate Graph</button>
                <button weight="1" callback="AddLine">Add Line</button>
            </vertical>
        </horizontal>
    </vertical>
    </body>
    '''.format(*viewport)

window = tkml.Window(markup, generate=False)


@window.custom
class GraphFrame(tkviewport.OpenGLFrame):
    def __init__(self, window, root, **kw):
        kw["frameTime"] = int(kw.pop("frameTime", 0))
        super().__init__(root, **kw)

    def startgl(self):
        refresh2d(self.width, self.height)

    def initgl(self):
        refresh2d(self.width, self.height)

    def redraw(self):
        DrawGraph(self.width, self.height)


window.GenerateWindow()


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1, 1, 1, 1)


def DrawGrid(width, xgap, ygap):
    # setup opengl to accept and array of vertexes
    glEnableClientState(GL_VERTEX_ARRAY)
    glColor(0.1, 0.1, 0.1)
    # draw many lines while opengl is setup for it
    for x in range(xOffset % xgap, viewport[0], xgap):
        # define the vertexes of the line
        lineVertices = [x, 0, 0.0, x, viewport[1], 0.0]

        glLineWidth(width)
        # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
        glVertexPointer(3, GL_FLOAT, 0, lineVertices)
        # Draw the line
        glDrawArrays(GL_LINES, 0, 2)

    for y in range(-yOffset % ygap, viewport[1], ygap):
        # define the vertexes of the line
        lineVertices = [0, y, 0.0, viewport[0], y, 0.0]

        glLineWidth(width)
        # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
        glVertexPointer(3, GL_FLOAT, 0, lineVertices)
        # Draw the line
        glDrawArrays(GL_LINES, 0, 2)

    # disable previous instructions
    glDisableClientState(GL_VERTEX_ARRAY)


def DrawLines():

    # setup opengl to accept and array of vertexes
    glEnableClientState(GL_VERTEX_ARRAY)

    lineVertices = [200.0, 100.0, 0.0, 100.0, 300.0, 0.0]

    # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
    glVertexPointer(3, GL_FLOAT, 0, lineVertices)
    # Draw the line
    glDrawArrays(GL_LINES, 0, 2)
    # draw the next line while still within client state to make better performance (i think)
    lineVertices = [300.0, 200.0, 0.0, 200.0, 400.0, 0.0]
    # tell openGL how to read the vertexes - groups of 3, floats, 0 gap, using array defined above
    glVertexPointer(3, GL_FLOAT, 0, lineVertices)
    # Draw the line
    glDrawArrays(GL_LINES, 0, 2)
    # disable previous instructions
    glDisableClientState(GL_VERTEX_ARRAY)


def DrawEquationLineStrip(equation, color):
    lineVertices = []
    sampleSize = 5
    # create a list of vertices for the graph
    for x in range(xOffset % sampleSize, viewport[0]+sampleSize, sampleSize):

        try:
            y = equation((x-xOffset)/xPixelsPerUnit)*yPixelsPerUnit-yOffset
            lineVertices.append(x)
            lineVertices.append(y)
            lineVertices.append(0)
        except ValueError:
            # do not add the value to the array
            pass

    glColor(color[0], color[1], color[2], 1)
    glLineWidth(2.5)
    glVertexPointer(3, GL_FLOAT, 0, lineVertices)
    # Draw the line
    glDrawArrays(GL_LINE_STRIP, 0, len(lineVertices)//3)


def DrawEquations():

    # setup drawing for the multiple equation lines
    glEnableClientState(GL_VERTEX_ARRAY)

    for i, equation in enumerate(equations):
        DrawEquationLineStrip(equation, lineColors[i])

    # disable previous instructions
    glDisableClientState(GL_VERTEX_ARRAY)


def DrawGraph(w, h):
    global viewport
    viewport = (w, h)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # render equations

    unitsInScreen = w/xPixelsPerUnit
    # pick unit scale based on units on screen

    scalar = 0.05

    # calculate scale from closest power of 10

    xUnitScale = 2 ** math.ceil(math.log2(unitsInScreen*scalar))

    yUnitScale = 2 ** math.ceil(math.log2(unitsInScreen*scalar))

    # one grid line should reprosent unit scale number of units

    DrawGrid(1.5, int(xPixelsPerUnit*xUnitScale)*2,
             int(yPixelsPerUnit*yUnitScale)*2)

    DrawGrid(1, int(xPixelsPerUnit*xUnitScale),
             int(yPixelsPerUnit*yUnitScale))

    DrawEquations()


@window.callback
def GenerateGraph():
    global equations
    equations = []
    for i in range(lineCount):
        equationString = window.values['input{0}'.format(i)].get()
        equations.append(eval('lambda x:'+equationString, math.__dict__))


@window.callback
def AddLine(startValue=''):
    global lineCount
    markup = equationField.format(lineCount)
    if lineCount != 0:
        window.AppendElements(
            '<body><seperator pady="3"/></body>', window.elements['equationholder'])

    window.AppendElements(markup, window.elements['equationholder'])
    x = lineCount  # save the current index into its own variable so it stays constant after new lines are made

    window.values['input{0}'.format(lineCount)].set(startValue)

    if lineCount > len(lineColors)-1:
        lineColors.append((random.random(), random.random(), random.random()))

    window.elements['colorpick{0}'.format(
        lineCount)].NormalizedColor = lineColors[lineCount]

    window.elements['colorpick{0}'.format(
        lineCount)].OnChangeEvent = lambda: ChangeLineColor(x)

    window.callbacks['remove{0}'.format(lineCount)] = lambda: RemoveLine(x)

    lineCount += 1


def RemoveLine(index):
    pass


def ChangeLineColor(index):
    global lineColors
    color = window.elements['colorpick{0}'.format(
        index)].NormalizedColor
    print(color)
    lineColors[index] = color


def OnMouseDrag(event):
    global lastMousePos, xOffset, yOffset
    if lastMousePos == None:
        lastMousePos = (event.x, event.y)
    relX = event.x - lastMousePos[0]
    relY = event.y - lastMousePos[1]
    xOffset += relX
    yOffset += relY

    lastMousePos = (event.x, event.y)


def OnMouseUp(event):
    global lastMousePos
    lastMousePos = None


def MouseWheel(event):
    ZoomX(event.delta)
    ZoomY(event.delta)


def ShiftMouseWheel(event):
    ZoomX(event.delta)


def CtrlMouseWheel(event):
    ZoomY(event.delta)


def ZoomX(delta):
    global xPixelsPerUnit
    change = delta/120/10
    xPixelsPerUnit += xPixelsPerUnit * change


def ZoomY(delta):
    global yPixelsPerUnit
    change = delta/120/10
    yPixelsPerUnit += yPixelsPerUnit*change


lineCount = 0

equations = []

equationField = """<horizontal>
            <colorfield ref="colorpick{0}" weight="0"/>
            <p weight="0">Enter Equation:</p>
            <field padx="5" varname="input{0}"/>
            <button weight="0" callback="remove{0}">x</button>
            </horizontal>"""


lineColors = [
    (1, .40, .40),
    (.40, 1, .40),
    (.40, .40, 1),
    (1, 1, .40),
    (1, .40, 1),
    (.40, 1, 1)
]


graphFrame = window.elements['graphframe']

graphFrame.bind('<B1-Motion>', OnMouseDrag)
graphFrame.bind('<MouseWheel>', MouseWheel)
graphFrame.bind('<Shift-MouseWheel>', ShiftMouseWheel)
graphFrame.bind('<Control-MouseWheel>', CtrlMouseWheel)
graphFrame.bind('<ButtonRelease-1>', OnMouseUp)
AddLine('x**2')
GenerateGraph()

window.mainloop()
