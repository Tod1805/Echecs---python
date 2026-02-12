import sys                                                                      #permet de quitter proprement le programme
import pygame                                                                   #librairie principale pour le jeu
from sound import soundbackground                                               #musique de fond
from sound import soundeffect                                                   #effet sonore

from pygame.locals import *                                                     # Constantes pygame (K_SPACE, QUIT, etc.)

class EtatDeJeu:
        def echiquier(self):
            self.plateau = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]                                                     
#Initialisation de pygame 

pygame.init()                                                                   # demarre tous les modules pygame
LARGEUR = HAUTEUR = 900
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Jeu d'échecs")                                      #Titre du jeu, titre de la fenetre

ej = EtatDeJeu()
encours = True                                                                  #controle de la boucle principal du jeu  


while encours :
    soundbackground()                                                               # joue le son d'arrière plan défini dans sound.py      
    for event in pygame.event.get():                                            #assiotiation  des evenements aux action ( clavier, souris, espace... )
        if event.type == pygame.QUIT:                                           #fermeture de la fenetre
            encours = False
    fenetre.fill((0,0,0))
    pygame.display.flip()                                                       #met à jour l'ecran
pygame.quit()
sys.exit()
