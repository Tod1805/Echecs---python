import sys # Permet de quitter proprement le programme
import pygame # Librairie principale pour le jeu
from sound import vibration, soundeffect, soundbackground # Importe les fonctions de son définies dans sound.py
from classes import EtatDeJeu # Importe la classe EtatDeJeu définie dans classes.py pour gérer l'état de la partie, les règles du jeu, les mouvements possibles, etc.
from pygame.locals import * # Constantes pygame (K_SPACE, QUIT, etc.)
from constantes import * # Importe les constantes définies dans constantes.py pour les dimensions de la fenêtre, les couleurs, les polices, les images, et les variables globales de contrôle du jeu

#Initialisation de pygame et de la fenêtre de jeu
pygame.init() # Initialise tous les modules de Pygame
pygame.font.init() # Initialise le module de police de caractères de Pygame
pygame.display.set_caption("Jeu d'échecs") # Définit le titre de la fenêtre du jeu d'échecs, qui s'affiche généralement dans la barre de titre de la fenêtre, pour identifier le jeu et lui donner une identité visuelle.

charger_images() 

while encours :                                                                  
    for event in pygame.event.get(): # Récupère tous les événements qui se sont produits depuis la dernière itération de la boucle, tels que les clics de souris, les pressions de touches, les mouvements de la souris, etc., et les traite un par un pour mettre à jour l'état du jeu en fonction des actions du joueur.
        if event.type == pygame.QUIT: # si l'evenement est de type QUIT (fermeture de la fenêtre), alors on quitte le programme proprement en appelant pygame.quit() pour fermer la fenêtre et sys.exit() pour terminer le processus Python.
            encours = False
        if event.type == pygame.MOUSEBUTTONDOWN and etat == "JEU" and etat_jeu is None: # Si le joueur clique avec la souris pendant que le jeu est en cours et qu'aucun menu n'est ouvert, on traite le clic pour sélectionner une pièce ou faire un mouvement
            pos = pygame.mouse.get_pos()
            colonne = pos[0] // 100
            ligne = pos[1] // 100
            if ligne < 8 and colonne < 8: # Vérifie que le clic est bien dans les limites du plateau de jeu (8x8 cases), pour éviter les erreurs d'indexation et garantir que les interactions du joueur sont correctement traitées uniquement lorsqu'elles se produisent sur le plateau de jeu
                if selection == (ligne, colonne):
                    selection = ()
                    clics_joueur = []
                elif len(clics_joueur) == 0:  # PREMIER CLIC
                    piece_cliquee = ej.plateau[ligne][colonne]
                    tour_joueur = 'w' if ej.trait_aux_blancs else 'b'
                    
                    if piece_cliquee != "" and piece_cliquee[0] == tour_joueur:
                        # On vérifie si la pièce peut bouger
                        possibles = ej.mouvements_valide(ligne, colonne)
                        if len(possibles) == 0:
                            # La pièce est bloquée, on affiche un message pendant 1 seconde et on réinitialise la sélection
                            message_bloque = "PIÈCE BLOQUÉE !"
                            debut_timer_bloque = pygame.time.get_ticks()
                            vibration() # Effet sonore
                            selection = ()
                            clics_joueur = []
                        else:
                            selection = (ligne, colonne)
                            clics_joueur.append(selection)
                else: # Deuxième clic
                    selection = (ligne, colonne)
                    clics_joueur.append(selection)
                if len(clics_joueur) == 2: # Si le joueur a cliqué deux fois, on essaie de faire le mouvement
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
                                    break # Si le mouvement choisi n'est pas dans les mouvements possibles, on ne fait rien (le clic est ignoré)
                            if mouvement_choisi:
                                # Le Roque est traité comme un mouvement spécial : on déplace le roi, puis la tour
                                if piece_depart[1] == 'K' and abs(arr_colonne - dep_colonne) == 2:
                                    tour_ligne = arr_ligne
                                    if arr_colonne == 6: # Petit roque
                                        ej.plateau[tour_ligne][5] = ej.plateau[tour_ligne][7]
                                        ej.plateau[tour_ligne][7] = ""
                                    elif arr_colonne == 2: # Grand roque
                                        ej.plateau[tour_ligne][3] = ej.plateau[tour_ligne][0]
                                        ej.plateau[tour_ligne][0] = ""

                                # Le déplacement du roi ou de la tour empêche le roque, on met à jour les variables correspondantes pour désactiver le roque si nécessaire
                                if piece_depart == "wK": ej.deplacement_roi_blanc = True
                                elif piece_depart == "bK": ej.deplacement_roi_noir = True
                                elif piece_depart == "wR":
                                    if dep_colonne == 0: ej.deplacement_tour_blanche_gauche = True
                                    elif dep_colonne == 7: ej.deplacement_tour_blanche_droite = True
                                elif piece_depart == "bR":
                                    if dep_colonne == 0: ej.deplacement_tour_noire_gauche = True
                                    elif dep_colonne == 7: ej.deplacement_tour_noire_droite = True

                                # Le déplacement capture une pièce adverse, on joue un son de capture et on désactive le roque si une tour est capturée
                                if piece_arrivee != "":
                                    soundeffect()
                                    # Désactiver le roque si une tour est capturée
                                    if arr_ligne == 7 and arr_colonne == 0: ej.deplacement_tour_blanche_gauche = True
                                    if arr_ligne == 7 and arr_colonne == 7: ej.deplacement_tour_blanche_droite = True
                                    if arr_ligne == 0 and arr_colonne == 0: ej.deplacement_tour_noire_gauche = True
                                    if arr_ligne == 0 and arr_colonne == 7: ej.deplacement_tour_noire_droite = True

                                ej.plateau[arr_ligne][arr_colonne] = piece_depart
                                ej.plateau[dep_ligne][dep_colonne] = ""

                                # La prise en passant est traitée comme un mouvement spécial : si un pion fait un double pas, on active la cible en passant, et si un pion adverse capture en passant, on enlève la pièce capturée du plateau
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

                                # Fin du tour : on enregistre la position, on change de joueur, on réinitialise la sélection et les clics, et on vérifie si le roi adverse est en échec pour déclencher le clignotement et le son de vibration
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
            # Menu de confirmation pour l'abandon et la proposition de nulle, et menu de promotion du pion
            # Si on attend une réponse O/N, on ne regarde RIEN d'autre
            if etat_jeu == "CONFIRMATION_ABANDON": # On vérifie si le joueur confirme son abandon ou sa proposition de nulle
                if event.key == pygame.K_o:
                    gagnant = f"Abandon des {'Blancs' if ej.trait_aux_blancs else 'Noirs'}"
                    etat = "FIN"
                    etat_jeu = None  # On ferme le menu
                elif event.key == pygame.K_n:
                    etat_jeu = None  # On annule et on revient au jeu
                continue # On passe directement à l'évenement suivant

            elif etat_jeu == "PROPOSITION_NULLE": # On vérifie si le joueur accepte la proposition de nulle
                if event.key == pygame.K_o:
                    gagnant = "Accord mutuel"
                    etat = "FIN"
                    etat_jeu = None
                elif event.key == pygame.K_n:
                    etat_jeu = None
                continue
                
            elif etat_jeu == "PROMOTION": # On vérifie quelle pièce le joueur choisit pour la promotion du pion
                r, c = possibilites_promotion
                touche_valide = True
                if event.key == pygame.K_q:    # Dame (Queen)
                    ej.plateau[r][c] = couleur_promue + "Q" # On place la pièce promue sur le plateau en fonction de la couleur du pion qui a atteint la dernière rangée (wQ pour une promotion d'un pion blanc, bQ pour une promotion d'un pion noir)
                elif event.key == pygame.K_r:  # Tour (Rook)
                    ej.plateau[r][c] = couleur_promue + "R"
                elif event.key == pygame.K_b:  # Fou (Bishop)
                    ej.plateau[r][c] = couleur_promue + "B"
                elif event.key == pygame.K_n:  # Cavalier (Knight)
                    ej.plateau[r][c] = couleur_promue + "N"
                else:
                    touche_valide = False
                if touche_valide:
                    etat_jeu = None # On ferme le menu de promotion et on reprend le jeu
                continue # On ne traite pas les autres touches (A, P, ESC) pendant la promotion

            # Espace pour démarrer la partie depuis le menu
            if etat == "MENU":
                if event.key == pygame.K_SPACE:
                    etat = "JEU"
                    soundbackground() # Lancer la musique de fond dès le début de la partie

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

    if etat == "MENU": # Affichage du menu principal avec le titre, les instructions et une image d'accueil
        fenetre.fill(NOIR)
        fenetre.blit(image_menu, rect_image)
        fenetre.blit(texte_bienvenue, rect_bienvenue)
        fenetre.blit(texte_instruction, rect_instruction)
    elif etat == "JEU": # Affichage du plateau de jeu, des pièces, des messages d'état (échec, échec et mat, tour actuel, etc.) et des indications de mouvements possibles
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

        if debut_partie: # Affiche un message de début de partie au centre de l'écran avant le premier coup
            pygame.draw.rect(fenetre, NOIR, rect_debut.inflate(20, 20))
            fenetre.blit(texte_debut, rect_debut)

        if selection != ():
            ligne, colonne = selection
            piece_cliquee = ej.plateau[ligne][colonne]
            tour_joueur = 'w' if ej.trait_aux_blancs else 'b'
            
            if piece_cliquee != "" and piece_cliquee[0] == tour_joueur: # Si la pièce cliquée appartient au joueur dont c'est le tour, on affiche les mouvements possibles pour cette pièce
                possibles = ej.mouvements_valide(ligne, colonne)
                for m in possibles:
                    m_ligne, m_colonne, type_mouv = m
                    if type_mouv == "roque":
                        couleur_point = (VOILET)
                    elif type_mouv is True:
                        couleur_point = (ROUGE_VIF) 
                    else:
                        couleur_point = (GRIS_CLAIR)
                    centre_x = m_colonne * 100 + 50
                    centre_y = m_ligne * 100 + 50
                    pygame.draw.circle(fenetre, couleur_point, (centre_x, centre_y), 15)
        couleur_actuelle = "w" if ej.trait_aux_blancs else "b"
        if ej.est_echec_et_mat(couleur_actuelle): # Affiche un message d'échec et mat au centre de l'écran avec le nom du gagnant
            etat = "FIN"
            gagnant = 'Blancs' if not ej.trait_aux_blancs else 'Noirs'
            texte_echec_mat = police_titre.render("Échec et mat ! Gagnant : " + gagnant, True, ROUGE_VIF)
            rect_echec_mat = texte_echec_mat.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
            pygame.draw.rect(fenetre, NOIR, rect_echec_mat.inflate(20, 20))
            fenetre.blit(texte_echec_mat, rect_echec_mat)
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif ej.est_en_echec(couleur_actuelle): # Affiche un message d'échec au roi du joueur actuel
            texte_echec = police_titre.render("Échec au roi " + ("Blanc" if couleur_actuelle == 'w' else "Noir"), True, (255, 50, 50))
            rect_echec = texte_echec.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 15))
            pygame.draw.rect(fenetre, NOIR, rect_echec.inflate(20, 20))
            fenetre.blit(texte_echec, rect_echec)
        elif ej.est_manque_de_materiel(): # Affiche un message de fin de partie pour manque de matériel
            etat = "FIN"
            gagnant = "Manque de matériel"
        nb_total = len(ej.historique_position)
        if nb_total < 20:
            manquant = 20 - nb_total
            message = f"ESC pour quitter | Options A/P bloquées - Encore {manquant} demi-coups"
            couleur_barre = (ROUGE_CLAIR)
        else:
            message = "ESC pour quitter | A : Abandonner | P : Proposer Nulle" # Affiche les options disponibles pour le joueur (abandonner, proposer nulle) et les conditions pour les débloquer (20 demi-coups)
            couleur_barre = (VERT_CLAIR)
        pygame.draw.rect(fenetre, couleur_barre, (0, HAUTEUR - 30, LARGEUR, 30))
        texte_msg = police_petite.render(message, True, NOIR)
        fenetre.blit(texte_msg, texte_msg.get_rect(center=(LARGEUR//2, HAUTEUR - 15)))
        couleur_tour = "Blancs" if ej.trait_aux_blancs else "Noirs"
        texte_tour = police_petite.render(f"Tour des {couleur_tour}", True, BLANC)
        pygame.draw.rect(fenetre, GRIS_FONCE, (5, 5, 150, 25)) #
        fenetre.blit(texte_tour, (10, 8))
    if case_roi_en_echec:
        temps_ecoule = pygame.time.get_ticks() - debut_clignotement
        if temps_ecoule < 2000: # Clignote pendant 2 secondes
            if (temps_ecoule // 250) % 2 == 0: # Alterne entre visible et invisible toutes les 250 ms
                r, c = case_roi_en_echec # Affiche un clignotement rouge sur la case du roi en échec
                voile = pygame.Surface((100, 100)) # Crée une surface pour le clignotement
                voile.set_alpha(128) # Transparence
                voile.fill(ROUGE) # Couleur du clignotement (rouge)
                fenetre.blit(voile, (c * 100, r * 100)) # Affiche le clignotement sur la case du roi en échec
                vibration() # Déclenche un son de vibration pour renforcer l'effet d'échec
        else: 
            case_roi_en_echec = None # Arrête le clignotement après 2 secondes
    elif etat_jeu == "PROMOTION": # Affiche un menu de promotion du pion, avec un voile sombre en arrière-plan et des options de promotion pour la pièce promue, afin d'informer le joueur de la promotion de son pion et de lui permettre de choisir la pièce qu'il souhaite obtenir en échange du pion
        voile = pygame.Surface((400, 200)) # Crée une surface pour le voile de promotion
        voile.set_alpha(220)
        voile.fill(GRIS_FONCE)
        fenetre.blit(voile, (200, 300))
    
        options = ["Dame Q", "Tour R", "Fou B", "Cavalier N"] # Options de promotion pour la pièce promue
        for i, option in enumerate(options): # Affiche les options de promotion pour la pièce promue
            texte_option = police_petite.render(option, True, BLANC) # Affiche les options de promotion en blanc
            fenetre.blit(texte_option, (250, 320 + i * 40)) # Affiche les options de promotion dans la fenêtre
    elif etat_jeu == "CONFIRMATION_ABANDON": # Affiche un menu de confirmation pour l'abandon de la partie, avec un voile sombre en arrière-plan et des instructions pour le joueur, afin d'éviter les abandons accidentels et de s'assurer que le joueur est conscient de sa décision avant de quitter la partie.
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(160)
        voile.fill(NOIR)
        fenetre.blit(voile, (0, 0))
        texte = police_titre.render("Abandonner la partie ?", True, BLANC)
        sous_texte = police_instruction.render("Appuyez sur O (Oui) ou N (Non)", True, GRIS_CLAIR)
        fenetre.blit(texte, texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50)))
        fenetre.blit(sous_texte, sous_texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 20)))
    elif etat_jeu == "PROPOSITION_NULLE": # Affiche un menu de proposition de nulle, avec un voile sombre en arrière-plan et des instructions pour le joueur, afin de permettre au joueur de proposer une nulle à son adversaire et d'attendre sa réponse avant de continuer la partie.
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(160)
        voile.fill(NOIR)
        fenetre.blit(voile, (0, 0))
        texte = police_titre.render("Accepter la nulle ?", True, BLANC)
        sous_texte = police_instruction.render("Appuyez sur O (Oui) ou N (Non)", True, GRIS_CLAIR)
        fenetre.blit(texte, texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50)))
        fenetre.blit(sous_texte, sous_texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 20)))
    elif etat == "FIN":
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
        voile = pygame.Surface((LARGEUR, HAUTEUR))
        voile.set_alpha(160)
        voile.fill(NOIR)
        fenetre.blit(voile, (0, 0))
        fenetre.blit(texte_fin, rect_fin) # Affiche le message de fin

        if "Abandon" in gagnant: # Si la partie s'est terminée par un abandon, on affiche un message spécifique avec le vainqueur
            titre = "PARTIE ABANDONNÉE"
            couleur_titre = ROUGE
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
            couleur_titre = (OR)
            sous_titre = f"Victoire des {gagnant} !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        elif "Manque de matériel" in gagnant:
            titre = "MATCH NUL !"
            sous_titre = "Match nul par manque de matériel !"
            pygame.mixer.fadeout(10000) # Fondu de 10 secondes pour la musique de fond
        #print("Debug : sous_titre =", sous_titre)  # Debug pour vérifier le contenu de sous_titre
        texte_vainqueur = police_instruction.render(sous_titre, True, BLANC)
        rect_vainqueur = texte_vainqueur.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 40))
        texte_titre = police_titre.render(titre, True, couleur_titre)
        rect_titre = texte_titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 90))
        fenetre.blit(texte_titre, rect_titre)
        fenetre.blit(texte_vainqueur, rect_vainqueur)
        fenetre.blit(texte_rejouer, rect_rejouer) # Affiche les instructions pour rejouer ou quitter
    couleur_actuelle = "white" if ej.trait_aux_blancs else "black" # Détermine la couleur du joueur actuel
    if ej.est_en_echec(couleur_actuelle): # Affiche un message d'échec au roi du joueur actuel
        texte_echec = police_titre.render("Échec au roi " + couleur_actuelle, True, (255, 50, 50)) # Affiche le message d'échec en rouge vif
        rect_echec = texte_echec.get_rect(center=(LARGEUR//2, HAUTEUR//2)) # Affiche le rectangle du message d'échec
        pygame.draw.rect(fenetre, NOIR, (rect_echec.x - 10, rect_echec.y - 10, rect_echec.width + 20, rect_echec.height + 20)) # Dessine un rectangle noir derrière le message d'échec pour le faire ressortir
        fenetre.blit(texte_echec, rect_echec) # Affiche le message d'échec au roi du joueur actuel
    
    if message_bloque != "":
            temps_actuel = pygame.time.get_ticks()
            # On vérifie si les 1000 ms (1 secondes) sont écoulées
            if temps_actuel - debut_timer_bloque < 1000:
                surface_texte = police_titre.render(message_bloque, True, BLANC)
                rect_texte = surface_texte.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 15))
                
                # On dessine un fond pour le texte (optionnel mais plus lisible)
                pygame.draw.rect(fenetre, (200, 0, 0), rect_texte.inflate(30, 30)) # Cadre rouge
                pygame.draw.rect(fenetre, NOIR, rect_texte.inflate(20, 20))  # Fond noir
                fenetre.blit(surface_texte, rect_texte)
            else:
                # Le temps est écoulé, on réinitialise le message
                message_bloque = ""

    pygame.display.flip() # Met à jour l'affichage de la fenêtre
pygame.quit() # Quitte pygame proprement
sys.exit() # Quitte le programme proprement
