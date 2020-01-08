
from OpenGL.WGL import PIXELFORMATDESCRIPTOR, ChoosePixelFormat, \
    SetPixelFormat, SwapBuffers, wglCreateContext, wglMakeCurrent
import os
from tkinter import *
from OpenGL.GLU import *

import sys
from OpenGL.GL import *

from objloader import *


from pygame.math import Vector3

# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
from ctypes.wintypes import HDC
from ctypes import WinDLL, c_void_p
# IMPORT OBJECT LOADER
_user32 = WinDLL('user32')
GetDC = _user32.GetDC
GetDC.restype = HDC
GetDC.argtypes = [c_void_p]

pfd = PIXELFORMATDESCRIPTOR()  # Create an open GL Context to be used by tkinter

PFD_TYPE_RGBA = 0
PFD_MAIN_PLANE = 0
PFD_DOUBLEBUFFER = 0x00000001
PFD_DRAW_TO_WINDOW = 0x00000004
PFD_SUPPORT_OPENGL = 0x00000020

pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER
pfd.iPixelType = PFD_TYPE_RGBA
pfd.cColorBits = 24
pfd.cDepthBits = 16
pfd.iLayerType = PFD_MAIN_PLANE


class OpenGLFrame(Frame):
    """ Common code for windows/x11 """

    def __init__(self, root, **kw):
        # Set background to empty string to avoid
        # flickering overdraw by Tk
        kw['bg'] = ""
        self.frameTime = kw.pop('frameTime', 0)

        self.oninitgl = kw.pop('startgl', self.startgl)
        # set delegates for when gl is set and
        self.oninitgl = kw.pop('initgl', self.initgl)
        # for when contents should be drawn
        self.onredraw = kw.pop('redraw', self.redraw)

        Frame.__init__(self, root, ** kw)
        self.bind('<Map>', self.tkMap)
        self.bind('<Configure>', self.tkResize)
        self.bind('<Expose>', self.tkExpose)

        self.cb = None

    def tkMap(self, evt):
          # TODO - Start function goes here
        """" Called when frame goes onto the screen """

        self._wid = self.winfo_id()
        self.tkCreateContext()
        self.startgl()
        self.oninitgl()

    # Binds Open GL to the current frame context using the pixel format setup previously
    def tkCreateContext(self):
        self.__window = GetDC(self.winfo_id())
        pixelformat = ChoosePixelFormat(self.__window, pfd)
        SetPixelFormat(self.__window, pixelformat, pfd)
        self.__context = wglCreateContext(self.__window)
        wglMakeCurrent(self.__window, self.__context)

    def tkMakeCurrent(self):
        if self.winfo_ismapped():
            wglMakeCurrent(self.__window, self.__context)

    def tkSwapBuffers(self):
        if self.winfo_ismapped():
            SwapBuffers(self.__window)  # draws the current frame to the screen

    def tkExpose(self, evt):
        if self.cb:
            self.after_cancel(self.cb)
        self._display()

    def tkResize(self, evt):
        """
        Things to do on window resize:
        Adjust viewport:
            glViewPort(0,0, width, height)
        Adjust projection matrix:
            glFrustum(left * ratio, right * ratio, bottom, top, nearClip,farClip)
        or
            glOrtho(left * ratio, right * ratio, bottom, top, nearClip,farClip)
        or
            gluOrtho2D(left * ratio, right * ratio, bottom, top)
        (assuming that left, right, bottom and top are all equal and
         ratio=width/height)
        """
        self.width, self.height = evt.width, evt.height

        if self.winfo_ismapped():
            glViewport(0, 0, self.width, self.height)
            self.oninitgl()

    def _display(self):
        self.update_idletasks()
        self.tkMakeCurrent()
        self.onredraw()
        self.tkSwapBuffers()
        if self.frameTime > 0:
            self.cb = self.after(self.frameTime, self._display)

    def initgl(self):
       # If the code gets to here there is a problem as it should be set in tags
        raise NotImplementedError

    def redraw(self):
        # If the code gets to here there is a problem
        raise NotImplementedError

    def startgl(self):
        raise NotImplementedError


class CubePreview(OpenGLFrame):
    def __init__(self, root, **tags):

        self.speed = tags.pop('speed', 1)

        self.clearCol = tags.pop('clearCol', (1, 1, 1))
        self.zpos = 5
        self.rotate = self.move = False
        self.hasObj = False
        self.hasClear = False

        self.prevMouse = None
        super().__init__(root, frameTime=24, **tags)

        self.heldKeys = {
            "w":False,"a":False,"s":False,"d":False
            
            }

        self.bind('<B1-Motion>', self.RotateCube)
        self.bind('<ButtonRelease-1>', self.OnMouseRelease)
        self.bind('<KeyPress>', self.StartForward)
        self.bind('<KeyRelease>', self.EndForward)

        self.camera = Camera()
        
    def OnMouseRelease(self, event):
        self.prevMouse = None

    def LoadObject(self):
        if not self.hasObj:
            self.hasObj = True
            self.obj = OBJ("testobject2.obj", swapyz=True)

    def initgl(self):

        # LOAD OBJECT AFTER PYGAME INIT

        fov = 90
        aspect = float(self.width)/float(self.height)

        near = 0.1
        far = 100

        # most obj files expect to be smooth-shaded

        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(fov, aspect, near, far)

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        if not self.hasClear:
            glClearColor(self.clearCol[0],
                         self.clearCol[1], self.clearCol[2], 1)
            self.hasClear = True
        self.LoadObject()

    def startgl(self):
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        # most obj files expect to be smooth-shaded
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)

    def redraw(self):
        if self.hasObj == False:
            self.LoadObject()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.GetInput()
        # RENDER OBJECT

        self.camera.TransformForCamera()
        
        glCallList(self.obj.gl_list)

    def RotateCube(self, event):
        if self.prevMouse == None:
            self.prevMouse = (event.x, event.y)
        rotX = self.prevMouse[0] - event.x
        rotY = event.y - self.prevMouse[1]
        self.camera.rotation.x -= rotX * 0.5
        self.camera.rotation.y += rotY* 0.5
        self.prevMouse = (event.x, event.y)

    def GetInput(self):
        direct = Vector3(0,0,0)
        dt = 0.1
        if self.heldKeys['w']:
            direct += Vector3(0,0,1*dt)
        if self.heldKeys['s']:
            direct += Vector3(0,0,-1*dt)
            
        if self.heldKeys['a']:
            direct += Vector3(1*dt,0,0)
        if self.heldKeys['d']:
            direct += Vector3(-1*dt,0,0)

        self.camera.position += direct.rotate(-self.camera.rotation.y, Vector3(1,0,0)).rotate(-self.camera.rotation.x, Vector3(0,1,0))

    def StartForward(self,event):
        self.heldKeys[event.char] = True
    def EndForward(self,event):
        self.heldKeys[event.char] = False




class Camera(object):
    def __init__(self):
        self.position = Vector3(0,0,-5)
        self.rotation = Vector3(0,0,0)
        
    def TransformForCamera(self):
        glRotate(self.rotation.y, 1, 0, 0)
        glRotate(self.rotation.x, 0, 1, 0)
        glTranslate(self.position.x, self.position.y, self.position.z)
        

if __name__ == "__main__":

    tk = Tk()
    tk.geometry('500x500')

    viewer = CubePreview(tk,height=300, width=200, speed=0, clearCol=(1,1,1,0))
    viewer.pack(fill="both",expand=1)
    viewer.focus_set()
    tk.mainloop()
