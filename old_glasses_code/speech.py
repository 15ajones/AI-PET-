import time
import pyaudio
import RPi.GPIO as GPIO
import wave
import speech_recognition as sr
from ctypes import *
from contextlib import contextmanager
from picamera import PiCamera
import requests
import uuid
import os
import json
from PIL import Image


#for text to speech
import gtts
from playsound import playsound
"""
IN ORDER TO DO TEXT TO SPEECH YOU NEED TO INSTALL THE FOLLOWING LIBRARIES:
pip3 install gTTS pyttsx3 playsound
"""
#these are necessary constants to be defined when setting up the microphone to record
FORM_1 = pyaudio.paInt16
CHANS=1
SAMP_RATE = 44100
CHUNK = 4096
RECORD_SECS = 3   #number of seconds you record for
DEV_INDEX = 0
WAV_OUTPUT_FILENAME = 'audio1.wav'


def record_audio(): #records audio and saves it in file called audio1.wav
    audio = pyaudio.PyAudio()
    stream=audio.open(format = FORM_1,rate=SAMP_RATE,channels=CHANS, input_device_index = DEV_INDEX, input=True, frames_per_buffer=CHUNK)
    print("recording")
    frames=[]

    for ii in range(0,int((SAMP_RATE/CHUNK)*RECORD_SECS)):
        data=stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)

    while True:
        data=stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
        if GPIO.input(18):
            break

    print("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    wavefile=wave.open(WAV_OUTPUT_FILENAME,'wb')
    wavefile.setnchannels(CHANS)
    wavefile.setsampwidth(audio.get_sample_size(FORM_1))
    wavefile.setframerate(SAMP_RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

def audio_to_text(): #reads audio from file audio1.wav, translates the audio to a text string and returns this string
    r = sr.Recognizer()
    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile('/home/pi/audio1.wav') as source:
        audio_text = r.listen(source)
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            
            # using google speech recognition
            text = r.recognize_google(audio_text)
            return text
        
        except:
            return ("error")
        


def text_to_audio(audio):
    tts = gtts.gTTS(audio, lang="en") #this sets the language to english
    tts.save("hello.mp3")
    #to play the sound: playsound("hello.mp3")
