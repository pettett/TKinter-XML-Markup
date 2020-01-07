# this demo will show how to use an external pygame script in conjection with tkml

# Original PyMaze can be downloaded from https://www.pygame.org/project/733/1271 - I did not make it

# this version of the game has been modified to include tkinter functionality


# this game has features things that mean tkml must be very changable, like the 10fps framrate meaning updates are performed every 100ms instead of
# 16.66 (17) or 41.66 (42) ms as is normal

#!/usr/bin/python
from sys import argv
import pygame
from pygame.locals import *
from PyMaze import Game, Maze
import tkml


if __name__ == '__main__':

    def Update():
        pygameFrame.screen.fill((0, 0, 255))
        game.loop()
        game.draw_maze()
        game.draw_player()
        pygameFrame.Flip()

    def GenerateNewMaze():
        print("this is a metaphor")
        global game
        game = Game(pygameFrame, 0, '30x40', 1)
        game.start()

    def Up():
        game.move_player('u')

    def Down():
        game.move_player('d')

    def Left():
        game.move_player('l')

    def Right():
        game.move_player('r')

    markup = '''
    <body>
    <horizontal>
    <pygameframe frametime=100 ref="pygameframe" width=800 height=600/>
    <vertical>
        <button label="Reset_Maze" callback="newmaze"/>
        <button label="Up" callback="up"/>
        <horizontal>
        <button label="Left" callback="left"/>
        <button label="Down" callback="down"/>
        <button label="Right" callback="right"/>
        </horizontal>
    </vertical>
    
    </horizontal>
    </body>
    '''

    window = tkml.Window(markup)
    window.callbacks = {
        'newmaze': GenerateNewMaze,
        'down': Down,
        'up': Up,
        'left': Left,
        'right': Right}

    pygameFrame = window.elements['pygameframe']
    pygameFrame.OnUpdate = Update

    # this is a cry for help
    game = Game(pygameFrame, 0, '30x40', 1)
    game.start()
    window.root.after(0, pygameFrame.MainLoop)
    window.mainloop()
