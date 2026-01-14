import pygame
from pygame.locals import *
pygame.init()

pygame.display.set_caption("Jeu d'échecs") # Créer la fenêtre et lui donner un nom

encours = True
background = pygame.image.load("fondecran.jpg")
echiquier = pygame.image.load("echiquier.jpg")
screen = pygame.display.set_mode((1280,720))
screen.blit(background, (0, 0))

while encours :
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encours = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                screen.blit(echiquier, (0, 0))
pygame.quit()
