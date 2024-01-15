import numpy as np
import pygame
from pygame.locals import *

# Equal Temperament
RATIOS = [
    1.0,
    1.059463,
    1.122462,
    1.189207,
    1.259921,
    1.33484,
    1.414214,
    1.498307,
    1.587401,
    1.681793,
    1.781797,
    1.887749,
    2,
]


# Theoretical
# RATIOS = [
#     1.0,
#     1.06,
#     1.125,
#     1.2,
#     1.25,
#     1.3,
#     1.42,
#     1.5,
#     1.6,
#     1.666666,
#     1.777777,
#     1.875,
#     2
# ]


class BaseSynth:
    _base_hz = 440
    _scale: dict
    sample_rate: int  # Samples per second
    buffer_size: int  # Buffer size of the pygame mixer
    mixer_size: int  # Mixer size I believe 16 bits up and down
    peak: int  # Peak amplitude

    def __init__(self, sample_rate=44100, buffer_size=512, mixer_size=-16, peak=4096):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.mixer_size = mixer_size
        self.peak = peak
        self.scale = self._base_hz

    @property
    def scale(self) -> dict:
        """
        A dict with keys of the keyboard key constants laid out for a music keyboard
        with values being the hz of a 12-note scale
        :return: dict
        """
        return self._scale

    @scale.setter
    def scale(self, hz):
        """
        Set the scale based on the given hz using the ratios
        :param hz:
        :return:
        """
        self._scale = {
            K_a: hz * RATIOS[0],
            K_w: hz * RATIOS[1],
            K_s: hz * RATIOS[2],
            K_d: hz * RATIOS[3],
            K_r: hz * RATIOS[4],
            K_f: hz * RATIOS[5],
            K_t: hz * RATIOS[6],
            K_g: hz * RATIOS[7],
            K_h: hz * RATIOS[8],
            K_u: hz * RATIOS[9],
            K_j: hz * RATIOS[10],
            K_i: hz * RATIOS[11],
            K_k: hz * RATIOS[12],
        }

    @property
    def base_hz(self):
        return self._base_hz

    @base_hz.setter
    def base_hz(self, hz):
        self._base_hz = hz
        self.scale = hz

    def sine_wave(self, hz: float) -> np.ndarray:
        """Compute N samples of a sine wave with given frequency and peak amplitude.
        Defaults to one second.
        """
        # Adapted this beauty from https://stackoverflow.com/a/62250319
        return np.array(
            [
                self.peak * np.sin(2.0 * np.pi * round(hz) * x / self.sample_rate)
                for x in range(0, self.sample_rate)
            ]
        ).astype(np.int16)

    def square_wave(self, hz) -> np.ndarray:
        """Compute N samples of a sine wave with given frequency and peak amplitude.
        Defaults to one second.
        """
        t = np.linspace(0, 1, self.sample_rate, endpoint=False)
        wave = np.sign(np.sin(2 * np.pi * round(hz) * t))
        return (self.peak * wave).astype(np.int16)


class MonoSynth(BaseSynth):
    channels = 1
    _shape = "sine"
    _wave_fn = BaseSynth.sine_wave
    _sounds: dict

    def __init__(self, sample_rate=44100, buffer_size=512, mixer_size=-16, peak=4096):
        super().__init__(sample_rate, buffer_size, mixer_size, peak)
        self._sounds = {}
        pygame.mixer.pre_init(
            frequency=self.sample_rate,
            size=self.mixer_size,
            channels=self.channels,
            buffer=self.buffer_size,
            allowedchanges=0,
        )

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape: str):
        if new_shape == "sine":
            self._shape = new_shape
            self._wave_fn = self.sine_wave
        elif new_shape == "square":
            self._shape = new_shape
            self._wave_fn = self.square_wave
        else:
            raise f"Shape {new_shape} not implemented!"

    def stop_sound(self, hz):
        sound = self._sounds[hz]
        sound.stop()

    def play_sound_at_hz(self, hz: float, ms=0):
        wave = self._wave_fn(hz)
        sound = pygame.sndarray.make_sound(wave)
        self._sounds[hz] = sound
        sound.play(-1)
        if ms > 0:
            pygame.time.delay(ms)
            sound.stop()

    # def play_chord_with_ratios_over_hz(self, hz: float, ratios: list, ms=0):
    #     wave = self._wave_fn(hz)
    #     for r in ratios[1:]:
    #         wave = sum([wave, self._wave_fn(hz * r / ratios[0])])
    #     self.sound = pygame.sndarray.make_sound(wave)
    #     self.sound.play(-1)
    #     if ms > 0:
    #         pygame.time.delay(ms)
    #         self.sound.stop()

    def handle_music_key_press(self, key):
        try:
            self.play_sound_at_hz(self.scale[key])
        except KeyError as e:
            print("Key not implemented!", e)

    def handle_music_key_release(self, key):
        try:
            self.stop_sound(self.scale[key])
        except KeyError as e:
            print("Key not implemented!", e)

    def transpose_up(self):
        hz_vals = list(self.scale.values())
        self.base_hz = hz_vals[1]

    def octave_up(self):
        self.base_hz = self.base_hz * 2

    def octave_down(self):
        self.base_hz = self.base_hz / 2
