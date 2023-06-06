import time
import random
from timeit import default_timer
import pyaudio
import RPi.GPIO as GPIO
import wave
import speech_recognition as sr
from ctypes import *
from contextlib import contextmanager
import requests
import uuid
import os
import json
from PIL import Image
import pyttsx3
import gtts
import threading
#from weather import Weather
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Pet:
    def __init__(self):
        

        self.petState = 0
        #0 is idle (goes to either state 1 or 3)
        #1 is listening (goes to either state 0 or 2)
        #2 is replying (goes to either 0 or 1)
        #3 is seeking attention (goes to either 0 or 1)
        self.happinessLevel = 10.0
        #happiness level is minimum 0, maximum 10 (different emotion face for every 2 levels, so we need 5 emotion faces)
        #below happiness level of 5, the pet begins to seek attention
        #how often the pet seeks attention increases until happiness level 2, then begins to decrease (the pet is now low energy) (so rise and then fall between 0 and 5, like a bell curve )
        
        self.animalType = "dog" #we are assuming its dog for now, but we can eventually change this to also include cat
        self.unhappinessTimer = time.time()
        self.lastAudioInput = ""

        self.reply_text = "Hello, My name is NOVA. How can I help you today?" # Default reply text for replystate.

        self.seekattention_text = "Hi, Where are you?" # When the state becomes seekattention_state, NOVA speaks seekattention_text

        button_t = threading.Thread(target=self.button_thread)
        button_t.start()
    
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
                print("button pressed")
                time.sleep(1)

    #----------------------------------------------------------------------------------------------------------------------------------

    #CODE FOR STATES


    def idleState(self): #(this calls decrease happiness level)(ALEERA)
        #in this function you:
            # 1. display the current emotion level
            # 2. display the whether
            # (^^ these display tasks will be called by calling functions defined in screen.py)
            # 3. check for notifications (don't do this yet)
            # 4. update happiness level (based on time since last interaction) y
            # 5. based on happiness level maybe switch to the seek attention state y
        time.sleep(0.5)
        if(time.time()-self.unhappinessTimer > 15):
            print("becoming less happy")
            self.decrease_happiness_level(0.2)
            self.unhappinessTimer = time.time()
            randomNum = random.random()
            print("randomNum: ", randomNum)
            if self.happinessLevel < 1.0:
                if randomNum < 0.2:
                    self.petState = 3
            elif self.happinessLevel < 2.0:
                if randomNum < 0.4:
                    self.petState = 3
            elif self.happinessLevel < 3.0:
                if randomNum < 0.8:
                    self.petState = 3
            elif self.happinessLevel < 4.0:
                if randomNum < 0.5:
                    self.petState = 3
            elif self.happinessLevel < 5.0:
                if randomNum < 0.3:
                    self.petState = 3
        print("in idle state. happinss level: ", self.happinessLevel)
        
        


    def listenState(self): #kihyun
        #in this function you:
        #listen for 10 seconds using mic
        #save this audio to a file
        #translate the audio file into text
        #save text in self.lastAudioInput
        #save this audio to a file called 'audio.wav'
        print("in listen state")
        # Set the sample rate, channels, and chunk size
        sample_rate = 44100
        chans = 1
        chunk = 1024
        filename = 'audio.wav'
        duration = 5
        dev_index = 0
        # Initialize PyAudio
        audio_interface = pyaudio.PyAudio()
        print("Device count:")
        print(audio_interface.get_device_count())
        print("max input channels:")
        print(audio_interface.get_default_input_device_info()['maxInputChannels'])
        # Open the microphone stream
        stream = audio_interface.open(format = pyaudio.paInt16, rate=sample_rate, channels = chans, input_device_index = dev_index,input = True,frames_per_buffer=chunk)
        
        # Start recording
        print("Recording started...")
        frames = []
        for i in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

        # Stop recording
        print("Recording ended!")
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
        self.unhappinessTimer = time.time()
        self.decideTask() #go straight to processing
      

        
    def decideTask(self): #kihyun
        print("in decide task state")
        #In this state,
        #translate the audio file('audio.wav') into text
        #save text in self.lastAudioInput

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile('audio.wav') as source:
                audio = recognizer.record(source)
                # self.lastAudioInput = recognizer.recognize_google(audio)
                print(recognizer.recognize_google(audio))
                #return text
        #except sr.UnknownValueError:
        #    print("Speech recognition could not understand audio.")

        #NLP STUFF GOES HERE
        except:
            print("couldn't translate audio to text")
            pass
        self.petState = 2

    def replyState(self):
        print("in reply state")
        print("replying!!!")
        self.petState = 0

    def seekAttentionState(self):
        print("in seek attention state")
        print("I'm seeking attention")
        self.petState = 0
    def run(self):
        while(True):
            if self.petState == 0:
                self.idleState()
            if self.petState == 1:
                self.listenState()
            if self.petState == 2:
                self.replyState()
            if self.petState == 3:
                self.seekAttentionState()
   

def __main__():
    pet = Pet()
    pet.run()

__main__()