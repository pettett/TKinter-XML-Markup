import tkml
import tkviewport
from OpenGL.GL import *
import math

markup = '''
<tkml>
<title>Tree Factal</title>
<style ref="label" width="3"></style>
<style ref="valSlider" showvalue="0" orient="horizontal" min="1"></style>
<body minWidth="800" minHeight="400">
<horizontal>
    <FractalFrame weight="1" sticky="NSWE" ref="fractalframe"/>
    
    <vertical scrolled="True" weight="0">
        <p width="40">Tree Fractal</p>
        
        <p>Branch Length</p>
        
        <horizontal>
            <slider style="valSlider" varname="branchLength" max="200" default="80"/>
            <p style="label" varname='branchLength'/>
        </horizontal>
        
        <p>Branch Splits</p>
        
        <horizontal>
        <slider style="valSlider" varname="branchSplits" max="10" default="2"/>
        <p style="label" varname='branchSplits'/>
        </horizontal>
        
        <p>Branch Count</p>
        
        <horizontal>
        <slider style="valSlider" varname="branchCount" max="20" default="4"/>
        <p style="label" varname='branchCount'/>
        </horizontal>

        <p>Branch Angle</p>
        <horizontal>
            <slider style="valSlider" varname="branchAngle" max="180" default="60"/>
            <p style="label" varname='branchAngle'/>
        </horizontal>
        
        <p>Branch Bend</p>
            <horizontal> <slider style="valSlider" varname="branchBend" min="-100" max="100" default="0"/>
            <p style="label" varname='branchBend'/>
        </horizontal>
        
        <colorfield ref="color0" startcol='#00FF00'/>
        <colorfield ref="color1" startcol='#0000FF'/>

        <vertical weight="1" sticky='SEW'>

        <button ref="startbutton" bg='green' activebackground='red4' callback="GenerateFractal">Generate Fractal</button>
        </vertical>
    </vertical>
</horizontal>
</body>
</tkml>
'''

class FractalFrame(tkviewport.OpenGLFrame):
    def __init__(self, window, root, **kw):
        super().__init__(root, **kw)

    def startgl(self):
        refresh2d(self.width, self.height)

    def initgl(self):
        refresh2d(self.width, self.height)

    def redraw(self):
        DrawFractal(self.width, self.height)

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1, 1, 1, 1)


lines = [0,0,0,100,100,0,200,200,0]
colors = [0,0,0,255,1,1]
def DrawFractal(width,height):

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    
    glLineWidth(1)
    glColorPointer(3, GL_UNSIGNED_BYTE, 0, colors)
    glVertexPointer(3, GL_FLOAT, 0, lines)
    
    
    
    glDrawArrays(GL_LINES, 0, len(lines)//3)
    # disable previous instructions
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)


    

def ColorLerp(t):
    return [int((startCol[0] * (1-t) + endCol[0] * t)*255),
            int((startCol[1] * (1-t) + endCol[1] * t)*255),
            int((startCol[2] * (1-t) + endCol[2] * t)*255)]


def MoveTurtle(remaining,startX,startY,angle):
    global lines,colors
    
    if remaining > 0:
        #t.pensize(remaining)

        #t.color(ColorLerp(remaining/branches))
        
        lines.extend([startX,startY,0])

        #first vertex color
        colors.extend(ColorLerp((remaining)/branches))

        
        endX = startX + math.sin(angle*0.0174533) * length * ((remaining+1)/branches)
        endY = startY + math.cos(angle*0.0174533) * length * ((remaining+1)/branches)

        lines.extend([endX,endY,0])

        #second vertex color
        colors.extend(ColorLerp((remaining-1)/branches))



        for i in range(0, splits):
            MoveTurtle(remaining-1,endX,endY,angle + (rotateAngle * i) + offsetAngle - bend)





ended = False
window = tkml.Window(markup,generate=False)
window.custom(FractalFrame)
window.GenerateWindow()

canvas = window.elements['fractalframe']
startColField = window.elements['color0']
endColField = window.elements['color1']

branches = 0
length = 0
splits = 0
angle = 0
bend = 0
inverseSplits = 0
rotateAngle = 0
offsetAngle = 0
startCol = (0, 0, 0)
endCol = (1, 1, 1)

@window.callback
def GenerateFractal():
    global length, branches, angle, splits, bend, t, ended, rotateAngle, offsetAngle, startCol, endCol,lines,colors
    length = window.values['branchLength'].get()
    branches = int(window.values['branchCount'].get())
    splits = int(window.values['branchSplits'].get())
    inverseSplits = 1/splits
    angle = window.values['branchAngle'].get()
    bend = window.values['branchBend'].get()
    window.elements['startbutton'].configure(bg='red')

    startCol = tuple(
        int(startColField.color.strip('#')[i:i+2], 16) for i in (0, 2, 4))
    endCol = tuple(
        int(endColField.color.strip('#')[i:i+2], 16) for i in (0, 2, 4))

    rotateAngle = angle/(splits-1)
    offsetAngle = -angle/2

    startCol = (startCol[0]/255, startCol[1]/255, startCol[2]/255)
    endCol = (endCol[0]/255, endCol[1]/255, endCol[2]/255)


    x = canvas.winfo_width()*0.5

    y = 0

    ended = False
    lines = []
    colors = []
    MoveTurtle(branches,x,y,0)

    ended = True
    canvas._display()
    
    window.elements['startbutton'].configure(bg='green')

window.mainloop()
