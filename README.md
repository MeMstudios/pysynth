# PySynth!

### Background
I started this project one day I was reading about music theory, golden ratios, and the fibonacci sequence.  Not to mention, something about a secret order of the Tool album, _Lateralus_, one of my favorite albums of all time.  Naturally I wanted to try and code something so I can gain a better understanding of it.  

The quickest way for me to experiment with code is using Python!  However, I couldn't find many great Python implementations of sound generation.  Also being a synthesizer lover, I decided to try to code a standalone synth in Python.  

### Requirements
Python3, Pygame, numpy

## Synth
It turns out, there are two ways you can divide the western music scale into note ratios: theoretical ratios and equal temperament ratios.  Both are at the top of the file and theoretical ratios are commented out because I found the equal temperament to be more suitable for this environment as they are more rigorous and don't include repeating numbers (0.66666).  

### BaseSynth
The BaseSynth is where I'm using some fancy Python syntax to set the scale dict using the current base_hz (default to 440) and the ratios constant.  The keys of the dict are the pygame keyboard key constants mimicking a piano starting on A (440 hz).  So, you can play a minor scale by going straight across the middle row, a through k.  

In the wave functions, we use numpy to generate arrays using equations I worked over from examples and some AI assistance.  These can be converted to audio using pygame's sndarray module!  

### MonoSynth
This is the first implementation of the BaseSynth where we use pygame to initialize a mixer and implement a shape setter.  

The methods `play_sound_at_hz` and `stop_sound` access a dict of pygame Sound objects to play or stop them.  

`handle_music_key_press` expects you to handle keys not related to music before calling this.  

The transpose and octave functions update the scale by setting the base_hz.  

## Main
In the main file we initialize the MonoSynth and the pygame event loop.  We'll handle any key presses aside from the music notes.  I have a purple window which will display a sine wave at your frequency and sample rate.  My idea is to create a new class that excepts a synth and generates the point plots to display the waves.  