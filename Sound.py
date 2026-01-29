import pygame
import time

def soundb():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("sounds\Title (Wii Play).mp3")
    sound.play(loops=-1)

start_time = None

def soundm():
    global start_time

    if start_time is None:
        pygame.mixer.music.load("sounds/Title (Wii Play).mp3")
        pygame.mixer.music.play()
        start_time = pygame.time.get_ticks()

    if pygame.time.get_ticks() - start_time >= 2000:
        pygame.mixer.music.stop()
        start_time = None