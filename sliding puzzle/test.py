
import pygame
from pygame import mixer
mixer.init()

start_sound = mixer.Sound('game-start.wav')

x =  input("Please choose the mode to start playing (1-3):\n 1 - Easy\n 2 - Medium\n 3 - Hard\n")
if int(x) == 1:
    print("ha")
    start_sound.play()
elif int(x) == 2:
    print("hi")
elif int(x) == 3:
    print("ho")

 