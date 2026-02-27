import sys                                                                      #permet de quitter proprement le programme
import pygame                                                                   #librairie principale pour le jeu
from sound import soundbackground                                               #musique de fond
from sound import soundeffect                                                   #effet sonore
from sound import soundbackground_tod

from pygame.locals import *                                                     # Constantes pygame (K_SPACE, QUIT, etc.)

IMAGES = {}
def charger_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        chemin = "images/" + piece + ".png"
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(chemin), (90, 90))

class EtatDeJeu:
    def __init__(self):
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
        self.trait_aux_blancs = True
    def mouvement_valide_pion(self, dep, arr, piece):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        direction = 1 if piece[0] == 'w' else -1
        if dep_colonne == arr_colonne and arr_ligne == dep_ligne + direction and self.plateau[arr_ligne][arr_colonne] == "":
            return True
        pion_depart = (piece == 'wp' and dep_ligne == 6) or (piece == 'bp' and dep_ligne == 1)
        if pion_depart and dep_colonne == arr_colonne and arr_ligne == dep_ligne + 2 * direction and self.plateau[dep_ligne + direction][dep_colonne] == "" and self.plateau[arr_ligne][arr_colonne] == "":
            return True
        if abs(dep_colonne - arr_colonne) == 1 and arr_ligne == dep_ligne + direction and self.plateau[arr_ligne][arr_colonne] != "" and self.plateau[arr_ligne][arr_colonne][0] != piece[0]:
            return True
        return False                                            
#Initialisation de pygame 

pygame.init()                                                                   # demarre tous les modules pygame
pygame.font.init()
LARGEUR = HAUTEUR = 800
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Jeu d'échecs")                                      #Titre du jeu, titre de la fenetre

ej = EtatDeJeu()
selection = ()                                                                   #pour stocker la case sélectionnée
clics_joueur = []                                                                #pour stocker les clics du joueur

encours = True                                                                  #controle de la boucle principal du jeu                                                              # joue le son d'arrière plan défini dans sound.py

etat = "MENU"

# Définition des polices
police_titre = pygame.font.SysFont("Verdana", 35, bold=True)
police_instruction = pygame.font.SysFont("Verdana", 25)
police_petite = pygame.font.SysFont("Arial", 18, bold=True)

# Couleurs
BLANC = (255, 255, 255)
GRIS_CLAIR = (200, 200, 200)

NOIR = (0, 0, 0)

taille_case = LARGEUR  // 8

image_menu = pygame.image.load("images/wp.png")
image_menu = pygame.transform.scale(image_menu, (400, 400))
rect_image = image_menu.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))

charger_images() 

while encours :                                                                  
    for event in pygame.event.get():                                            #assiotiation  des evenements aux action ( clavier, souris, espace... )
        if event.type == pygame.QUIT:                                           #fermeture de la fenetre
            encours = False
        if event.type == pygame.MOUSEBUTTONDOWN and etat == "JEU":
                pos = pygame.mouse.get_pos()
                colonne = pos[0] // 100
                ligne = pos[1] // 100
                if selection == (ligne, colonne):
                    selection = ()
                    clics_joueur = []
                else:
                    selection = (ligne, colonne)
                    clics_joueur.append(selection)
                if len(clics_joueur) == 2:
                    dep_ligne, dep_colonne = clics_joueur[0]
                    arr_ligne, arr_colonne = clics_joueur[1]
                    piece = ej.plateau[dep_ligne][dep_colonne]
                    if piece != "":
                        if piece[1] == 'p':
                            valide = ej.mouvement_valide_pion((dep_ligne, dep_colonne), (arr_ligne, arr_colonne), piece)
                        if valide:
                            ej.plateau[arr_ligne][arr_colonne] = piece
                            ej.plateau[dep_ligne][dep_colonne] = ""
                    selection = ()
                    clics_joueur = []
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if etat == "MENU":
                    etat = "JEU"
                    soundbackground_tod()
            if event.key == pygame.K_RETURN:
                if etat == "JEU":
                    etat = "MENU"
                    pygame.mixer.stop()
            if etat == "FIN":
                if event.key == pygame.K_r:
                    ej = EtatDeJeu()
                    etat = "MENU"
                if event.key == pygame.K_q:
                    encours = False
            if event.key == pygame.K_ESCAPE:
                if etat == "JEU":
                    etat = "FIN"
                    pygame.mixer.fadeout(5000)                                    # Fondu de 5 secondes pour la musique de fond
    if etat == "MENU":
        fenetre.fill((0,0,0))                                                     #met à jour l'ecran
        texte_bienvenue = police_titre.render("Bienvenue dans notre jeu d'échecs", True, (255, 255, 255))
        texte_instruction = police_instruction.render("Appuyez sur ESPACE pour jouer", True, (200, 200, 200))

        rect_bienvenue = texte_bienvenue.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 250))
        rect_instruction = texte_instruction.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 200))

        fenetre.blit(image_menu, rect_image)
        fenetre.blit(texte_bienvenue, rect_bienvenue)
        fenetre.blit(texte_instruction, rect_instruction)

    elif etat == "JEU":
        for ligne in range(8):
            for colonne in range (8):
                couleur = NOIR if (ligne + colonne) % 2 == 0 else BLANC
                pygame.draw.rect(fenetre, couleur, pygame.Rect(colonne * taille_case, ligne * taille_case, taille_case, taille_case))
        
        for ligne in range(8):
            for colonne in range(8):
                piece = ej.plateau[ligne][colonne]
                if piece != "":
                    x = (colonne * 100) + 5
                    y = (ligne * 100) + 5
                    fenetre.blit(IMAGES[piece], (x, y))

        message = "ESC : Quitter | ENTREE : Menu"
        texte_message = police_petite.render(message, True, (255, 255, 255))
        
        rect_fond = pygame.Rect(0, HAUTEUR - 30, LARGEUR, 30)
        pygame.draw.rect(fenetre, GRIS_CLAIR, rect_fond)
        rect_texte = texte_message.get_rect(center=(LARGEUR//2, HAUTEUR - 15))
        fenetre.blit(texte_message, rect_texte)
    elif etat == "FIN":
        voile = pygame.Surface((LARGEUR, HAUTEUR))                              # Crée une surface pour le voile
        voile.set_alpha(180)                                                    # Transparence du voile
        voile.fill((0,0,0))                                                     # Couleur du voile (noir)
        fenetre.blit(voile, (0, 0))                                             # Affiche le voile sur la fenêtre  
        texte_fin = police_titre.render("Partie terminée", True, (255, 50, 50))
        texte_rejouer = police_instruction.render("Appuyez sur R pour rejouer ou Q pour quitter", True, (200, 200, 200))

        rect_fin = texte_fin.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50))
        rect_rejouer = texte_rejouer.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))

        fenetre.blit(texte_fin, rect_fin)
        fenetre.blit(texte_rejouer, rect_rejouer)
    pygame.display.flip()
pygame.quit()
sys.exit()
