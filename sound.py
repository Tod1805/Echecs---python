import pygame

def soundbackground():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds\Title (Wii Play).mp3")
    sound.play(loops=-1)

def soundeffect():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds/chess hitting wood.mp3")
    sound.play()
