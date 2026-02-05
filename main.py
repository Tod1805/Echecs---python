#Importation

from os import sys  #permet de quitter proprement le programme
import pygame   #librairie principale pour le jeu
from sound import soundbackground   #musique de fon
from sound import soundeffect   #effet sonore

from pygame.locals import *     # Constantes pygame (K_SPACE, QUIT, etc.)

#Initialisation de pygame 

pygame.init()   # demarre tous les modules pygame

pygame.display.set_caption("Jeu d'échecs")  #Titre du jeu, titre de la fenetre

encours = True  #controle de la boucle principal du jeu  
menu = pygame.image.load("images\ecrannoir.png")    #appel de l'image du menu
echiquier = pygame.image.load("images\echiquier.jpg")   #appel de l'image de l'echequier
game_over = pygame.image.load("images\ecranfingameover.jpg")    #appel de l'image game overt
screen = pygame.display.set_mode((900,900))     # Création de la fenêtre du jeu (900x900 pixels)
screen.blit(menu, (0, 0))   # Affichage du menu au lancement

# Chargement de l'image du pion blanc avec transparence
pionblanc = pygame.image.load("images\pionblanc.png").convert_alpha()
# Redimensionnement et création des 8 pions blancs
PB1 = pygame.transform.scale(pionblanc, (60, 60))
PB2 = pygame.transform.scale(pionblanc, (60, 60))
PB3 = pygame.transform.scale(pionblanc, (60, 60))
PB4 = pygame.transform.scale(pionblanc, (60, 60))
PB5 = pygame.transform.scale(pionblanc, (60, 60))
PB6 = pygame.transform.scale(pionblanc, (60, 60))
PB7 = pygame.transform.scale(pionblanc, (60, 60))
PB8 = pygame.transform.scale(pionblanc, (60, 60))

# Création de la police d'écriture
police = pygame.font.SysFont("Arial", 40, bold=True)
# texte qui s'afficherons a l'ecran 
texte_accueil1 = police.render("Bienvenue sur notre jeu d'échecs", True, (255, 255, 255))   #en blanc,sur le menu
texte_accueil2 = police.render("Appuyez sur ESPACE pour jouer", True, (255, 255, 255))    #en blanc,sur le menu
texte_revenir_accueil = police.render("Appuyez sur ENTREE pour revenir à l'accueil", True, (255, 255, 255))     #en blanc, sur la page game over
texte_quitter1 = police.render("Appuyer sur Q pour quitter le jeu", True, (255, 255, 255))     #en blanc,sur la page game over
texte_quitter2 = police.render("Appuyer sur S pour vraiment quitter", True, (255, 255, 255))    #en blanc sur la page d'acceuille

# Affichage des textes du menu
screen.blit(texte_accueil1, (150, 40))
screen.blit(texte_accueil2, (150, 400))

# position des pions mobiles

x = 145     # Position horizontale du pion
y = 607     # Position verticale du pion

# boucle principal du jeu 
while encours :
    pygame.display.flip()   #met à jour l'ecran
    for event in pygame.event.get():    #assiotiation  des evenements aux action ( clavier, souris, espace... )
        #fermeture de la fenetre 
        if event.type == pygame.QUIT:
            encours = False

        #appuie sur une touche du clavier
        if event.type == pygame.KEYDOWN:

            #Lorsque le touche espace est présser, lancement de la partie
            if event.key == pygame.K_SPACE:
                screen.blit(menu, (0, 0))
                screen.blit(echiquier, ((140, 150)))
                screen.blit(texte_quitter1, (130, 50))

                #affichage des pions 
                screen.blit(PB1, (x,y))
                screen.blit(PB2, (220,607))
                screen.blit(PB3, (295,607))
                screen.blit(PB4, (370,607))
                screen.blit(PB5, (445,607))
                screen.blit(PB6, (520,607))
                screen.blit(PB7, (595,607))
                screen.blit(PB8, (670,607))

                #lancement de la musique de fond 
                soundbackground()

            #lorsque l'on presse la touche Q, l'ecran de fin s'affiche 
            if event.key == pygame.K_q:
                screen.blit(menu, (0, 0))
                screen.blit(game_over, (220, 200))
                screen.blit(texte_revenir_accueil, (20, 20))
                screen.blit(texte_quitter2, (90, 100))

            #lorque l'on presse la touche entrer, retour à l'acceuil
            if event.key == pygame.K_RETURN:
                screen.blit(menu, (0, 0))
                screen.blit(texte_accueil1, (150, 40))
                screen.blit(texte_accueil2, (150, 400))

            #pour quitter defenitivement le jeu 
            if event.key == pygame.K_s:
                encours = False

            # Déplacements du pion contrôlé avec les flèches
            if event.key == pygame.K_UP:
                y = y - 75
            if event.key == pygame.K_DOWN:
                y = y + 75
            if event.key == pygame.K_LEFT:
                x = x - 75
            if event.key == pygame.K_RIGHT:
                x = x + 75

            # Redessin de l'échiquier et des pions après déplacement
            screen.blit(echiquier, ((140, 150)))

            soundeffect()    #lancement de l'effet sonore de fin

            screen.blit(PB1, (x,y))
            screen.blit(PB2, (220,607))
            screen.blit(PB3, (295,607))
            screen.blit(PB4, (370,607))
            screen.blit(PB5, (445,607))
            screen.blit(PB6, (520,607))
            screen.blit(PB7, (595,607))
            screen.blit(PB8, (670,607))
            
        pygame.display.flip()   # Mise à jour finale de l'écran

pygame.quit()
sys.exit()
