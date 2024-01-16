from synth import MonoSynth
import pygame
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE, K_RIGHT, K_UP, K_DOWN, K_LEFT
import math

hz, sample_rate = 440, 44100
synth = MonoSynth(hz, sample_rate)

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

x_offset = 0
running = True
freq = 0

print("Welcome to PySynth!")

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                print("Transposing up!")
                synth.transpose_up()
            elif event.key == K_UP:
                print("Octave up!")
                synth.octave_up()
            elif event.key == K_DOWN:
                print("Octave down!")
                synth.octave_down()
            else:
                freq = synth.handle_music_key_press(event.key)
        elif event.type == KEYUP:
            synth.handle_music_key_release(event.key)
            freq = 0
        elif event.type == pygame.QUIT:
            running = False

    if not freq:
        freq = 0

    screen.fill("purple")
    # Draw the wave
    points = []

    for x in range(0, width):
        y = int(100 * math.sin(freq * (x + x_offset)))
        points.append((x, height // 2 + y))

    pygame.draw.lines(screen, (0, 0, 0), False, points, 2)

    pygame.display.flip()

    clock.tick(60)

    x_offset += sample_rate