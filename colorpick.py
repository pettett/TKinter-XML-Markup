from tkinter import *
import tkml


class Gradient(Canvas):  # TODO - change to openGL Gradient
    '''A gradient frame which uses a canvas to draw the background'''

    def __init__(self, parent, color1="#000000", color2="#FFFFFF", **kwargs):
        self.barWidth = kwargs.pop('barwidth', 4)
        self.widthScalar = 1/self.barWidth
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2

        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        limit = int(width*self.widthScalar)
        if limit == 0:
            limit = int(100*self.widthScalar)

        (r1, g1, b1) = tuple(
            int(self._color1.strip('#')[i:i+2], 16) for i in (0, 2, 4))
        (r2, g2, b2) = tuple(
            int(self._color2.strip('#')[i:i+2], 16) for i in (0, 2, 4))

        r1 *= 257
        g1 *= 257
        b1 *= 257
        r2 *= 257
        g2 *= 257
        b2 *= 257

        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(i*self.barWidth, 0, i*self.barWidth, height,
                             tags=("gradient",), fill=color, width=self.barWidth+1)
        self.lower("gradient")


class ColorPick:
    layout = '''
<body>
        <style ref='colorslider' type=INT orient=HORIZONTAL showvalue=0 callback="OnColorChanged" max=255></style>
        <style ref="colorgradient" barwidth=6 height=10></style>
    <vertical>

        <p>Select Colour</p>
        <horizontal weight=1>
        <vertical weight=1>

        <slider style='colorslider' arg=0 weight=10 varname='r'/>

        <gradient style="colorgradient" ref='redgradient'></gradient>

        <slider style='colorslider' arg=1 weight=10 varname='g'/>

        <gradient style="colorgradient" ref='greengradient'></gradient>

        <slider style='colorslider' arg=2 weight=10 varname='b'/>

        <gradient style="colorgradient" ref='bluegradient'></gradient>

        </vertical>

        <canvas weight=1 height=20 ref='colorpreview'/>

        </horizontal>
        <horizontal>
        <button callback="Submit" label="Submit"/>
        <button callback="Cancel" label="Cancel"/>
        </horizontal>
    </vertical>
    </body>
    '''

    def __init__(self, parent, startCol):
        (r, g, b) = tuple(
            int(startCol.strip('#')[i:i+2], 16) for i in (0, 2, 4))
        self.startColor = startCol
        top = self.top = Toplevel(parent)
        window = tkml.Window(self.layout, top)
        window.callbacks = {"OnColorChanged": self.SetNewColor,
                            "Submit": self.Submit,
                            "Cancel": self.Cancel}
        self.r = window.values['r']
        self.g = window.values['g']
        self.b = window.values['b']
        self.redGradient = window.elements['redgradient']
        self.blueGradient = window.elements['bluegradient']
        self.greenGradient = window.elements['greengradient']
        self.colorPreview = window.elements['colorpreview']

        # setting colors defaults correct color and activates trace command that initalizes gradients
        self.r.set(r)
        self.g.set(g)
        self.b.set(b)
        self.SetNewColor(-1)  # update for all values changed

    def SetNewColor(self, changed):
        r = self.r.get()
        g = self.g.get()
        b = self.b.get()

        self.UpdateGradients(changed, r, g, b)

    def UpdateGradients(self, changed, r, g, b):
        self.color = '#%02x%02x%02x' % (
            r, g, b)

        if changed != 0:
            self.redGradient._color1 = '#00%02x%02x' % (
                g, b)
            self.redGradient._color2 = '#ff%02x%02x' % (
                g, b)
            self.redGradient._draw_gradient()
        if changed != 1:
            self.greenGradient._color1 = '#%02x00%02x' % (
                r, b)
            self.greenGradient._color2 = '#%02xff%02x' % (
                r, b)
            self.greenGradient._draw_gradient()
        if changed != 2:
            self.blueGradient._color1 = '#%02x%02x00' % (
                r, g)
            self.blueGradient._color2 = '#%02x%02xff' % (
                r, g)
            self.blueGradient._draw_gradient()

        self.colorPreview.configure(bg=self.color)

    def Submit(self):
        self.top.destroy()

    def Cancel(self):
        self.color = self.startColor
        self.top.destroy()


class ColorField(Button):
    def OnChange(self):
        pass

    def __init__(self, parent, **kwargs):
        self.root = parent
        self.color = kwargs.pop('startcol', '#FFFFFF')
        self.OnChangeEvent = self.OnChange
        super().__init__(parent, command=self.OnInput, bg=self.color,
                         activebackground=self.color, text="Change Color", **kwargs)

    @property
    def NormalizedColor(self):
        (r, g, b) = tuple(
            int(self.color.strip('#')[i:i+2], 16) for i in (0, 2, 4))
        return (r/255, g/255, b/255)

    @NormalizedColor.setter
    def NormalizedColor(self, color):
        r = int(color[0]*255)
        g = int(color[1]*255)
        b = int(color[2]*255)

        self.color = '#%02x%02x%02x' % (
            r, g, b)
        super().configure(bg=self.color, activebackground=self.color)

    def OnInput(self):
        d = ColorPick(self.root, self.color)
        self.root.wait_window(d.top)

        self.color = d.color
        self.OnChangeEvent()
        super().configure(bg=self.color, activebackground=self.color)


if __name__ == "__main__":
    root = Tk()

    Button(root, text="Hello!").pack()
    ColorField(root).pack()
    root.mainloop()
