import sys                                                                      # permet de quitter proprement le programme
import pygame                                                                   # librairie principale pour le jeu
from sound import soundbackground, vibration, soundeffect, soundbackground_tod  # importe les fonctions de son définies dans sound.py
from classes import EtatDeJeu
from pygame.locals import *                                                     # Constantes pygame (K_SPACE, QUIT, etc.)

IMAGES = {}
def charger_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        chemin = "images/" + piece + ".png"
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(chemin), (90, 90))


#Initialisation de pygame 

pygame.init()                                                                   # demarre tous les modules pygame
pygame.font.init()
LARGEUR = 800
HAUTEUR = 830
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Jeu d'échecs")                                      #Titre du jeu, titre de la fenetre

ej = EtatDeJeu()
selection = ()                                                                   #pour stocker la case sélectionnée
clics_joueur = []                                                                #pour stocker les clics du joueur
message_erreur = ""
debut_message_erreur = 0
encours = True                                                                  #controle de la boucle principal du jeu                                               
etat = "MENU"
etat_jeu = None
gagnant = ""
historique_positions = []
debut_clignotement = 0
case_roi_en_echec = None
debut_partie = True

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
                if ligne < 8 and colonne < 8 :
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

                    if piece_depart != "":
                        tour_correct = (ej.trait_aux_blancs and piece_depart[0] == 'w') or (not ej.trait_aux_blancs and piece_depart[0] == 'b')
                        if tour_correct:
                            # On récupère tous les mouvements valides pour cette pièce
                            # Ils sont sous la forme (ligne, col, est_capture)
                            mouvements_possibles = ej.mouvements_valide(dep_ligne, dep_colonne)
                            
                            # On cherche si le clic d'arrivée correspond à un mouvement autorisé
                            mouvement_choisi = None
                            for m in mouvements_possibles:
                                if m[0] == arr_ligne and m[1] == arr_colonne:
                                    mouvement_choisi = m
                                    break
                            
                            if mouvement_choisi:
                                # --- 1. GESTION DU ROQUE ---
                                if piece_depart[1] == 'K' and abs(arr_colonne - dep_colonne) == 2:
                                    tour_ligne = arr_ligne
                                    if arr_colonne == 6: # Petit roque
                                        ej.plateau[tour_ligne][5] = ej.plateau[tour_ligne][7]
                                        ej.plateau[tour_ligne][7] = ""
                                    elif arr_colonne == 2: # Grand roque
                                        ej.plateau[tour_ligne][3] = ej.plateau[tour_ligne][0]
                                        ej.plateau[tour_ligne][0] = ""

                                # --- 2. MISE À JOUR DES DRAPEAUX ---
                                if piece_depart == "wK": ej.deplacement_roi_blanc = True
                                elif piece_depart == "bK": ej.deplacement_roi_noir = True
                                elif piece_depart == "wR":
                                    if dep_colonne == 0: ej.deplacement_tour_blanche_gauche = True
                                    elif dep_colonne == 7: ej.deplacement_tour_blanche_droite = True
                                elif piece_depart == "bR":
                                    if dep_colonne == 0: ej.deplacement_tour_noire_gauche = True
                                    elif dep_colonne == 7: ej.deplacement_tour_noire_droite = True

                                # --- 3. EXÉCUTION DU MOUVEMENT ---
                                if piece_arrivee != "":
                                    soundeffect()
                                    # Désactiver le roque si une tour est capturée
                                    if arr_ligne == 7 and arr_colonne == 0: ej.deplacement_tour_blanche_gauche = True
                                    if arr_ligne == 7 and arr_colonne == 7: ej.deplacement_tour_blanche_droite = True
                                    if arr_ligne == 0 and arr_colonne == 0: ej.deplacement_tour_noire_gauche = True
                                    if arr_ligne == 0 and arr_colonne == 7: ej.deplacement_tour_noire_droite = True

                                ej.plateau[arr_ligne][arr_colonne] = piece_depart
                                ej.plateau[dep_ligne][dep_colonne] = ""

                                # --- 4. GESTION DU PION (Promotion & En Passant) ---
                                if piece_depart[1] == 'p':
                                    # En passant (prise physique)
                                    if (arr_ligne, arr_colonne) == ej.case_en_passant:
                                        ej.plateau[dep_ligne][arr_colonne] = ""
                                    
                                    # Double pas (mise à jour de la cible en passant)
                                    if abs(arr_ligne - dep_ligne) == 2:
                                        ej.case_en_passant = ((dep_ligne + arr_ligne) // 2, dep_colonne)
                                    else:
                                        ej.case_en_passant = None
                                    
                                    # Promotion
                                    if arr_ligne == 0 or arr_ligne == 7:
                                        etat_jeu = "PROMOTION"
                                        possibilites_promotion = (arr_ligne, arr_colonne)
                                        couleur_promue = piece_depart[0]
                                else:
                                    ej.case_en_passant = None

                                # --- 5. FIN DU TOUR ---
                                debut_partie = False
                                ej.enregistrer_position()
                                ej.trait_aux_blancs = not ej.trait_aux_blancs
                                ej.compteur_50_coups = 0 if (piece_depart[1] == 'p' or piece_arrivee != "") else ej.compteur_50_coups + 1

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
            # --- 1. PRIORITÉ ABSOLUE : LES MENUS DE CONFIRMATION ---
            # Si on attend une réponse O/N, on ne regarde RIEN d'autre
            if etat_jeu == "CONFIRMATION_ABANDON":
                if event.key == pygame.K_o:
                    gagnant = f"Abandon des {'Blancs' if ej.trait_aux_blancs else 'Noirs'}"
                    etat = "FIN"
                    etat_jeu = None  # On ferme le menu
                elif event.key == pygame.K_n:
                    etat_jeu = None  # On annule et on revient au jeu
                continue # On passe directement à l'évenement suivant

            elif etat_jeu == "PROPOSITION_NULLE":
                if event.key == pygame.K_o:
                    gagnant = "Accord mutuel"
                    etat = "FIN"
                    etat_jeu = None
                elif event.key == pygame.K_n:
                    etat_jeu = None
                continue

            # --- 2. GESTION DES AUTRES ÉTATS ---
            if etat == "MENU":
                if event.key == pygame.K_SPACE:
                    etat = "JEU"
                    soundbackground_tod()

            elif etat == "JEU":
                # On ne vérifie A et P que si aucun menu n'est ouvert
                if etat_jeu is None:
                    nb_coups = len(ej.historique_position)
                    if event.key == pygame.K_a:
                        if nb_coups >= 20: 
                            etat_jeu = "CONFIRMATION_ABANDON"
                    elif event.key == pygame.K_p:
                        if nb_coups >= 20: 
                            etat_jeu = "PROPOSITION_NULLE"
                
                # Touches de navigation toujours actives en jeu
                if event.key == pygame.K_RETURN:
                    etat = "MENU"
                    pygame.mixer.stop()
                elif event.key == pygame.K_ESCAPE:
                    etat = "FIN"

            elif etat == "FIN":
                if event.key == pygame.K_r:
                    ej = EtatDeJeu()
                    etat = "MENU"
                    debut_partie = True
                elif event.key == pygame.K_q:
                    encours = False
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

        if debut_partie:
            texte_debut = police_titre.render("AUX BLANCS DE JOUER", True, (255, 255, 255))
            rect_debut = texte_debut.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            pygame.draw.rect(fenetre, (0, 0, 0), rect_debut.inflate(20, 20))
            fenetre.blit(texte_debut, rect_debut)

        if selection != ():
            ligne, colonne = selection
            piece_cliquee = ej.plateau[ligne][colonne]
            tour_joueur = 'w' if ej.trait_aux_blancs else 'b'
            
            if piece_cliquee != "" and piece_cliquee[0] == tour_joueur:
                possibles = ej.mouvements_valide(ligne, colonne)
                for m in possibles:
                    m_ligne, m_colonne, type_mouv = m
                    if type_mouv == "roque":
                        couleur_point = (148, 0, 211)
                    elif type_mouv is True:
                        couleur_point = (250, 50, 50)
                    else:
                        couleur_point = (100, 100, 100)
                    centre_x = m_colonne * 100 + 50
                    centre_y = m_ligne * 100 + 50
                    pygame.draw.circle(fenetre, couleur_point, (centre_x, centre_y), 15)
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
            texte_echec = police_titre.render("Échec au roi " + ("Blanc" if couleur_actuelle == 'w' else "Noir"), True, (255, 50, 50))
            rect_echec = texte_echec.get_rect(center=(LARGEUR//2, HAUTEUR//2))
            pygame.draw.rect(fenetre, (0, 0, 0), rect_echec.inflate(20, 20))
            fenetre.blit(texte_echec, rect_echec)
        elif ej.est_manque_de_materiel():
            etat = "FIN"
            gagnant = "Manque de matériel"
        nb_total = len(ej.historique_position)
        if nb_total < 20:
            manquant = 20 - nb_total
            message = f"ESC pour quitter | Options A/P bloquées - Encore {manquant} demi-coups"
            couleur_barre = (200, 100, 100)
        else:
            message = "ESC pour quitter | A : Abandonner | P : Proposer Nulle"
            couleur_barre = (100, 200, 100)
        pygame.draw.rect(fenetre, couleur_barre, (0, HAUTEUR - 30, LARGEUR, 30))
        texte_msg = police_petite.render(message, True, (0, 0, 0))
        fenetre.blit(texte_msg, texte_msg.get_rect(center=(LARGEUR//2, HAUTEUR - 15)))
        couleur_tour = "Blancs" if ej.trait_aux_blancs else "Noirs"
        texte_tour = police_petite.render(f"Tour des {couleur_tour}", True, (255, 255, 255))
        pygame.draw.rect(fenetre, (50, 50, 50), (5, 5, 150, 25))
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

    elif etat_jeu == "PROMOTION":
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
    
    elif etat_jeu == "CONFIRMATION_ABANDON":
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(160)
        voile.fill((0, 0, 0))
        fenetre.blit(voile, (0, 0))
        texte = police_titre.render("Abandonner la partie ?", True, (255, 255, 255))
        sous_texte = police_instruction.render("Appuyez sur O (Oui) ou N (Non)", True, (200, 200, 200))
        fenetre.blit(texte, texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50)))
        fenetre.blit(sous_texte, sous_texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 20)))
    elif etat_jeu == "PROPOSITION_NULLE":
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(160)
        voile.fill((0, 0, 0))
        fenetre.blit(voile, (0, 0))
        texte = police_titre.render("Accepter la nulle ?", True, (255, 255, 255))
        sous_texte = police_instruction.render("Appuyez sur O (Oui) ou N (Non)", True, (200, 200, 200))
        fenetre.blit(texte, texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50)))
        fenetre.blit(sous_texte, sous_texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 20)))
    elif etat == "FIN":
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(180)
        voile.fill((0,0,0))
        fenetre.blit(voile, (0, 0))
        
        couleur_titre = (200, 200, 200)

        if "Abandon" in gagnant:
            titre = "PARTIE ABANDONNÉE"
            couleur_titre = (255, 100, 100) # Rouge un peu plus doux
            # On extrait le vainqueur pour le sous-titre
            vainqueur = "Blancs" if "Noirs" in gagnant else "Noirs"
            sous_titre = f"Victoire des {vainqueur} par abandon"
            
        elif "Accord mutuel" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Nulle par accord mutuel"

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
