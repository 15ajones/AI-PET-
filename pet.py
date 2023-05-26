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
#THINK ABOUT EMAILING OR SOMETHING, AS MOST OLD PEOPLE USE EMAIL

class PET:
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

        self.lastAudioInput = ""
    
   

    def increase_happiness_level(self): #(ALEERA)
        #when this is called, the happiness level is updated to increase (this function will be triggered by either speaking to the pet or button pressing)
        #how much the happiness level is increased by is still to be determined
        pass

    def decrease_happiness_level(self): #(ALEERA)
        #when this is called, the happiness level is decreased. This function will be called by a timer reaching a certain value (its called more, the more time passes since the last interaction with the pet)
        pass


    #------------CODE FOR ANY THREADS WHICH RUN CONSTANTLY--------------------------------------------------------------------------

    def button_thread(self): #(this function calls increase happiness level)
        #this function will be run as a thread constantly (you should constantly be able to detect a button press)
        while True:
            if not GPIO.input(18):#replace with wherever the button is
                #button has been pressed
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
            # 4. update happiness level (based on time since last interaction)
            # 5. based on happiness level maybe switch to the seek attention state
        pass

    def listenState(self): #kihyun
        #in this function you:
        #listen for 10 seconds using mic
        #save this audio to a file
        #translate the audio file into text
        #save text in self.lastAudioInput
        pass

    def replyState(self): #kihyun
        #takes the self.lastAudioInput
        #translates to audio and save as a file
        #play the audio via the speaker
        pass

    def seekAttentionState(self): #kihyun
        #seeks attention
        #takes the string "hi where are you"
        #plays that through the speaker
        pass

    #-----------------------------------------------------------------------------------------------------------------------------------         


    # ------MAIN------
    def main(self):
        while True:
            if self.petState == 0:
                self.idleState()
            if self.petState == 1:
                self.listenState()
            if self.petState == 2:
                self.replyState()
            if self.petState == 3:
                self.seekAttentionState()
            
