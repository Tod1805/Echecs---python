import pygame

# from pygame.locals import *
pygame.init()

pygame.display.set_caption("Jeu d'échecs")

encours = True
menu = pygame.image.load("ecrannoir.png")
echiquier = pygame.image.load("echiquier.jpg")
game_over = pygame.image.load("ecranfingameover.jpg")
screen = pygame.display.set_mode((900,900))
screen.blit(menu, (0, 0))

pionblanc = pygame.image.load("pionblanc.png").convert_alpha()
# PB = pionblanc.resize((50, 50))

police = pygame.font.SysFont("Arial", 40, bold=True)
texte_accueil1 = police.render("Bienvenue sur notre jeu d'échecs", True, (255, 255, 255))
texte_accueil2 = police.render("Appuyez sur ESPACE pour jouer", True, (255, 255, 255))
texte_revenir_accueil = police.render("Appuyez sur ENTREE pour revenir à l'accueil", True, (255, 255, 255))
texte_quitter1 = police.render("Appuyer sur Q pour quitter le jeu", True, (255, 255, 255))
texte_quitter2 = police.render("Appuyer sur S pour vraiment quitter", True, (255, 255, 255))
screen.blit(texte_accueil1, (150, 40))
screen.blit(texte_accueil2, (150, 400))
x = 340
y = 480

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
                screen.blit(pionblanc, (x,y))
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
            #if event.key == pygame.K_LEFT:
            #    y = y - 90
            #if event.key == pygame.K_RIGHT:
             #   y = y - 90
            #if event.key == pygame.K_LEFT:
             #   y = y - 90
            #if event.key == pygame.K_LEFT:
             #   y = y - 90

pygame.quit()

