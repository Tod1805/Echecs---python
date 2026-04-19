import pygame
def soundeffect():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds/chess hitting wood.mp3")
    sound.set_volume(0.1) # Réduire le volume de l'effet sonore       
    sound.play()

def soundbackground():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds/The_Winner_Is_Soundtrack.mp3")
    sound.play(loops=-1)

def vibration():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds/vibration.mp3")
    sound.play(maxtime=500) # Joue le son de vibration pendant 500 millisecondes pour simuler une vibration courte
