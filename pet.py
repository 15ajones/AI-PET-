import time
import random
from timeit import default_timer
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
import pyttsx3
import gtts
from weather import Weather
from threading import thread
#THINK ABOUT EMAILING OR SOMETHING, AS MOST OLD PEOPLE USE EMAIL

class Pet:

    def __init__(self):
        self.petState = 0
        #0 is idle (goes to either state 1 or 3)
        #1 is listening (goes to either state 0 or 2)
        #2 is replying (goes to either 0 or 1)
        #3 is seeking attention (goes to either 0 or 1)
        self.weather = self.Weather()
        self.happinessLevel = 10.0
        #happiness level is minimum 0, maximum 10 (different emotion face for every 2 levels, so we need 5 emotion faces)
        #below happiness level of 5, the pet begins to seek attention
        #how often the pet seeks attention increases until happiness level 2, then begins to decrease (the pet is now low energy) (so rise and then fall between 0 and 5, like a bell curve )
        
        self.animalType = "dog" #we are assuming its dog for now, but we can eventually change this to also include cat

        self.lastAudioInput = ""

        self.reply_text = "Hello, My name is NOVA. How can I help you today?" # Default reply text for replystate.

        self.seekattention_text = "Hi, Where are you?" # When the state becomes seekattention_state, NOVA speaks seekattention_text
    



    # ------------ HAPPINESS LEVEL CODE --------------------------------------------------------------
    def increase_happiness_level(self,increaseValue): 
        self.happinessLevel = min(10, self.happinessLevel + increaseValue)

    def decrease_happiness_level(self,decreaseValue):
        self.happinessLevel = max(0, self.happinessLevel - decreaseValue)
    # ------------------------------------------------------------------------------------------------


    #------------CODE FOR ANY THREADS WHICH RUN CONSTANTLY--------------------------------------------------------------------------

    def button_thread(self): #(this function calls increase happiness level)
        #this function will be run as a thread constantly (you should constantly be able to detect a button press)
        while True:
            if not GPIO.input(18):#replace with wherever the button is
                #button has been pressed
                self.increase_happiness_level(0.2)
                if(self.petState == 0 or self.petState == 3):
                    self.petState = 1
                time.sleep(1)

    #----------------------------------------------------------------------------------------------------------------------------------



    #-------CODE FOR EACH STATE---------------------------------------------------------------------------------------------------------
    def idleState(self): #(this calls decrease happiness level)(ALEERA)
        #in this function you:
            # 1. display the current emotion level
            # 2. display the whether
            # (^^ these display tasks will be called by calling functions defined in screen.py)
            # 3. check for notifications (don't do this yet)
            # 4. update happiness level (based on time since last interaction) y
            # 5. based on happiness level maybe switch to the seek attention state y
            
         

        time.sleep(1)#need to change this (threading) so that it is not blocking
        #will change to 30mins?
        if(self.weather.currentWeather != self.weather.previousWeather):#will probably be an interrupt instead that is called when there is a change
            weatherEffect = self.weather.getWeatherEffect()
            self.increase_happiness_level(weatherEffect)
            self.weather.previousWeather = self.weather.currentWeather

        self.decrease_happiness_level(1.0)
        print("Happiness decreased. Current happiness level:", self.happinessLevel)
        #self.weather.changeWeather() #for testing
        #WILL VARY PROBABILITIES BASED ON CAT OR DOG
        #MAKE FUNCTION TO EASILY CALCULATE PROBABILITIES
        if self.happinessLevel < 1.0:
            if random.random() < 0.2:
                self.petState = 3
        elif self.happinessLevel < 2.0:
            if random.random() < 0.4:
                self.petState = 3
        elif self.happinessLevel < 3.0:
            if random.random() < 0.8:
                self.petState = 3
        elif self.happinessLevel < 4.0:
            if random.random() < 0.5:
                self.petState = 3
        elif self.happinessLevel < 5.0:
            if random.random() < 0.3:
                self.petState = 3


    def listenState(self): #kihyun
        #in this function you:
        #listen for 10 seconds using mic
        #save this audio to a file
        #translate the audio file into text
        #save text in self.lastAudioInput
        #save this audio to a file called 'audio.wav'

        #----------------------------------------------------------------------------------------------------------------------------------
        # Set the sample rate, channels, and chunk size
        sample_rate = 44100
        channels = 1
        chunk = 1024
        filename = 'audio.wav'
        duration = 10

        audio_interface = pyaudio.PyAudio()

        stream = audio_interface.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)

        #print("Recording started...")
        frames = []
        for i in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        #print("Recording ended!")
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

        # Open a wave file for writing
        wf = wave.open(filename, 'wb')

        # Set the audio file parameters
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)

        # Write the audio frames to the file
        wf.writeframes(b''.join(frames))
        wf.close()
        self.increase_happiness_level(0.2) #assuming this is after listening for 10 seconds
        self.decideTask(self) #go straight to processing


    def decideTask(self): #kihyun
        #In this state,
        #translate the audio file('audio.wav') into text
        #save text in self.lastAudioInput

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile('audio.wav') as source:
                audio = recognizer.record(source)
                self.lastAudioInput = recognizer.recognize_google(audio)
                #return text
        #except sr.UnknownValueError:
        #    print("Speech recognition could not understand audio.")

        #NLP STUFF GOES HERE
        except:
            print("couldn't translate audio to text")
            pass
        
        self.petState = 2 #setting state to reply task state

    def replyState(self): #kihyun
        #takes the self.lastAudioInput
        #translates to audio and save as a file
        #play the audio via the speaker
        

        #----------------------------------------------------------------------------------------------------------------------------------
        #Andy's Code
        #tts = gtts.gTTS(audio, lang="en") #this sets the language to english
        #tts.save("hello.mp3")
        #to play the sound: playsound("hello.mp3")
        
        #----------------------------------------------------------------------------------------------------------------------------------
        #Default response. For now, when the NOVA gets into replystate, it will reply "Hello my name is NOVA"
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Convert text to speech
        engine.say(self.reply_text)
        engine.runAndWait()

        #----------------------------------------------------------------------------------------------------------------------------------
        self.increase_happiness_level(0.2)
        self.petState = 0


    def seekAttentionState(self): #kihyun
        #seeks attention
        #takes the string "hi where are you"
        #plays that through the speaker

        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Convert text to speech
        engine.say(self.seekattention_text)
        engine.runAndWait()
        self.petState = 0


    #-----------------------------------------------------------------------------------------------------------------------------------         


# ------MAIN------
def __main__():

    programPet = Pet()
    print(programPet.petState)
    while True:
        if programPet.petState == 0:
            programPet.idleState()
        if programPet.petState == 1:
            programPet.listenState()
        if programPet.petState == 2:
            programPet.replyState()
        if programPet.petState == 3:
            programPet.seekAttentionState()
   