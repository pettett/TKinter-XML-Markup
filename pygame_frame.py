import pygame
from pygame.locals import *
import tkinter as tk
import os
import platform
import tkml.tkml


def init():
    # import all the current functions so they can be used by tkml
    import pygame
    import tkinter as tk
    import os
    import platform


class PygameFrame(tk.Frame):
    displayFlags = {
        "fullscreen": FULLSCREEN,
        'opengl': OPENGL,
        'hwsurface': HWSURFACE,
        'noframe': NOFRAME}

    def GenerateScreen(self, size):
        self.screen = pygame.display.set_mode(size, self.displayFlags)

    def __init__(self, root, **tags):
        self.frameTime = tags.pop('frametime', 17)
        flags = tags.pop('flags', [])

        super().__init__(root, **tags)
        os.environ['SDL_WINDOWID'] = str(super().winfo_id())

        if platform.system == "Windows":  # allow code to be run cross-platform
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        pygame.display.init()

        # If HDSURFACE or OPENGL enable DOUBLEBUFF
        self.displayFlags = RESIZABLE
        for flag in flags:
            if flag in PygameFrame.displayFlags:
                flag = PygameFrame.displayFlags[flag.lower()]
                self.displayFlags |= flag
                if flag == HWSURFACE or flag == OPENGL:
                    self.displayFlags |= DOUBLEBUF
        self.GenerateScreen((500, 500))
        self.root = root
        self.OnUpdate = None
        self.bind('<Configure>', self.Resize)

    def Resize(self, event):
        size = (event.width, event.height)
        self.GenerateScreen(size)

    def MainLoop(self):
        self.root.after(self.frameTime, self.MainLoop)

        if self.OnUpdate != None:
            self.OnUpdate()

    def Flip(self):
        pygame.display.update()


tkml.TKMLElement("pygameframe", PygameFrame, hasFont=False)

if __name__ == "__main__":
    import math

    def DrawCircle(screen, timeOffset):
        time = pygame.time.get_ticks()*0.001

        circleXOffset = int(math.sin(time + timeOffset)*50)
        circleYOffset = int(math.cos(time + timeOffset)*50)

        pygame.draw.circle(screen, (0, 0, 0),
                           (250 + circleXOffset, 250 + circleYOffset), 25)

    def OnUpdate():
        screen.fill(pygame.Color(255, 255, 255))
        scale = 1.05
        DrawCircle(screen, 0 * scale)
        DrawCircle(screen, 1 * scale)
        DrawCircle(screen, 2 * scale)
        DrawCircle(screen, 3 * scale)
        DrawCircle(screen, 4 * scale)
        DrawCircle(screen, 5 * scale)

        pygame.display.flip()

    root = tk.Tk()
    root.columnconfigure(0, weight=10)
    root.columnconfigure(1, weight=1)
    # creates embed frame for pygame window
    embed = PygameFrame(root, height=500, width=500)
    embed.OnUpdate = OnUpdate
    embed.grid(column=0, sticky='nsew')  # Adds grid
    screen = embed.screen
    buttonwin = tk.Frame(root, width=75, height=500, bg="red")
    buttonwin.grid(column=1, row=0, sticky='nsew')

    root.after(0, embed.MainLoop)
    root.mainloop()
