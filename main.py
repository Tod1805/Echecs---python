from os import sys
import pygame
from sound import soundbackground
from sound import soundeffect

from pygame.locals import *
pygame.init()

pygame.display.set_caption("Jeu d'échecs")

encours = True
menu = pygame.image.load("images\ecrannoir.png")
echiquier = pygame.image.load("images\echiquier.jpg")
game_over = pygame.image.load("images\ecranfingameover.jpg")
screen = pygame.display.set_mode((900,900))
screen.blit(menu, (0, 0))

pionblanc = pygame.image.load("images\pionblanc.png").convert_alpha()
PB1 = pygame.transform.scale(pionblanc, (60, 60))
PB2 = pygame.transform.scale(pionblanc, (60, 60))
PB3 = pygame.transform.scale(pionblanc, (60, 60))
PB4 = pygame.transform.scale(pionblanc, (60, 60))
PB5 = pygame.transform.scale(pionblanc, (60, 60))
PB6 = pygame.transform.scale(pionblanc, (60, 60))
PB7 = pygame.transform.scale(pionblanc, (60, 60))
PB8 = pygame.transform.scale(pionblanc, (60, 60))


police = pygame.font.SysFont("Arial", 40, bold=True)
texte_accueil1 = police.render("Bienvenue sur notre jeu d'échecs", True, (255, 255, 255))
texte_accueil2 = police.render("Appuyez sur ESPACE pour jouer", True, (255, 255, 255))
texte_revenir_accueil = police.render("Appuyez sur ENTREE pour revenir à l'accueil", True, (255, 255, 255))
texte_quitter1 = police.render("Appuyer sur Q pour quitter le jeu", True, (255, 255, 255))
texte_quitter2 = police.render("Appuyer sur S pour vraiment quitter", True, (255, 255, 255))
screen.blit(texte_accueil1, (150, 40))
screen.blit(texte_accueil2, (150, 400))
x = 145
y = 607

while encours :
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encours = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.blit(menu, (0, 0))
                screen.blit(echiquier, ((140, 150)))
                screen.blit(texte_quitter1, (130, 50))
                screen.blit(PB1, (x,y))
                screen.blit(PB2, (220,607))
                screen.blit(PB3, (295,607))
                screen.blit(PB4, (370,607))
                screen.blit(PB5, (445,607))
                screen.blit(PB6, (520,607))
                screen.blit(PB7, (595,607))
                screen.blit(PB8, (670,607))
                soundbackground()
            if event.key == pygame.K_q:
                screen.blit(menu, (0, 0))
                screen.blit(game_over, (220, 200))
                screen.blit(texte_revenir_accueil, (20, 20))
                screen.blit(texte_quitter2, (90, 100))
            if event.key == pygame.K_RETURN:
                screen.blit(menu, (0, 0))
                screen.blit(texte_accueil1, (150, 40))
                screen.blit(texte_accueil2, (150, 400))
            if event.key == pygame.K_s:
                encours = False
            if event.key == pygame.K_UP:
                y = y - 75
            if event.key == pygame.K_DOWN:
                y = y + 75
            if event.key == pygame.K_LEFT:
                x = x - 75
            if event.key == pygame.K_RIGHT:
                x = x + 75
            screen.blit(echiquier, ((140, 150)))
            soundeffect()
            screen.blit(PB1, (x,y))
            screen.blit(PB2, (220,607))
            screen.blit(PB3, (295,607))
            screen.blit(PB4, (370,607))
            screen.blit(PB5, (445,607))
            screen.blit(PB6, (520,607))
            screen.blit(PB7, (595,607))
            screen.blit(PB8, (670,607))
        pygame.display.flip()

pygame.quit()
sys.exit()
