import pygame
import tkmlDecoder as decode

pygame.init()

windowWidth = 500
windowHeight = 500

screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)

clock = pygame.time.Clock()

running = True

markup = '''
<horizontal>
    <element color="0-0-255"/>
    <element color="255-0-0"/>
    <element color="0-255-0"/>
</horizontal>
'''
rootElement = decode.Decode(markup)


def DrawElement(screen, element, rect):
    if 'color' in element.tags:
        col = element.tags['color'].split('-')
        col = (int(col[0]), int(col[1]), int(col[2]))
    else:
        col = (255, 255, 255)

    pygame.draw.rect(screen, col, rect)


def DrawHorizontalElements(screen, root, rect):
    childCount = len(root.children)
    for index, child in enumerate(root.children):
        childRect = pygame.Rect(rect.left + rect.width/childCount *
                                index, rect.top, rect.width/childCount, rect.height)
        DrawElement(screen, child, childRect)


while running:

    # main loop
    for event in pygame.event.get():
        print('cheese')
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # entire window is dirty, resize
            windowHeight = event.h
            windowWidth = event.w
            print(windowWidth, windowHeight)
            screen = pygame.display.set_mode(
                (windowWidth, windowHeight), pygame.RESIZABLE)

    screenRect = pygame.Rect(0, 0, windowWidth, windowHeight)

    DrawHorizontalElements(screen, rootElement, screenRect)

    pygame.display.flip()

    clock.tick(60)
