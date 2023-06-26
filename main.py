import time
import sys
import random
from datetime import datetime
import pytz
from timeit import default_timer
import pyaudio
import RPi.GPIO as GPIO
import wave
import pydub
import simpleaudio
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
from ibm_watson import AssistantV2
from ibm_watson import SpeechToTextV1
from nlp import hasTime, hasDate, getOccurence, getStrongestEmotion, categoriseText
from newsapiFile import getTopNewsHeadlines
import pygame
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

from watson_assistant_functions import spotify_track_find_and_play
from watson_assistant_functions import get_weather_data
from watson_assistant_functions import play_response
from watson_assistant_functions import spotify_podcast_find
from watson_assistant_functions import record_audio
from watson_assistant_functions import spotify_track_find_and_play_v2
from calendarFile import Event, Day, CalendarClass
from smsapiFile import sendSMS
from emailFile import list_emails, getService, getNewEmails
#from weather import Weather
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


import board
import busio
# Import MPR121 module.
import adafruit_mpr121

# Set up the Watson Assistant credentials
api_key = 'p7Fj1Ty5O5Qi_BWHYehHC1jA3ai2r14wgyRlqghSJe8u'
assistant_url = 'https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/90bab243-6d6c-4c20-915e-b9c50e07883a'
assistant_id = '89672e43-8b25-4ee6-bf98-81c10aab9800'
action_skill_id = 'aeb1f59d-0354-483e-8730-52c792c569e3'
dialog_skill_id = 'db4c637a-587d-489f-82fc-eabdd9122335'
draft_environment_id = 'e327fd2f-fb3b-4117-96f9-2746faa0fa3d'
live_environment_id = 'c10287b5-463e-4c01-82a2-7988df39a298'

# Set up the Speech to Text service
apikey_speech_to_text = 'vIC0cr98ZS3tO7FxgceuzsjCrhDUjiMc2IbSEtSdEzjv'
url_speech_to_text = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/cbab904d-34fb-41dc-a0fd-40cca19ff9e6'
authenticator = IAMAuthenticator(apikey_speech_to_text)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url_speech_to_text)

# Set up the Text to Speech service
apikey_text_to_speech = 'Hr1EeXcU03t3n9kXgNLGI6_7OaDpApVkVjfWaUuM3svT'
url_text_to_speech = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/033cb2d2-2c96-450b-ac92-3eee1477221c'
authenticator = IAMAuthenticator(apikey_text_to_speech)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url_text_to_speech)

# Spotify API credentials
client_id = 'a5c2a4ce9c0c463fa474bf55fb0750c7'
client_secret = '34446cd588974b158fd968ce46bd608b'
redirect_uri = 'http://localhost:8888/callback'
username = 'ab4o1l8is3u3ssvxwbqobt4qo'

# Authenticate with Watson Assistant
authenticator = IAMAuthenticator(api_key)
assistant = AssistantV2(
    version='2021-11-27',
    authenticator=authenticator
)

assistant.set_service_url(assistant_url)

#response=assistant.get_workspace(workspace_id=dialog_skill_id).get_result()

# Create a session with Watson Assistant
session = assistant.create_session(draft_environment_id).get_result()
#session = assistant.create_session(live_environment_id).get_result()
session_id = session['session_id']


class Pet:
    def __init__(self):
        

        self.petState = 0
        #0 is idle (goes to either state 1 or 3)
        #1 is listening (goes to either state 0 or 2)
        #2 is replying (goes to either 0 or 1)
        #3 is seeking attention (goes to either 0 or 1)
        self.userName = ""
        self.location = "London"
        self.happinessLevel = 10.0
        #happiness level is minimum 0, maximum 10 (different emotion face for every 2 levels, so we need 5 emotion faces)
        #below happiness level of 5, the pet begins to seek attention
        #how often the pet seeks attention increases until happiness level 2, then begins to decrease (the pet is now low energy) (so rise and then fall between 0 and 5, like a bell curve )
        
        self.animalType = "dog" #we are assuming its dog for now, but we can eventually change this to also include cat
        self.unhappinessTimer = time.time()
        self.lastAudioInput = ""

        self.reply_text = "Hello, My name is NOVA. How can I help you today?" # Default reply text for replystate.

        self.seekattention_text = "Hi, Where are you?" # When the state becomes seekattention_state, NOVA speaks seekattention_text
        self.eventsToAnnounce = []
        self.counter = 0 #counts the number of waiting state of NOVA
        self.trackcounter = 0 # counts the number of tracks in the tracklist
        self.seekattention_counter = 0 #counts the number of visiting seekattentionState
        self.emergency_counter = 0
        # self.emailService = getService()
        self.prevTime = int(time.time())
        self.calendar = CalendarClass(currentDayIndex=0)#change this to be the correct day at some point
        button_t = threading.Thread(target=self.button_thread)
        button_t.start()

        notification_t = threading.Thread(target=self.notification_thread)
        notification_t.start()

        touch_sensor_t = threading.Thread(target=self.touch_sensor_thread)
        touch_sensor_t.start()

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
                elif self.petState == 4:
                    self.petState = 0
                print("button pressed")
                time.sleep(1)


    def notification_thread(self):
        current_time = time.time()
        while True:
            time.sleep(1)
    
            if self.petState==0:
                if time.time() - current_time >= 10:
                    print("checking for notifications")
                    current_time = time.time()

                    tz_London = pytz.timezone('Europe/London')

                    # Get the current time in London
                    datetime_London = datetime.now(tz_London)

                    # Format the time as a string and print it
                    dayTime = datetime_London.strftime("%H%M")


                    # get day of week as an integer
                    dayIndex = datetime_London.weekday()
                    
                    newAnnouncement = self.calendar.checkAnnouncements(dayTime)#change it to be the current time
                    if newAnnouncement == "alarm":
                        self.petState = 4
                    elif newAnnouncement:
                        self.eventsToAnnounce.append(newAnnouncement)

                    self.calendar.possibleChangeDay(dayIndex)
                    # getNewEmails(self.emailService, self.prevTime) #this prints
                    self.prevTime = int(time.time())

    def touch_sensor_thread(self):
        # Create I2C bus.
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create MPR121 object.
        mpr121 = adafruit_mpr121.MPR121(i2c)
        # Loop forever testing each input and printing when they're touched.
        while True:
            
           
               # Loop through all 12 inputs (0-11).
            if self.petState == 0:
                   
              for i in range(12):
                # Call is_touched and pass it then number of the input.  If it's touched
                # it will return True, otherwise it will return False.
                if mpr121[i].value:
                    print("increasing happiness level because of stroking")
                    self.increase_happiness_level(0.05)

            time.sleep(0.25)  # Small delay to keep from spamming output messages.

#
            

        

    #------------- CODE FOR SETUP ----------------------------------------------------------------
    def setup(self):
        #what we need to do:
        # 1. get name 
        # 2. get where you live 
        # 3. get cat or dog
        # 4. get emergency contact 
        print("hi there! I'm Nova, your new pet and smart assistant! To get started, I need to ask you a few questions")
        time.sleep(1)
        print("firstly, what is your name?")
        self.userName = self.getVoiceInput()
        print("excellent, now what country/city do you live in")
        self.location = self.getVoiceInput()
        print("")
        print("and what animal do you prefer between a dog and a cat?")
        self.animalType = self.getVoiceInput()
        print("perfect, we're ready to get started")


    # every attention seek, we do a probability
    # 1. hey, give me attention 
    # 2. hey, how're you doing
    # 3. checking if calendar is free and if more than an hour is free: recommend a task between meditate (play meditation), exercise (play easy yoga), podcast
    

    #----------------------------------------------------------------------------------------------



    #----------------------------------------------------------------------------------------------------------------------------------

    #CODE FOR STATES

    def initiateProb(self, happinessLevel, animalType):#check if values are okay
        if animalType == "dog":
            multiplier = 1.25
        else:
            multiplier = 1
        if happinessLevel < 1.0:
            return 0.8*multiplier
        elif happinessLevel < 2.0:
            return 0.5*multiplier
        elif happinessLevel < 3.0:
            return 0.3*multiplier
        elif happinessLevel < 4.0:
            return 0.2*multiplier
        elif happinessLevel < 5.0:
            return 0.1*multiplier
        else:
            return 0
        
    def idleState(self): #(this calls decrease happiness level)(ALEERA)
        #in this function you:
            # 1. display the current emotion level
            # 2. display the whether
            # (^^ these display tasks will be called by calling functions defined in screen.py)
            # 3. check for notifications (don't do this yet)
            # 4. update happiness level (based on time since last interaction) y
            # 5. based on happiness level maybe switch to the seek attention state y
        time.sleep(1)
        if(time.time()-self.unhappinessTimer > 15):#this is the number to set how often it gets less happy
            print("becoming less happy")
            self.decrease_happiness_level(0.2)
            self.unhappinessTimer = time.time()
            randomNum = random.random()
            print("randomNum: ", randomNum)
            if randomNum < (self.initiateProb(self.happinessLevel, self.animalType)):
                self.petState = 3
            #if self.happinessLevel < 1.0:
             #   if randomNum < 0.2:
              #      self.petState = 3
            #elif self.happinessLevel < 2.0:
             #   if randomNum < 0.4:
              #      self.petState = 3
            #elif self.happinessLevel < 3.0:
             #   if randomNum < 0.8:
              #      self.petState = 3
            #elif self.happinessLevel < 4.0:
             #   if randomNum < 0.5:
              #      self.petState = 3
            #elif self.happinessLevel < 5.0:
             #   if randomNum < 0.3:
              #      self.petState = 3
        print("in idle state. happinss level: ", self.happinessLevel)
        #display stuff -> get the emotion level and display the face
        #get the weather -> display the weather
        

        #announcing calendar events
        while len(self.eventsToAnnounce) > 0:
            event = self.eventsToAnnounce.pop(0)
            print("you have ", event, " coming up in less than 15 minutes")#needs to be replaced with the speaker


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
        dev_index = 1
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

        #---------------------------------------------------------------------
        # Initialize the recognizer
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile('audio.wav') as source:
                audio = recognizer.record(source)
                # self.lastAudioInput = recognizer.recognize_google(audio)
                recognized_text = recognizer.recognize_google(audio)
                print("audio input was: ", recognized_text)
                self.lastAudioInput = recognized_text
                self.petState = 2
                return
                #return text
        #except sr.UnknownValueError:
        #    print("Speech recognition could not understand audio.")

        #NLP STUFF GOES HERE
        except:
            print("couldn't translate audio to text")
            self.lastAudioInput = "error"
            self.petState = 2
            return

        


    

    def seekMoreInfo(self, infoTitle):
        print("please provide the ",infoTitle, " for the event.")#played by the speaker
        newInfo = self.getVoiceInput()
        while newInfo == 0:
            print("didn't hear that. please provide the ",infoTitle, " for the event.")
            newInfo = self.getVoiceInput()
        return newInfo

    def getVoiceInput(self):
        sample_rate = 44100
        chans = 1
        chunk = 1024
        filename = 'audio.wav'
        duration = 5
        dev_index = 1
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

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile('audio.wav') as source:
                audio = recognizer.record(source)
                # self.lastAudioInput = recognizer.recognize_google(audio)
                recognized_text = recognizer.recognize_google(audio)
                print("audio input was: ", recognized_text)
                return recognized_text
       

        except:
            print("couldn't translate audio to text")
            return 0

    def replyState(self):
        print("in reply state")
        recognized_text = self.lastAudioInput
        print("last audio input was: ", recognized_text)
        
        #-----------------------------------------------------------------------
        #CALENDAR SHIIIIIT
        task = categoriseText(recognized_text)
        print("task is: ", task)
        
        task = list(task)
        for i in range(len(task)):
            if len(task[i]) > 0:
                task[i] = task[i][0]
            else:
                task[i] = ""
        print("formatted task is: ", task)
        taskTitle = task[0]
        

        
        """
        1. check, plan, alarm, reminder    (p, e, w, n, m, conv)

        check -> day -> time
        plan -> day -> time -> activity
        alarm -> day -> time -> name -> occurance
        reminder -> day -> time -> name -> occurance
        gugug
        types of day: "today", "tomorrow", "yesterday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"
        """
        if taskTitle == "check" or taskTitle == "plan" or taskTitle == "alarm" or taskTitle == "reminder":
            for i in range(len(task)):
                if i == 0:
                    continue
                elif i == 1 and task[i] == "":
                    task[i] = self.seekMoreInfo("day")
                elif i == 2 and task[i] == "":
                    task[i] = self.seekMoreInfo("time")
                elif i == 3 and task[i] == "":
                    if len(task) == 4:
                        task[i] = self.seekMoreInfo("activity")
                    else:
                        task[i] = self.seekMoreInfo("name")
                elif i == 4 and task[i] == "":
                    task[i] = self.seekMoreInfo("occurance")

            if taskTitle == "check":
                result = self.calendar.check(task[1], task[2])
                print("checking calendar. result is this: ", result)
            elif taskTitle == "plan":
                result = self.calendar.plan(task[1], task[2], task[3])
                print("planning in calendar. result is this: ", result)
            elif taskTitle == "alarm":
                result = self.calendar.setAlarm(task[1], task[2])
                print("adding alarm. result is this: ", result)
            elif taskTitle == "reminder":
                result = self.calendar.plan(task[1], task[2], "reminder "+ task[3])
                print("adding reminder. result is this: ", result)


            self.petState = 0
            return
        
        #------------------------------------- NEWS ------------------------------
        if taskTitle == "n":
            print("Here are the news headlines")
            print(getTopNewsHeadlines(task[1]))
            self.petState = 0
            return
        #-------------------------------------------------------------------------

        else:
            response = assistant.message(
            assistant_id=draft_environment_id,
            session_id=session_id,
            input={
                'message_type': 'text',
                'text': self.lastAudioInput
            }
            ).get_result()
            # Retrieve and print Watson Assistant's response
            try:
                response_text = response['output']['generic'][0]['text']
            except:
                print("I didn't understand. Press my button if you want to repeat yourself.")
                self.petState = 0
                return
            print("Watson Assistant: ", response_text)

        
            if(response_text == "waiting for reply"):
                self.counter = self.counter + 1
                if(self.counter > 10): #condition to move on to the seekattention state
                    self.petState = 3
                else:
                    self.petState = 1
        
    #-------------------------------------------------------------------------------------------------------------------------------------
    #News_Podcast

            elif(response_text == 'News Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('The News Agent', 'Lord, Ladies, and Boris Johnson honour')
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Comedy_Podcast

            elif(response_text == 'Comedy Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('Please Tell Me A Story', 'Omid: "A Fine Piece Of Ass')
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Sports_Podcast_Tennis

            elif(response_text == 'Tennis Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('The Tennis Podcast', 'Roland Garros Day 14 - lga in a classic; Djokovic-Ruud preview')
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Sports_Podcast_Cricket

            elif(response_text == 'Cricket Podcast will be played soon'):

                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('The Vaughany and Tuffers Cricket Club', 'Reflecting on an incredible year with Sam Curran')
                self.petState = 1


    #-------------------------------------------------------------------------------------------------------------------------------------
    #Sports_Podcast_Football

            elif(response_text == 'Football will be played soon'):
            
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('Football Daily', 'The Day After Man Citys Treble Win')
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Sports_Podcast_Golf

            elif(response_text == 'Golf Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('Beefs Golf Club', 'The First Tee')
                self.petState = 1


    #-------------------------------------------------------------------------------------------------------------------------------------
    #Music_Podcast_Pop

            elif(response_text == 'Pop Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('Switched on Pop', 'Listening to Draft Punk: Random Access Memories')
                self.petState = 1


    #-------------------------------------------------------------------------------------------------------------------------------------
    #Music_Podcast_Classic

            elif(response_text == 'Classic Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('That Classic Podcast', 'So long, farewell, auf wiedersehan, goodbye!')
                self.petState = 1


    #-------------------------------------------------------------------------------------------------------------------------------------
    #Music_Podcast_Jazz

            elif(response_text == 'Jazz Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('The Jazz Session', 'The Jazz Session #617: Bill Lowe')
                self.petState = 1


    #-------------------------------------------------------------------------------------------------------------------------------------
    #Music_Podcast_Rock

            elif(response_text == 'Rock Podcast will be played soon'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_podcast_find('Rockonteurs with Gary Kemp and Guy Pratt', 'S4E27: Jerry Shirley')
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Weather
            elif(response_text == 'Checking the weather right now in London'):
                
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                get_weather_data()
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Playing_track

            elif(response_text == 'Sure, can you kindly teach me the title of the music and the name of the artist?'):

                # play_response(response_text)
                print("the speaker would say: ", response_text)
                spotify_track_find_and_play()
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Pausing_state

            elif(response_text == "Pausing the audio"):
                # Create OAuth Object
                oauth_object = spotipy.SpotifyOAuth(client_id,client_secret,redirect_uri)

                # Create token
                token_dict = oauth_object.get_access_token()
                token = token_dict['access_token']

                # Create Spotify Object
                spotifyObject = spotipy.Spotify(auth=token)

                # Create a Spotipy client with user authorization
                scope = 'user-read-playback-state,user-modify-playback-state'
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

                sp.pause_playback()
                # play_response("The audio is now paused")
                print("the speaker would say: the audio is now paused")
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1
    #-------------------------------------------------------------------------------------------------------------------------------------
    #Irrelevant

            elif(response_text == 'irrelevant'):

                #play_response("I am sorry could you repeat what you just said?")
                print("I am sorry could you repeat what you just said?")
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1

    #-------------------------------------------------------------------------------------------------------------------------------------
    #Termination

            elif(response_text == "Bye Bye!"):
                # End the session
                #play_response(response_text)
                print("the speaker would say: ", response_text)
                self.counter = 0
                self. emergency_counter = 0

                assistant.delete_session(draft_environment_id, session_id)
                sys.exit()
                #self.petState = 1
    #-------------------------------------------------------------------------------------------------------------------------------------
            else:
                # play_response(response_text)
                print("the speaker would say: ", response_text)
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1
    #-------------------------------------------------------------------------------------------------------------------------------------
    
    #def seekAttentionState(self):
    
    #    print("in seek attention state")
    #    print("I'm seeking attention")#play on speaker
    #    self.petState = 0


    def seekAttentionState(self):
        file_name = "tracklist.txt"

        print("in seek attention state")
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()
                number_of_track = len(lines)
        except:
            pass


        if(number_of_track > 1 and self.seekattention_counter % 2 == 0):
            #play_response("Everyday is a good day to listen to music, can I play a song based on your playing history?")
            print("Everyday is a good day to listen to music, can I play a song based on your playing history?")
            record_audio()

            try:
                with open('audio.wav', 'rb') as audio:
                    response = speech_to_text.recognize(audio=audio, content_type='audio/wav')
                    text = response.result['results'][0]['alternatives'][0]['transcript']
                    #return text
            except :
                print("Speech recognition could not understand audio.")
                text = "pass"
            
            if("yes" in text or "sure" in text or "go" in text):
                try:
                    with open(file_name, "r") as file:
                        lines = file.readlines()
                        random_track = random.choice(lines).strip()
                        spotify_track_find_and_play_v2(random_track)
                        self.seekattention_counter = self.seekattention_counter + 1
                        self.counter = 0
                        self.trackcounter = number_of_track
                        self.petState = 1
                except FileNotFoundError:
                    print("The file does not exist.")
                    #play_response("The file does not exist")
                    self.seekattention_counter = self.seekattention_counter + 1
                    self.counter = 0
                    self.petState = 1
                    pass
                except IOError:
                    print("An error occurred while reading the file.")
                    #play_response("An error occurred while reading the file")
                    self.seekattention_counter = self.seekattention_counter + 1
                    self.counter = 0
                    self.petState = 1
                    pass
            
            elif("no" in text or "stop" in text):
                #play_response("Okay let me know if you need anything else")
                print("Okay let me know if you need anything else")
                self.seekattention_counter = self.seekattention_counter + 1
                self.counter = 0
                self.emergency_counter = 0
                self.petState = 1
            
            elif("pass" in text):
                self.seekattention_counter = self.seekattention_counter + 1
                self.emergency_counter = self.emergency_counter + 1
                self.counter = 0
                self.petState = 1
            

            else:
                self.seekattention_counter = self.seekattention_counter + 1
                self.counter = 0
                self.emergency_counter = self.emergency_counter + 1
                self.petState = 1



        elif(self.trackcounter == 0 and self.seekattention_counter % 2 == 0):
            #play_response("Let me know your taste of music! I can search a music and play it for you. Try this by just saying play me a music!")
            print("Let me know your taste of music! I can search a music and play it for you. Try this by just saying play me a music!")
            
            
            self.seekattention_counter = self.seekattention_counter + 1
            self.counter = 0
            self.petState = 1
        #-------------------------------------------------------------------------------------------------------------------------------------
        #Emergency state
        elif(self.emergency_counter > 4):
            print("Are you okay? If don't respond to this I am assuming you are in danger and I am asking for some help to your Whatsapp friend")
            sendSMS()
            sys.exit()
        
        #-------------------------------------------------------------------------------------------------------------------------------------
        
        else:
            #play_response("Hello, where are you?")
            print("Hello where are you?")
            self.seekattention_counter = self.seekattention_counter + 1
            self.counter = 0
            self.petState = 1


    def alarmState(self):
        print("sounding alarm")
        # pygame.mixer.init()

        # # Load the audio file
        # audio_file = "digital_alarm.wav"
        # pygame.mixer.music.load(audio_file)

        # # Play the audio file
        # pygame.mixer.music.play()

        # # while audio playing, wait
        # while pygame.mixer.music.get_busy():
        #  pygame.time.Clock().tick(10)

        
        # pygame.mixer.quit()

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
            if self.petState == 4:
                self.alarmState()



def __main__():

    pet = Pet()
    pet.run()

__main__()

"""
to do:
1. touch sensor
2. screen
3. make speaker work in main
2. aleera - email notifications
3. aleera email reply by voice?
4. aleera add whatsapp notifications
5. aleera add if happiness level stays low for too long sends messages to emergency contacts
6. anthony - asking what plan is for your day
7. anthony - other things that make it human (positive stuff, recommending meditating)
7. anthony - set up sequence
7. anthony - cat and dog mode
8. kihyun - do specific recommendations
9. kihyun - modify spotify code on main branch
10. kihyun - saving interests in a text file
"""
