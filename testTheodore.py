import sys                                                                      # permet de quitter proprement le programme
import pygame                                                                   # librairie principale pour le jeu
from sound import soundbackground, vibration, soundeffect, soundbackground_tod  # importe les fonctions de son définies dans sound.py

from pygame.locals import *                                                     # Constantes pygame (K_SPACE, QUIT, etc.)

IMAGES = {}
def charger_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        chemin = "images/" + piece + ".png"
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(chemin), (90, 90))

class EtatDeJeu: # Classe pour représenter l'état du jeu d'échecs, y compris le plateau, le trait aux blancs, le compteur de 50 coups et l'historique des positions
    def __init__(self): # Initialise l'état du jeu avec le plateau de départ, le trait aux blancs, le compteur de 50 coups et l'historique des positions
        self.plateau = [ # Le plateau de jeu est représenté par une liste de listes, où chaque élément est une chaîne de caractères représentant la pièce présente sur la case ou une chaîne vide pour les cases vides
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], # Les pièces noires sont représentées par des chaînes de caractères commençant par 'b' et les pièces blanches par des chaînes commençant par 'w'
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], # Les pions sont représentés par 'p', les tours par 'R', les cavaliers par 'N', les fous par 'B', la dame par 'Q' et le roi par 'K'
            ["", "", "", "", "", "", "", ""],# Les cases vides sont représentées par des chaînes de caractères vides
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], # Les pièces blanches sont représentées par des chaînes de caractères commençant par 'w' et les pièces noires par des chaînes commençant par 'b'
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],# Les pions sont représentés par 'p', les tours par 'R', les cavaliers par 'N', les fous par 'B', la dame par 'Q' et le roi par 'K'
        ]
        self.trait_aux_blancs = True # True si c'est au tour des blancs, False pour les noirs
        self.compteur_50_coups = 0 # Compteur pour la règle des 50 coups
        self.historique_position = [] # Historique des mouvements pour la nulle par répétition
    def mouvement_valide_pion(self, dep, arr, piece):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        direction = - 1 if piece[0] == 'w' else 1
        if dep_colonne == arr_colonne and arr_ligne == dep_ligne + direction and self.plateau[arr_ligne][arr_colonne] == "":
            return True
        pion_depart = (piece == 'wp' and dep_ligne == 6) or (piece == 'bp' and dep_ligne == 1)
        if pion_depart and dep_colonne == arr_colonne and arr_ligne == dep_ligne + 2 * direction and self.plateau[dep_ligne + direction][dep_colonne] == "" and self.plateau[arr_ligne][arr_colonne] == "":
            return True
        if abs(dep_colonne - arr_colonne) == 1 and arr_ligne == dep_ligne + direction and self.plateau[arr_ligne][arr_colonne] != "" and self.plateau[arr_ligne][arr_colonne][0] != piece[0]:
            return True
        return False
    def mouvement_valide_cavalier(self, dep, arr):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        diff_ligne = abs(arr_ligne - dep_ligne)
        diff_colonne = abs(arr_colonne - dep_colonne)
        return (diff_ligne == 2 and diff_colonne == 1) or (diff_ligne == 1 and diff_colonne == 2)
    def mouvement_valide_fou(self, dep, arr):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        if abs(arr_ligne - dep_ligne) == abs(arr_colonne - dep_colonne):
            return self.chemin_libre(dep, arr)
        return False
    def chemin_libre(self, dep, arr):
        d_ligne = 0 if arr[0] == dep[0] else (1 if arr[0] > dep[0] else -1)
        d_colonne = 0 if arr[1] == dep[1] else (1 if arr[1] > dep[1] else -1)
        current_ligne, current_colonne = dep[0] + d_ligne, dep[1] + d_colonne
        while (current_ligne, current_colonne) != (arr[0], arr[1]):
            if self.plateau[current_ligne][current_colonne] != "":
                return False
            current_ligne += d_ligne
            current_colonne += d_colonne
        return True
    def mouvement_valide_tour(self, dep, arr):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        if dep_ligne == arr_ligne or dep_colonne == arr_colonne:
            return self.chemin_libre(dep, arr)
        return False
    def simuler_mouvement_et_verifier_echec(self, dep, arr, couleur):
        piece_depart = self.plateau[dep[0]][dep[1]]
        piece_arrivee = self.plateau[arr[0]][arr[1]]
        self.plateau[arr[0]][arr[1]] = piece_depart
        self.plateau[dep[0]][dep[1]] = ""
        en_echec = self.est_en_echec(couleur)
        self.plateau[dep[0]][dep[1]] = piece_depart
        self.plateau[arr[0]][arr[1]] = piece_arrivee
        return en_echec
    def mouvement_valide_roi(self, dep, arr):
        dep_ligne, dep_colonne = dep
        arr_ligne, arr_colonne = arr
        
        diff_ligne = abs(arr_ligne - dep_ligne)
        diff_colonne = abs(arr_colonne - dep_colonne)
        return diff_ligne <= 1 and diff_colonne <= 1
    def mouvements_valide(self, ligne, colonne):
        mouvements = []
        piece = self.plateau[ligne][colonne]
        if piece == "":
            return mouvements
        for r in range(8):
            for c in range(8):
                valide = False
                piece_destination = self.plateau[r][c]
                if piece_destination != "" and piece_destination[0] == piece[0]:
                    continue
                type_p = piece[1]
                if type_p == 'p':
                    valide = self.mouvement_valide_pion((ligne, colonne), (r, c), piece)
                elif type_p == 'N':
                    valide = self.mouvement_valide_cavalier((ligne, colonne), (r, c))
                elif type_p == 'B':           
                    valide = self.mouvement_valide_fou((ligne, colonne), (r, c))
                elif type_p == 'R':
                    valide = self.mouvement_valide_tour((ligne, colonne), (r, c))
                elif type_p == 'Q':
                    valide = self.mouvement_valide_fou((ligne, colonne), (r, c)) or self.mouvement_valide_tour((ligne, colonne), (r, c))
                elif type_p == 'K':
                    valide = self.mouvement_valide_roi((ligne, colonne), (r, c))
                if valide:
                    couleur_joueur = piece[0]
                    if not self.simuler_mouvement_et_verifier_echec((ligne, colonne), (r, c), couleur_joueur):
                        mouvements.append((r, c))
        return mouvements
    def est_en_echec(self, couleur_roi):
        roi_position = None
        chercher = couleur_roi + "K"
        for r in range(8):
            for c in range(8):
                if self.plateau[r][c] == chercher:
                    roi_position = (r, c)
                    break
            if roi_position:
                break
        if not roi_position:
            return False
        couleur_ennemie = 'b' if couleur_roi == 'w' else 'w'
        for r in range(8):
            for c in range(8):
                piece = self.plateau[r][c]
                if piece != "" and piece[0] == couleur_ennemie:
                    mouvements_possibles = self.get_mouvements_physiques(r, c)
                    if roi_position in mouvements_possibles:
                        return True
        return False
    def get_mouvements_physiques(self, ligne, colonne):
        mouvements = []
        piece = self.plateau[ligne][colonne]
        if piece == "":
            return mouvements
        for r in range(8):
            for c in range(8):
                valide = False
                piece_destination = self.plateau[r][c]
                if piece_destination != "" and piece_destination[0] == piece[0]:
                    continue
                type_p = piece[1]
                if type_p == 'p':
                    valide = self.mouvement_valide_pion((ligne, colonne), (r, c), piece)
                elif type_p == 'N':
                    valide = self.mouvement_valide_cavalier((ligne, colonne), (r, c))
                elif type_p == 'B':           
                    valide = self.mouvement_valide_fou((ligne, colonne), (r, c))
                elif type_p == 'R':
                    valide = self.mouvement_valide_tour((ligne, colonne), (r, c))
                elif type_p == 'Q':
                    valide = self.mouvement_valide_fou((ligne, colonne), (r, c)) or self.mouvement_valide_tour((ligne, colonne), (r, c))
                elif type_p == 'K':
                    valide = self.mouvement_valide_roi((ligne, colonne), (r, c))
                if valide:
                    mouvements.append((r, c))
        return mouvements
    def est_echec_et_mat(self, couleur):
        if not self.est_en_echec(couleur):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.plateau[r][c]
                if piece != "" and piece[0] == couleur:
                    mouvements = self.mouvements_valide(r, c)
                    if len(mouvements) > 0:
                        return False
        return True
    def est_pat(self, couleur):
        if self.est_en_echec(couleur):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.plateau[r][c]
                if piece != "" and piece[0] == couleur:
                    mouvements = self.mouvements_valide(r, c)
                    if len(self.mouvements_valide(r, c)) > 0:
                        return False
        return True
    def enregistrer_position(self):
        position_actuelle = tuple(tuple(row) for row in self.plateau)
        self.historique_position.append(position_actuelle)
    def est_triple_repetition(self):
        if not self.historique_position:
            return False
        position_actuelle = self.historique_position[-1]
        occurrences = self.historique_position.count(position_actuelle)

        return occurrences >= 3
    def est_manque_de_matériel(self):
        pieces_blanches = []
        pieces_noires = []
        for ligne in range(8):
            for colonne in range (8):
                piece = self.plateau[ligne][colonne]
                if piece != "":
                    if piece[0] == 'w':
                        pieces_blanches.append(piece[1])
                    else:
                        pieces_noires.append(piece[1])
        if len(pieces_blanches) == 1 and len(pieces_noires) == 1:
            return True # Roi contre roi
        if len(pieces_blanches) <= 2 and len(pieces_noires) <= 2:
            unique_blanc = [p for p in pieces_blanches if p != 'K']
            unique_noir = [p for p in pieces_noires if p != 'K']
            if (not unique_blanc and unique_noir in [['N'], ['B']]) or (not unique_noir and unique_blanc in [['N'], ['B']]):
                return True # Roi contre roi + cavalier ou fou
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

gagnant = ""
historique_positions = []

debut_clignotement = 0
case_roi_en_echec = None

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
                    piece_depart = ej.plateau[dep_ligne][dep_colonne]
                    piece_arrivee = ej.plateau[arr_ligne][arr_colonne]

                    if piece_depart !="":
                        tour_correct = (ej.trait_aux_blancs and piece_depart[0] == 'w') or (not ej.trait_aux_blancs and piece_depart[0] == 'b')
                        if tour_correct:
                            if piece_arrivee != "" and piece_depart[0] == piece_arrivee[0]:
                                valide = False
                            else:
                                type_piece = piece_depart[1]
                                if type_piece == 'p':
                                    valide = ej.mouvement_valide_pion((dep_ligne, dep_colonne), (arr_ligne, arr_colonne), piece_depart)
                                elif type_piece == 'N':
                                    valide = ej.mouvement_valide_cavalier((dep_ligne, dep_colonne), (arr_ligne, arr_colonne))
                                elif type_piece == 'B':
                                    valide = ej.mouvement_valide_fou((dep_ligne, dep_colonne), (arr_ligne, arr_colonne))
                                elif type_piece == 'R':
                                    valide = ej.mouvement_valide_tour((dep_ligne, dep_colonne), (arr_ligne, arr_colonne))
                                elif type_piece == 'Q':
                                    valide = ej.mouvement_valide_fou((dep_ligne, dep_colonne), (arr_ligne, arr_colonne)) or ej.mouvement_valide_tour((dep_ligne, dep_colonne), (arr_ligne, arr_colonne))
                                elif type_piece == 'K':
                                    valide = ej.mouvement_valide_roi((dep_ligne, dep_colonne), (arr_ligne, arr_colonne))
                            if valide:
                                if ej.simuler_mouvement_et_verifier_echec((dep_ligne, dep_colonne), (arr_ligne, arr_colonne), piece_depart[0]):
                                    valide = False
                            if valide:
                                ej.plateau[arr_ligne][arr_colonne] = piece_depart
                                ej.plateau[dep_ligne][dep_colonne] = ""
                                ej.enregistrer_position()
                                ej.trait_aux_blancs = not ej.trait_aux_blancs
                                joueur_actuel = 'w' if ej.trait_aux_blancs else 'b'
                                if ej.est_echec_et_mat(joueur_actuel):
                                    print(f"Echec et mat ! Les {'Blancs' if joueur_actuel == 'b' else 'Noirs'} ont gagné !")
                                    etat = "FIN"
                                    gagnant = 'Noirs' if joueur_actuel == 'w' else 'Blancs'
                                elif ej.est_pat(joueur_actuel):
                                    etat = "FIN"
                                    gagnant = "Pat"
                                elif ej.compteur_50_coups >= 100: # 50 coups pour chaque joueur sans déplacement de pion ni capture
                                    etat = "FIN"
                                    gagnant = "50 coups"
                                elif ej.est_triple_repetition():
                                    etat = "FIN"
                                    gagnant = "Répétition"
                                elif ej.est_manque_de_matériel(): # Vérifie les conditions de nulle par manque de matériel (roi contre roi, roi contre roi + fou ou roi contre roi + cavalier)
                                    etat = "FIN"
                                    gagnant = "Manque de matériel"
                                if (piece_depart == "wp" and arr_ligne == 0) or (piece_depart == "bp" and arr_ligne == 7):
                                    etat = "PROMOTION"
                                    possibilites_promotion = (arr_ligne, arr_colonne)
                                    couleur_promue = 'w' if piece_depart[0] == 'w' else 'b'
                                if ej.simuler_mouvement_et_verifier_echec((dep_ligne, dep_colonne), (arr_ligne, arr_colonne), piece_depart[0]):
                                    valide = False
                                    print("Mouvement invalide : met le roi en échec")
                                if piece_arrivee != "":
                                    soundeffect()
                                est_capture = (piece_arrivee != "")
                                est_pion = (piece_depart[1] == 'p')
                                if est_capture or est_pion:
                                    ej.compteur_50_coups = 0 # Réinitialise le compteur de 50 coups si une pièce a été capturée ou si un pion
                                else:
                                    ej.compteur_50_coups += 1 # Ajoute 1 au compteur de 50 coups si aucun pion n'a été déplacé et aucune pièce n'a été capturée

                    selection = ()
                    clics_joueur = []
                couleur_suivante = 'w' if ej.trait_aux_blancs else 'b'
                if ej.est_en_echec(couleur_suivante):
                    debut_clignotement = pygame.time.get_ticks()
                    for r in range(8):
                        for c in range(8):
                            if ej.plateau[r][c] == couleur_suivante + "K":
                                case_roi_en_echec = (r, c)
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
                    pygame.mixer.fadeout(10000)                                    # Fondu de 10 secondes pour la musique de fond
            if etat == "PROMOTION":
                if event.key == pygame.K_q:
                    ej.plateau[possibilites_promotion[0]][possibilites_promotion[1]] = couleur_promue + "Q"
                    ej.trait_aux_blancs = not ej.trait_aux_blancs
                    etat = "JEU"
                elif event.key == pygame.K_r:
                    ej.plateau[possibilites_promotion[0]][possibilites_promotion[1]] = couleur_promue + "R"
                    ej.trait_aux_blancs = not ej.trait_aux_blancs
                    etat = "JEU"
                elif event.key == pygame.K_b:
                    ej.plateau[possibilites_promotion[0]][possibilites_promotion[1]] = couleur_promue + "B"
                    ej.trait_aux_blancs = not ej.trait_aux_blancs
                    etat = "JEU"
                elif event.key == pygame.K_n:
                    ej.plateau[possibilites_promotion[0]][possibilites_promotion[1]] = couleur_promue + "N"
                    ej.trait_aux_blancs = not ej.trait_aux_blancs
                    etat = "JEU"
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
        if selection != ():
            ligne, colonne = selection
            possibles = ej.mouvements_valide(ligne, colonne)
            for m in possibles:
                m_ligne, m_colonne = m

                couleur_point = (100, 100, 100)
                rayon = 15

                if ej.plateau[m_ligne][m_colonne] !="":
                    couleur_point = (255, 50, 50)
                    rayon = 15

                centre_x = m_colonne * 100 + 50
                centre_y = m_ligne * 100 + 50
                pygame.draw.circle(fenetre, couleur_point, (centre_x, centre_y), rayon)
        couleur_actuelle = "w" if ej.trait_aux_blancs else "b"
        if ej.est_echec_et_mat(couleur_actuelle):
            etat = "FIN"
            gagnant = 'Blancs' if not ej.trait_aux_blancs else 'Noirs'
            texte_echec_mat = police_titre.render("Échec et mat ! Gagnant : " + gagnant, True, (255, 50, 50))
            rect_echec_mat = texte_echec_mat.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
            pygame.draw.rect(fenetre, (0, 0, 0), rect_echec_mat.inflate(20, 20))
            fenetre.blit(texte_echec_mat, rect_echec_mat)
            pygame.mixer.fadeout(10000)                                                                           # Fondu de 10 secondes pour la musique de fond
        elif ej.est_en_echec(couleur_actuelle):
            texte_echec = police_titre.render("Échec au roi " + ("Blancs" if couleur_actuelle == 'w' else "Noirs"), True, (255, 50, 50))
            rect_echec = texte_echec.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            pygame.draw.rect(fenetre, (0, 0, 0), rect_echec.inflate(20, 20))
            fenetre.blit(texte_echec, rect_echec)
        message = "ESC : Quitter | ENTREE : Menu"
        texte_message = police_petite.render(message, True, (255, 255, 255))
        
        rect_fond = pygame.Rect(0, HAUTEUR - 30, LARGEUR, 30)
        pygame.draw.rect(fenetre, GRIS_CLAIR, rect_fond)
        rect_texte = texte_message.get_rect(center=(LARGEUR//2, HAUTEUR - 15))
        fenetre.blit(texte_message, rect_texte)
        couleur_tour = "Blancs" if ej.trait_aux_blancs else "Noirs"
        texte_tour = police_petite.render(f"Tour des {couleur_tour}", True, (255, 255, 255))
        pygame.draw.rect(fenetre, (50, 50, 50), (5, 5, 120, 25))
        fenetre.blit(texte_tour, (10, 8))
    if case_roi_en_echec:
        temps_ecoule = pygame.time.get_ticks() - debut_clignotement
        if temps_ecoule < 2000:                                                                # Clignote pendant 2 secondes
            if (temps_ecoule // 250) % 2 == 0:                                                 # Alterne entre visible et invisible toutes les 250 ms
                r, c = case_roi_en_echec                                                       # Affiche un clignotement rouge sur la case du roi en échec
                s = pygame.Surface((100, 100))                                                 # Crée une surface pour le clignotement
                s.set_alpha(128)                                                               # Transparence
                s.fill((255, 0, 0))                                                            # Couleur rouge
                fenetre.blit(s, (c * 100, r * 100))                                            # Affiche le clignotement sur la case du roi en échec
                vibration()                                                                    # Déclenche un son de vibration pour renforcer l'effet d'échec
        else: 
            case_roi_en_echec = None                                                           # Arrête le clignotement après 2 secondes

    
    
    elif etat == "PROMOTION":
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
    
        overlay = pygame.Surface((400, 200))                                                   # Crée une surface pour l'overlay de promotion
        overlay.set_alpha(220)                                                                 # Transparence de l'overlay
        overlay.fill((50, 50, 50))                                                             # Couleur de l'overlay (gris foncé)
        fenetre.blit(overlay, (200, 300))                                                      # Affiche l'overlay de promotion au centre de la fenêtre
    
        options = ["Dame Q", "Tour R", "Fou B", "Cavalier N"]                                  # Options de promotion pour la pièce promue
        for i, option in enumerate(options):                                                   # Affiche les options de promotion pour la pièce promue
            texte_option = police_petite.render(option, True, (255, 255, 255))                 # Affiche les options de promotion en blanc
            fenetre.blit(texte_option, (250, 320 + i * 40))                                    # Affiche les options de promotion dans la fenêtre

    elif etat == "FIN":
        voile = pygame.Surface((LARGEUR, HAUTEUR))                                             # Crée une surface pour le voile
        voile.set_alpha(180)                                                                   # Transparence du voile
        voile.fill((0,0,0))                                                                    # Couleur du voile (noir)
        fenetre.blit(voile, (0, 0))                                                            # Affiche le voile sur la fenêtre  
        
        couleur_titre = (200, 200, 200) # Attribue la couleur gris à la variable couleur_titre

        if "Pat" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Match nul par pat !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif "Répétition" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Match nul par répétition !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif "50 coups" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Match nul par règle des 50 coups !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif gagnant in ["Blancs", "Noirs"]:
            titre = "ECHEC ET MAT !"
            couleur_titre = (255, 215, 0)
            sous_titre = f"Victoire des {gagnant} !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif "Manque de matériel" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Match nul par manque de matériel !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond

        texte_titre = police_titre.render(titre, True, couleur_titre)
        rect_titre = texte_titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 90))
        texte_vainqueur = police_instruction.render(sous_titre, True, (255, 255, 255)) 
        rect_vainqueur = texte_vainqueur.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 40))



        texte_fin = police_titre.render("Partie terminée", True, (255, 50, 50)) # Affiche le message de fin en rouge vif
        texte_rejouer = police_instruction.render("Appuyez sur R pour rejouer ou Q pour quitter", True, (200, 200, 200))# Affiche les instructions pour rejouer ou quitter en gris clair
        rect_fin = texte_fin.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 200)) # Dessine un rectangle du message de fin
        rect_rejouer = texte_rejouer.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50)) # Dessine un rectangle des instructions pour rejouer ou quitter

        fenetre.blit(texte_titre, rect_titre)
        fenetre.blit(texte_vainqueur, rect_vainqueur)
        fenetre.blit(texte_fin, rect_fin) # Affiche le message de fin
        fenetre.blit(texte_rejouer, rect_rejouer) # Affiche les instructions pour rejouer ou quitter
    couleur_actuelle = "white" if ej.trait_aux_blancs else "black" # Détermine la couleur du joueur actuel
    if ej.est_en_echec(couleur_actuelle): # Affiche un message d'échec au roi du joueur actuel
        texte_echec = police_titre.render("Échec au roi " + couleur_actuelle, True, (255, 50, 50)) # Affiche le message d'échec en rouge vif
        rect_echec = texte_echec.get_rect(center=(LARGEUR//2, HAUTEUR//2)) # Affiche le rectangle du message d'échec
        pygame.draw.rect(fenetre, (0, 0, 0), (rect_echec.x - 10, rect_echec.y - 10, rect_echec.width + 20, rect_echec.height + 20)) # Dessine un rectangle noir derrière le message d'échec pour le faire ressortir
        fenetre.blit(texte_echec, rect_echec) # Affiche le message d'échec au roi du joueur actuel
    pygame.display.flip() # Met à jour l'affichage de la fenêtre
    
pygame.quit() # Quitte pygame proprement
sys.exit() # Quitte le programme proprement
