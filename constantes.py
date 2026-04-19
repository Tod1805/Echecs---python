import sys # permet de quitter proprement le programme
import pygame # librairie principale pour le jeu
from sound import vibration, soundeffect, soundbackground  # importe les fonctions de son définies dans sound.py
from classes import EtatDeJeu
from pygame.locals import * # Constantes pygame (K_SPACE, QUIT, etc.)
pygame.font.init()

# Initialisation de l'état de jeu et des variables de contrôle
ej = EtatDeJeu() # Créer une instance de la classe EtatDeJeu pour gérer l'état de la partie, les règles du jeu, les mouvements possibles, etc., ce qui permet d'organiser le code de manière modulaire et de faciliter la gestion de la logique du jeu.
selection = () # Stocker la case sélectionnée par le joueur
clics_joueur = [] # Stocker les clics du joueur
message_erreur = "" # Stocker le message d'erreur à afficher au joueur en cas de coup invalide ou de situation de jeu particulière, pour fournir des retours clairs et informatifs sur les actions du joueur et les règles du jeu.
debut_message_erreur = 0 # Stocker le moment où le message d'erreur a été déclenché, pour permettre de contrôler la durée d'affichage du message à l'écran et de le faire disparaître après un certain temps, afin d'éviter que le message ne reste affiché indéfiniment et n'encombre l'interface du jeu.
encours = True # Contrôler la boucle principale du jeu                                              
etat = "MENU" # Stocker l'état actuel du jeu (MENU, JEU, FIN, etc.) pour gérer les différentes phases du jeu et afficher les éléments appropriés à chaque étape.         
etat_jeu = None # Stocker l'état de la partie en cours (en échec, en échec et mat, en pat, etc.) pour déterminer les conditions de fin de partie et afficher les messages correspondants au joueur.
gagnant = "" # Stocker le gagnant de la partie (blanc, noir, nul) pour afficher le résultat de la partie à la fin du jeu et fournir une conclusion satisfaisante au joueur.
historique_positions = [] # Stocker l'historique des positions du plateau pour permettre de vérifier les conditions de nulle par répétition et d'afficher l'historique des coups joués, ce qui enrichit l'expérience de jeu et permet au joueur de suivre l'évolution de la partie.
debut_clignotement = 0 # Stocker le moment où le clignotement du roi en échec a commencé, pour permettre de contrôler la durée du clignotement et de le faire arrêter après un certain temps, afin d'attirer l'attention du joueur sur la situation d'échec sans que cela devienne trop distrayant ou gênant.    
case_roi_en_echec = None # Stocker la position du roi en échec pour permettre de faire clignoter le roi en échec et d'attirer l'attention du joueur sur la situation d'échec, ce qui améliore la lisibilité du jeu et aide le joueur à comprendre les conséquences de ses actions et les menaces sur son roi.
debut_partie = True # Contrôler le début de la partie pour afficher les éléments du menu et les instructions au joueur avant de commencer la partie, ce qui permet de créer une introduction immersive et de préparer le joueur à l'expérience de jeu.
message_bloque = "" # Stocker le message à afficher lorsque le joueur est bloqué pour fournir des retours clairs et informatifs sur la situation de blocage du joueur et les raisons pour lesquelles il ne peut pas jouer, ce qui enrichit l'expérience de jeu et aide le joueur à comprendre les conséquences de ses actions.
debut_timer_bloque = 0 # Stocker le moment où le timer de blocage a commencé pour permettre de contrôler la durée du message de blocage affiché à l'écran et de le faire disparaître après un certain temps, afin d'éviter que le message ne reste affiché indéfiniment et n'encombre l'interface du jeu.    
titre = "" # Stocker le titre à afficher dans les différentes phases du jeu pour fournir des informations claires sur l'état actuel du jeu et les événements importants qui se produisent, ce qui améliore la lisibilité du jeu et aide le joueur à comprendre les conséquences de ses actions et les résultats de la partie.    
sous_titre = "" # Stocker le sous-titre à afficher dans les différentes phases du jeu pour fournir des informations supplémentaires sur l'état actuel du jeu et les événements importants qui se produisent, ce qui enrichit l'expérience de jeu et aide le joueur à comprendre les conséquences de ses actions et les résultats de la partie. 
texte_debut = "" # Stocker le texte de début de partie pour l'afficher au centre de l'écran avant le premier coup, afin d'informer les joueurs que la partie va commencer et leur indiquer qui joue en premier, ce qui crée une introduction immersive et prépare les joueurs à l'expérience de jeu.
pos = (0, 0) # Stocker la position du clic de souris pour déterminer la case sélectionnée par le joueur et les mouvements possibles, ce qui permet d'interagir avec le plateau de jeu de manière intuitive et de fournir une interface utilisateur fluide.

# Constantes pour les dimensions de la fenêtre et du plateau
LARGEUR = 800
HAUTEUR = 830
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))
taille_case = LARGEUR  // 8

# Couleurs utilisées dans le jeu
BLANC = (255, 255, 255)
GRIS_CLAIR = (200, 200, 200)
GRIS_FONCE = (50, 50, 50)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
ROUGE_VIF = (255, 50, 50) # Rouge vif pour les captures
ROUGE_CLAIR = (200, 100, 100)
VERT_CLAIR = (100, 200, 100)
VOILET = (148, 0, 211) # Violet pour les pointes pour les coups spéciaux
OR = (255, 215, 0) # Or pour les titres de victoire
couleur_titre = GRIS_CLAIR # Couleur par défaut pour le titre, peut être modifiée selon le type de fin
couleur_titre = ROUGE

# Variables globales pour les polices, les images et les éléments d'interface du menu et de la fin de partie
police_titre = pygame.font.SysFont("Verdana", 35, bold=True)
police_instruction = pygame.font.SysFont("Verdana", 25)
police_petite = pygame.font.SysFont("Arial", 18, bold=True)
image_menu = pygame.image.load("images/wp.png")
image_menu = pygame.transform.scale(image_menu, (400, 400))
rect_image = image_menu.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))
texte_bienvenue = police_titre.render("Bienvenue dans notre jeu d'échecs", True, BLANC)
texte_instruction = police_instruction.render("Appuyez sur ESPACE pour jouer", True, GRIS_CLAIR)
rect_bienvenue = texte_bienvenue.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 250))
rect_instruction = texte_instruction.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 200))
texte_debut = police_titre.render("AUX BLANCS DE JOUER", True, BLANC)
rect_debut = texte_debut.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 15))
texte_fin = police_titre.render("Partie terminée", True, (255, 50, 50))
texte_rejouer = police_instruction.render("Appuyez sur R pour rejouer ou Q pour quitter", True, GRIS_CLAIR)
rect_fin = texte_fin.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 200))
rect_rejouer = texte_rejouer.get_rect(center=(LARGEUR//2, HAUTEUR//2 + 50))

IMAGES = {}
def charger_images():
    """Charge les images des pièces d'échecs à partir du dossier 'images' et les redimensionne à 90x90 pixels, en les stockant dans un dictionnaire global IMAGES avec les clés correspondant aux codes des pièces (par exemple, 'wK' pour le roi blanc, 'bQ' pour la dame noire, etc.), ce qui permet de les afficher facilement sur le plateau de jeu lors de la boucle principale."""
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        chemin = "images/" + piece + ".png"
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(chemin), (90, 90))

