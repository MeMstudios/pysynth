from synth import MonoSynth
import pygame
from pygame.locals import KEYDOWN, KEYUP, K_ESCAPE, K_RIGHT, K_UP, K_DOWN, K_LEFT

if __name__ == "__main__":
    synth = MonoSynth(sample_rate=44100)
    synth.shape = "square"
    pygame.init()
    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
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
                synth.handle_key_press(event.key)
        elif event.type == KEYUP:
            synth.handle_key_release(event.key)
