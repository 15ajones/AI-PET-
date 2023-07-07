# import pygame

# # Initialize Pygame
# pygame.init()

# # Set the audio device
# pygame.mixer.init()

# # Load the audio file
# sound = pygame.mixer.Sound("output.wav")

# # Play the audio file
# sound.play()

# # Wait until the sound finishes playing
# pygame.time.wait(sound.get_length() * 1000)

# # Quit Pygame
# pygame.quit()

# import simpleaudio as sa

# filename = 'output.wav'
# wave_obj = sa.WaveObject.from_wave_file(filename)
# play_obj = wave_obj.play()
# play_obj.wait_done()  # Wait until sound has finished playing

#!usr/bin/env python  
#coding=utf-8  

import pyaudio  
import wave  

#define stream chunk   
chunk = 1024  

#open a wav format music  
f = wave.open(r"output.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)  

#play stream  
while data:  
    stream.write(data)  
    data = f.readframes(chunk)  

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate() 