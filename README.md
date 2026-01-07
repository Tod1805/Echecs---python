# Echecs---python
Nous souhaitons créer un jeu d'échecs en 2D avec des animations dans le jeu d'échecs et dans la prise entre les pièces (par exemple lorsqu'une pièce mange une autre pièce il y aura une animation).

-Quel système de contrôl ?
le pointeur souris

- Ya-t-il une confirmation de déplacement?
Non il n'y aura pas de confirmation de déplacement pour faciliter le déroulement de la partie.

- Lorsqu'une pièce se fera manger y aura-t-il une animation?
Oui, il y aura une petite image de sang pendant 3 secondes après la prise de la pièce.

- Une partie aura-t-elle une durée limitée ?
Oui, il y aura des parties de 10 et de 15 min. Chacun aura un timer de 10 min. Lorsque le timer est fini la partie prend fin.

- Que se passe-t-il si on fait une mouvement illégal ?
Le joueur est averti par un petit message et la case apparait rouge momentanement.

- Lorsqu'une piece est menacee d'etre mangée, y aura-t-il des animations ?
Oui, la pièce suera et si c'est le Roi et qu'il n'y a pas de moyen d'echapper à l'échec et mat il deviendra un peu plus claire momentanement.

- Peut-on revenir en arrière et annulé un mouvement?
Non, il n'y aura pas de possibilité de rejouer.

- Est ce que le jeu autorise l'annulation d'un coup?
non, impossible de revenir en arriere pour ne pas compliquer la partie.

- En combien de dimensions sera le jeux ?
Le jeu sera en 2D.

- Comment la pièce se déplace-t-elle lors d'un changement de case ?
Elle glissera sur le plateau jusqu'a sa destination.

- Que se passe-t-il lors d'un match nul?
il n'y a ni perdant ni gagnant donc aucune animation de defaite ni de victoire et un message d'egalité apparaitra.

- Peux-t-on recommencer un partie en cours?
Oui, si a la demande du premier joueur le deuxieme confirme qu'il ne veux plus jouer, la partie peux s'arreter. Pour la recommencer, il suffit de relancer une nouvelle partie.

- Est ce que on doit se débrouiller tout seul ou est ce que on aura des messages d'aide ou de conseils?
Il est possible de recevoir de l'aide/conseils prealablements construits sur d'autres parties d'autres joueurs.

- Y aura-t-il du son lorsque le pion mangera un autre pion ou lorsqu'il se fera manger?
il y aura differents sons pour chaque actions, échec, échec et mat et prise de pièce.

- Est-ce que le déplacement des pions est visible?
Oui, il y aura meme differentes animations en fonctions des pions.

Planning :

Semaine 1 : 
	Création des groupes et choix du projet

Semaine 2 : 
	Création de notre cahier des charges

Semaine 3 : 
Création de notre calendrier

Semaine 4 :
Coder le plateau : Théodore et Diego
Dessiner les images de pièces dans sur pixel studio pour pouvoir les utiliser plus tard : Naomi et Oklenne

Semaine 5 :
	Coder les positions initiales des pièces. Si les pièces sont mal placées alors la partie ne peut pas commencer.
Blancs (en bas) : Théodore et Diego
Noirs (en haut) : Oklenne et Naomi

Semaine 6 :
	Codage des déplacements du pion, du roi et de la tour.
Pions : Diego et Théodore
Roi et Tour : Oklenne et Naomi

Semaine 7 :
	Codage des déplacements de la dame, du cavalier et du fou.
Cavalier : Théodore et Diego
Dame et Fou : Oklenne et Naomi

Semaine 8 :
	Coder le principe d’échec. Quand le roi est en échec il doit se déplacer ou manger la pièce qui le met en échec ou mettre une pièce entre la pièce qui met le roi en échec et le roi si possible.

Semaine 9 :
	Coder comment manger d’autres pièces. (Oklenne et Naomi) Coder les coups illégaux. Si quelqu’un fait un coup illégal, la case apparaît rouge et un il y a un son pour dire que ça ne marche pas. (Théodore et Diego)

Semaine 10 :
	Coder le principe de roque entre le roi et la tour.

Semaine 11 :
	Coder le principe de promotion. Lorsqu’un pion arrive sur la dernière ligne, le joueur doit choisir en quelle pièce il veut transformer son pion en :
Dame : Diego 
Tour : Thédore
Cavalier : Oklenne
Fou : Naomi

Semaine 12 :
	Coder le principe d’échec et mat. Si le roi est en échec et qu’il ne peut pas sortir de l’échec au prochain coup alors la partie s’arrête. Diego et Théodore

Semaine 13 :
	Coder le principe de la partie nulle. Si les deux joueurs se mettent d’accord, la partie est nulle. (Oklenne et Naomi) Si le matériel est insuffisant pour mater, la partie est nulle. (Diego et Théodore)

Semaine 14 :
	Si le joueur ne peut plus faire de mouvement et qu’il n’est pas en échec, la partie est nulle. (Oklenne et Naomi) Si 3 coups sont répétés de chaque côté, la partie est nulle. (Théodore et Diego)
	
Semaine 15 :
	 Création des différentes animations de déplacement et des sons des pièces lorsqu’il y a échec, échec et mat, lorsqu’une pièce se déplace ou qu’elle mange une autre pièce. Création d’une page d’accueil début où l’on choisit de jouer en 1 contre 1 et on met une musique de fond. Oklenne et Naomi
	
Semaine 16 :
Recherche de bug et de problèmes dans le programme.
	
Semaine 17 :
	Recherche de bug et de problèmes dans le programme.

pyxel studio project : www.pyxelstudio.net/nr8zdx92

