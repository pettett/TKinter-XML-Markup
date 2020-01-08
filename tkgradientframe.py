
from math import *
import glshaderloader as glsl

import tkinter
import tkviewport
from OpenGL.GL import *
import colorsys
import tkml



class GradientFrame(tkviewport.OpenGLFrame):
    
    def __init__(self,w, root, **kw):
        self.color = kw.pop("color","red")
        self.direction = kw.pop("direction","quad")
        self.bands = kw.pop("bands",2)
        self.base = (1,1,1)
        super().__init__(root,frameTime=10, **kw)
        self.tris = [0 ,
                              1 ,
                              2 ,
                              
                              2 ,
                              1 ,
                              3]

        
        
    def GenerateColors(self,r,g,b):
        self.base = (r,g,b)
        

            
    def CalculateVerts(self):
        heightChange = self.height/(self.bands-1)
        self.verts = []
        #add a line of verts for every band in the list
        for y in range(self.bands):
            self.verts.extend([self.width,y*heightChange-1,0,
                            -1,y*heightChange-1,0])

        
    def startgl(self):
        if self.color == "red":
            out = "vec3(uvx,base.y,base.z)"
        elif self.color == "green":
            out = "vec3(base.x,uvx,base.z)"
        elif self.color == "blue":
            out = "vec3(base.x,base.y,uvx)"
        
        
        self.shader = glsl.Program([glsl.ShaderFragment(
"""
#version 330 core
out vec4 FragColor;
  
in vec4 vertexColor; // the input variable from the vertex shader (same name and same type)  

void main()
{
    FragColor = vertexColor;
}
"""),glsl.ShaderVertex("""
#version 330 core
layout (location = 0) in vec3 aPos; // the position variable has attribute position 0


out vec4 vertexColor; // specify a color output to the fragment shader
uniform vec3 base = vec3(1,1,1);

void main()
{
    float uvx = (aPos.x+1)*0.5;
    
    
    gl_Position = vec4(aPos, 1.0);
    
    vertexColor = vec4("""+out+""", 1.0); // set the output variable to a dark-red color
}""")])
        
        self.refresh2d()
    def initgl(self):
        self.refresh2d()

    def redraw(self):
        #on redraw only called when size changed so replace quad edges
        self.CalculateVerts()
        self.RedrawGradient()
        

    def refresh2d(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(1, 0, 1, 1)
        
    def RedrawGradient(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glViewport(0,0,self.width,self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)

        
        glsl.Program.use(self.shader)
        self.shader.pass_vec3("base",self.base)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        
        glVertexPointer(3, GL_FLOAT, 0, self.verts)

        glDrawElements(GL_TRIANGLES, 6,GL_UNSIGNED_BYTE,self.tris)
        
        glDisableClientState(GL_VERTEX_ARRAY)

class ColorPick:
    layout = '''
<body>
        <style ref='colorslider' type="INT" orient="horizontal" showvalue="0" callback="OnColorChanged" max="255"></style>
        <style ref="colorgradient" height="10"></style>
    <vertical>

        <p>Select Colour</p>
        <horizontal weight="1">
        <vertical weight="1">

        <slider style='colorslider' arg="0" varname='r'/>

        <GradientFrame style="colorgradient" color="red" height="150" ref='redgradient' weight="1"/>

        <slider style="colorslider" arg="1" varname="g"/>

        <GradientFrame style="colorgradient" color="green" height="150" weight="1" ref='greengradient'></GradientFrame>

        <slider style='colorslider' arg="2" varname='b'/>

        <GradientFrame style="colorgradient" color="blue" height="150" weight="1" ref='bluegradient'></GradientFrame>

        </vertical>

        <canvas weight="1" height="20" width="50" ref='colorpreview'/>

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
        top = self.top = tkinter.Toplevel(parent)
        
        window = tkml.Window(self.layout, root=top,generate=False)
        
        window.customs["GradientFrame"] = GradientFrame
        window.GenerateWindow()
        

        
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

        window.callback(self.OnColorChanged)
        window.callback(self.Submit)
        window.callback(self.Cancel)


        self.OnColorChanged(-1)
    
    def OnColorChanged(self, changed):
        r = self.r.get()
        g = self.g.get()
        b = self.b.get()

        self.UpdateGradients(changed, r, g, b)

    def UpdateGradients(self, changed, r, g, b):
        self.color = '#%02x%02x%02x' % (
            r, g, b)


        self.redGradient.GenerateColors(r/255,g/255,b/255)

            

        self.greenGradient.GenerateColors(r/255,g/255,b/255)


        self.blueGradient.GenerateColors (r/255,g/255,b/255)

        self.colorPreview.configure(bg=self.color)
    
    def Submit(self):
        self.top.destroy()

    def Cancel(self):
        self.color = self.startColor
        self.top.destroy()


class ColorField(tkinter.Button):
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
    root = tkinter.Tk()

    tkinter.Button(root, text="Hello!").pack()
    ColorField(root).pack()
    root.mainloop()

