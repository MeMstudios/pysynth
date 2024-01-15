from synth import MonoSynth
import pygame
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE, K_RIGHT, K_UP, K_DOWN, K_LEFT

synth = MonoSynth(sample_rate=44100)
synth.shape = "square"

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True
print("Welcome to PySynth!")

while running:
    event = pygame.event.wait()
    if event.type == KEYDOWN or event.type == pygame.QUIT:
        if event.key == K_ESCAPE:
            break
        elif event.key == K_RIGHT:
            print("Transposing up!")
            synth.transpose_up()
        elif event.key == K_UP:
            print("Octave up!")
            synth.octave_up()
        elif event.key == K_DOWN:
            print("Octave down!")
            synth.octave_down()
        else:
            synth.handle_music_key_press(event.key)
    elif event.type == KEYUP:
        synth.handle_music_key_release(event.key)
