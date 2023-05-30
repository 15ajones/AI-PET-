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


class PET:
    class WEATHER:
        def __init__(self):
            self.currentWeather = "default"
            self.previousWeather = self.currentWeather
            self.previousWeatherEffect = 0.0
            #weather types = "default", "sunny", "rainy", "thunder" for now**
        def getWeather(self):
            #here would be the call to the api to get the current weather
            pass
       # def changeWeather(self): #FUNCTION USED FOR TESTING
        #    self.previousWeather = self.currentWeather;
         #   if self.currentWeather == "default":
          #      self.currentWeather = "sunny"
          #  elif self.currentWeather == "sunny":
           #    self.currentWeather = "rainy"
           # elif self.currentWeather == "rainy":
           #    self.currentWeather = "thunder"
           # elif self.currentWeather == "thunder":
           #    self.currentWeather = "default"
        def getWeatherEffect(self):
            def weatherEffectChange(weatherVal):
                weatherEffect = weatherVal - self.previousWeatherEffect
                self.previousWeatherEffect = weatherVal
                return weatherEffect
            if self.currentWeather == "default":
                return weatherEffectChange(0.0)
            elif self.currentWeather == "sunny":
                return weatherEffectChange(1.0)
            elif self.currentWeather == "rainy":
                return weatherEffectChange(-1.0)
            elif self.currentWeather == "thunder":
                return weatherEffectChange(-2.0)

    def __init__(self):
        self.petState = 0
        #0 is idle (goes to either state 1 or 3)
        #1 is listening (goes to either state 0 or 2)
        #2 is replying (goes to either 0 or 1)
        #3 is seeking attention (goes to either 0 or 1)
        self.weather = self.WEATHER()
        self.happinessLevel = 10.0
        #happiness level is minimum 0, maximum 10 (different emotion face for every 2 levels, so we need 5 emotion faces)
        #below happiness level of 5, the pet begins to seek attention
        #how often the pet seeks attention increases until happiness level 2, then begins to decrease (the pet is now low energy) (so rise and then fall between 0 and 5, like a bell curve )
        
        self.animalType = "dog" #we are assuming its dog for now, but we can eventually change this to also include cat

        self.lastAudioInput = ""
    
    
    #also need to include when being stroked?
    def increase_happiness_level(self,increaseValue): 
        self.happinessLevel += increaseValue
        if self.happinessLevel > 10.0:
            self.happinessLevel = 10.0

    def decrease_happiness_level(self,decreaseValue):
        self.happinessLevel -= decreaseValue
        if self.happinessLevel < 0.0:
            self.happinessLevel = 0.0


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
            
            while self.petState == 0:

                time.sleep(1)#need to change this (threading) so that it is not blocking
                #will change to 30mins?
                if(self.weather.currentWeather != self.weather.previousWeather):#will probably be an interupt instead that is called when there is a change
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
        self.increase_happiness_level(0.2);#assuming this is after listening for 10 seconds

    def replyState(self): #kihyun
        #takes the self.lastAudioInput
        #translates to audio and save as a file
        #play the audio via the speaker
        self.increase_happiness_level(0.2);#is this needed

    def seekAttentionState(self): #kihyun
        #seeks attention
        #takes the string "hi where are you"
        #plays that through the speaker
        pass

    #-----------------------------------------------------------------------------------------------------------------------------------         


    # ------MAIN------
    def main(self):
        print(self.petState)
        while True:
            if self.petState == 0:
                self.idleState()
            if self.petState == 1:
                self.listenState()
            if self.petState == 2:
                self.replyState()
            if self.petState == 3:
                self.seekAttentionState()
   

pet = PET()
pet.main()
