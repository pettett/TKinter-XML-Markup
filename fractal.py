import tkml
import turtle

markup = '''
<tkml>
<title>Tree Factal</title>
<style ref="label" width=3></style>
<style ref="valSlider" showvalue=0 orient=HORIZONTAL min=1></style>
<body minWidth=800 minHeight=400>
<horizontal>
    <canvas ref="canvas" sticky="NSWE"></canvas>

    <vertical scrolled=True weight=0>
        <p>Tree Fractal</p>
        <p>Branch Length</p>
        <horizontal> <slider style="valSlider" varname="branchLength" max=200 default=80></slider><p style="label" varname='branchLength'></p></horizontal>
        <p>Branch Splits</p>
        <horizontal> <slider style="valSlider" varname="branchSplits" max=10 default=3></slider><p style="label" varname='branchSplits'></p></horizontal>
        <p>Branch Count</p>
        <horizontal> <slider style="valSlider" varname="branchCount" max=20 default=8></slider><p style="label" varname='branchCount'></p></horizontal>
        <p>Branch Angle</p>
        <horizontal> <slider style="valSlider" varname="branchAngle" max=180 default=180></slider><p style="label" varname='branchAngle'></p></horizontal>
        <p>Branch Bend</p>
        <horizontal> <slider style="valSlider" varname="branchBend" min=-100 max=100 default=0></slider> <p style="label" varname='branchBend'></p></horizontal>
        
        <colorfield ref="color0" startcol='#00FF00'/>
        <colorfield ref="color1" startcol='#0000FF'/>

        <vertical weight=1 sticky='SEW'>
        <p>Skip Frames</p>
        <horizontal> <slider style="valSlider" varname="skipFrames" min=1 max=9999 default=256></slider> <p style="label" varname='skipFrames'></p></horizontal>
        <button ref="startbutton" bg='green' activebackground='red4' callback="OnGenerateFractal">Generate Fractal</button>
        </vertical>
    </vertical>
</horizontal>
</body>
</tkml>
'''


def GenerateFractal():
    global length, branches, angle, splits, bend, t, ended, rotateAngle, offsetAngle, startCol, endCol
    length = window.values['branchLength'].get()
    branches = int(window.values['branchCount'].get())
    splits = int(window.values['branchSplits'].get())
    inverseSplits = 1/splits
    angle = window.values['branchAngle'].get()
    bend = window.values['branchBend'].get()
    skips = int(window.values['skipFrames'].get())
    window.elements['startbutton'].configure(bg='red')

    startCol = tuple(
        int(startColField.color.strip('#')[i:i+2], 16) for i in (0, 2, 4))
    endCol = tuple(
        int(endColField.color.strip('#')[i:i+2], 16) for i in (0, 2, 4))

    rotateAngle = angle/(splits)
    offsetAngle = angle/splits

    startCol = (startCol[0]/255, startCol[1]/255, startCol[2]/255)
    endCol = (endCol[0]/255, endCol[1]/255, endCol[2]/255)

    t.reset()
    t.ht()
    t.penup()

    t.setheading(90)
    t.speed(0)
    t._tracer(skips, 0)
    x = canvas.winfo_width()*0.5-382*0.5

    y = -canvas.winfo_height() + 269*0.5
    t.setpos(x, y)
    ended = False
    t.pendown()
    MoveTurtle(branches)
    t.penup()
    ended = True
    window.elements['startbutton'].configure(bg='green')


def ColorLerp(t):
    return (startCol[0] * (1-t) + endCol[0] * t, startCol[1] * (1-t) + endCol[1] * t, startCol[2] * (1-t) + endCol[2] * t)


def MoveTurtle(remaining):

    if remaining > 0:
        t.pensize(remaining)

        t.color(ColorLerp(remaining/branches))

        t.forward(length * ((remaining+1)/branches))

        heading = t.heading()
        for i in range(0, splits):
            if ended:
                return

            t.pendown()

            t.setheading(offsetAngle - (rotateAngle * i) + heading - bend)

            MoveTurtle(remaining-1)

        # offset the effect of the bending from the for loop
        # t.left(offsetAngle)
        t.setheading(heading)
        t.backward(length * ((remaining+1)/branches))
    else:
        t.penup()


ended = False
window = tkml.Window(markup)
canvas = window.elements['canvas']
startColField = window.elements['color0']
endColField = window.elements['color1']
t = turtle.RawTurtle(canvas)

t.penup()
t.pendown()
t.ht()
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
window.callbacks = {"OnGenerateFractal": GenerateFractal}
window.mainloop()
