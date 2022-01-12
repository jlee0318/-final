import pygame
import random
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1000, 800))

pygame.display.set_caption("Tetris 2P")


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255, 0, 0))
    pygame.display.update()


