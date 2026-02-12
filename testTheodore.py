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
pygame.font.init()
LARGEUR = HAUTEUR = 1000
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Jeu d'échecs")                                      #Titre du jeu, titre de la fenetre

ej = EtatDeJeu()
encours = True                                                                  #controle de la boucle principal du jeu  

soundbackground()                                                              # joue le son d'arrière plan défini dans sound.py

etat = "MENU"

COULEUR_1 = (0, 0, 0)
COULEUR_2 = (255, 255, 255)

taille_case = LARGEUR  // 8

while encours :                                                                  
    for event in pygame.event.get():                                            #assiotiation  des evenements aux action ( clavier, souris, espace... )
        if event.type == pygame.QUIT:                                           #fermeture de la fenetre
            encours = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if etat == "MENU":
                    etat = "JEU"

    
    fenetre.fill((0,0,0))                                                      #met à jour l'ecran
    
    if etat == "MENU":
        police = pygame.font.SysFont("Arial", 30, bold=True)
        
        texte_bienvenue = police.render("Bienvenue dans notre jeu d'échecs", True, (255, 255, 255))
        texte_instruction = police.render("Appuyez sur ESPACE pour commencer", True, (200, 200, 200))

        fenetre.blit(texte_bienvenue, (LARGEUR//2 - 200, HAUTEUR//2 - 50))
        fenetre.blit(texte_instruction, (LARGEUR//2 - 220, HAUTEUR//2 + 20))

    elif etat == "JEU":
        for ligne in range(8):
            for colonne in range (8):
                couleur = COULEUR_1 if (ligne + colonne) % 2 == 0 else COULEUR_2
                pygame.draw.rect(fenetre, couleur, pygame.Rect(colonne * taille_case, ligne * taille_case, taille_case, taille_case))
        pygame.display.flip()
pygame.quit()
sys.exit()
