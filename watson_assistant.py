from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from watson_speech_to_text import record_audio
#from weather import get_weather_data
import requests

import pyaudio
import json
import speech_recognition as sr
import pyttsx3
import sys
import pydub
import simpleaudio
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import wave
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import json

# Spotify API credentials
client_id = 'a5c2a4ce9c0c463fa474bf55fb0750c7'
client_secret = '34446cd588974b158fd968ce46bd608b'
redirect_uri = 'http://localhost:8888/callback'
username = 'ab4o1l8is3u3ssvxwbqobt4qo'

# Set up the Text to Speech service
apikey_text_to_speech = 'RL8bEBwfNsNhJ8uzZWGVWIWKZi_sIe2eptFqcGdytYXH'
url_text_to_speech = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/5da2b1e5-0bde-4a8c-bd7a-ebb249bb968b'
authenticator = IAMAuthenticator(apikey_text_to_speech)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url_text_to_speech)


def play_response(response_text):
    response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

    # Save the audio to a file
    output_file = "output.wav"
    with open(output_file, 'wb') as audio_file:
        audio_file.write(response_speech.content)

    print("Text to Speech conversion completed.")
    # Load the audio file
    audio = pydub.AudioSegment.from_wav(output_file)

    # Play the audio
    play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    play_obj.wait_done()


def spotify_podcast_find(podcast_name, episode_name):
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

    # Search for a podcast
    #podcast_name = 'The News Agent'
    #episode_name = 'Lord, Ladies, and Boris Johnson honour'
    results = sp.search(q=f'podcast:{podcast_name} episode:{episode_name}', type='episode', limit=1)

    # Extract the URI of the first track found
    if len(results['episodes']['items']) > 0:
        episode_uri = results['episodes']['items'][0]['uri']
        print("Episode URI:", episode_uri)

        # Play the song
        devices = sp.devices()
        if len(devices['devices']) > 0:
            device_id = devices['devices'][0]['id']
            sp.start_playback(device_id=device_id, uris=[episode_uri])
            print("Playing the podcast...")
            #print(device_id)
        else:
            print("No active devices found.")
    else:
        print("Podcast not found.")


def convert_text_to_speech(input_text):

    output_file = "output.wav"
    try:
        # Perform text to speech conversion
        response = text_to_speech.synthesize(input_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

        # Save the audio to a file
        with open(output_file, 'wb') as audio_file:
            audio_file.write(response.content)

        print("Text to Speech conversion completed.")
        # Load the audio file
        audio = pydub.AudioSegment.from_wav(output_file)

        # Play the audio
        play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
        play_obj.wait_done()

    except Exception as e:
        print("Error converting text to speech:", str(e))

def get_weather_data():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = '417af52d6a054b1434bb65cbfd0f2ae2'
    CITY = 'London'

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    if response["cod"] == 200:
        kelvin_temperature = response["main"]["temp"]
        celsius_temperature = kelvin_temperature - 273.15  # Convert from Kelvin to Celsius

        weather_data = {
            "City": response["name"],
            "Weather": response["weather"][0]["description"],
            "Temperature": celsius_temperature,
            "Humidity": response["main"]["humidity"],
            "Wind Speed": response["wind"]["speed"],
            "Visibility": response["visibility"],
        }

        print("Weather in", weather_data["City"])
        print("Description:", weather_data["Weather"])
        #print("Temperature:", weather_data["Temperature"], "°C")
        #print("Humidity:", weather_data["Humidity"], "%")
        #print("Wind Speed:", weather_data["Wind Speed"], "m/s")
        #print("Visibility:", weather_data["Visibility"])

        # Determine the number based on the weather description
        description = weather_data["Weather"].lower()
        if description == "clear sky":
            print("sunny")
            convert_text_to_speech("it is sunny out there")

        elif description in ["few clouds", "scattered clouds", "broken clouds", "overcast clouds"]:
            print("cloudy")
            convert_text_to_speech("it is cloudy out there")

        elif description in ["mist", "fog", "haze", "smoke"]:
            print("foggy")
            convert_text_to_speech("it is foggy out there")

        elif description in ["light rain", "moderate rain", "heavy rain", "showers"]:
            print("rainy")
            convert_text_to_speech("it is rainy out there")

        elif description == "thunderstorm":
            print("thunderstorm")
            convert_text_to_speech("it is storming out there")

        elif description in ["snow", "light snow", "moderate snow", "heavy snow"]:
            print("snowy")
            convert_text_to_speech("it is snowy out there")

        else:
            print("Number: Unknown")

    else:
        print("Error:", response["message"])




def watson_assistant():
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
    apikey_text_to_speech = 'VuaGgCFJlz3O0G0fx7WZYVbY18bz-XvaJoR2_c7529aK'
    url_text_to_speech = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/09dcd622-dc3f-466a-a1c0-48939e44648d'
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
    #print(session_id)

    while True:
    # Send a user input to Watson Assistant
    #user_input = input("Enter your message (or 'exit' to end the session): ")

    #if user_input == 'exit':
    #    break
#-------------------------------------------------------------------------------------------------------------------------------------
        # Set the sample rate, channels, and chunk size
        #Starts the recording and save it as wav file
        sample_rate = 44100
        channels = 1
        chunk = 1024
        filename = 'audio.wav'
        duration = 5

        # Initialize PyAudio
        audio_interface = pyaudio.PyAudio()

        # Open the microphone stream
        stream = audio_interface.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)

        # Start recording
        print("Recording started...")
        frames = []
        for i in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
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
#-------------------------------------------------------------------------------------------------------------------------------------
#Speech to text conversion occurs

        try:
            with open('audio.wav', 'rb') as audio:
                response = speech_to_text.recognize(audio=audio, content_type='audio/wav')
                input_text = response.result['results'][0]['alternatives'][0]['transcript']
                #return text

                
        except :
            #print("Speech recognition could not understand audio.")
            print("No sound detected")
            input_text = 'nothing is detected'

    
#-------------------------------------------------------------------------------------------------------------------------------------

        print(input_text)
        response = assistant.message(
        assistant_id=draft_environment_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': input_text
        }
        ).get_result()
        # Retrieve and print Watson Assistant's response
        response_text = response['output']['generic'][0]['text']
        print("Watson Assistant: ", response_text)


        #if (input_text != 'nothing is detected' and input_text != 'stop') :
        #    response = assistant.message(
        #    assistant_id=draft_environment_id,
        #    session_id=session_id,
        #    input={
        #        'message_type': 'text',
        #        'text': input_text
        #    }
        #    ).get_result()
            # Retrieve and print Watson Assistant's response
        #    response_text = response['output']['generic'][0]['text']
        #    print("Watson Assistant: ", response_text)
        if(response_text == 'waiting for reply'):
            watson_assistant()

#-------------------------------------------------------------------------------------------------------------------------------------
#News_Podcast

        elif(response_text == 'News Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('The News Agent', 'Lord, Ladies, and Boris Johnson honour')


#-------------------------------------------------------------------------------------------------------------------------------------
#Comedy_Podcast

        elif(response_text == 'Comedy Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('Please Tell Me A Story', 'Omid: "A Fine Piece Of Ass')


#-------------------------------------------------------------------------------------------------------------------------------------
#Sports_Podcast_Tennis

        elif(response_text == 'Tennis Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('The Tennis Podcast', 'Roland Garros Day 14 - lga in a classic; Djokovic-Ruud preview')


#-------------------------------------------------------------------------------------------------------------------------------------
#Sports_Podcast_Cricket

        elif(response_text == 'Cricket Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('The Vaughany and Tuffers Cricket Club', 'Reflecting on an incredible year with Sam Curran')


#-------------------------------------------------------------------------------------------------------------------------------------
#Sports_Podcast_Football

        elif(response_text == 'Football will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('Football Daily', 'The Day After Man Citys Treble Win')



#-------------------------------------------------------------------------------------------------------------------------------------
#Sports_Podcast_Golf

        elif(response_text == 'Golf Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('Beefs Golf Club', 'The First Tee')


#-------------------------------------------------------------------------------------------------------------------------------------
#Music_Podcast_Pop

        elif(response_text == 'Pop Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('Switched on Pop', 'Listening to Draft Punk: Random Access Memories')


#-------------------------------------------------------------------------------------------------------------------------------------
#Music_Podcast_Classic

        elif(response_text == 'Classic Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('That Classic Podcast', 'So long, farewell, auf wiedersehan, goodbye!')


#-------------------------------------------------------------------------------------------------------------------------------------
#Music_Podcast_Jazz

        elif(response_text == 'Jazz Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('The Jazz Session', 'The Jazz Session #617: Bill Lowe')


#-------------------------------------------------------------------------------------------------------------------------------------
#Music_Podcast_Rock

        elif(response_text == 'Rock Podcast will be played soon'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            spotify_podcast_find('Rockonteurs with Gary Kemp and Guy Pratt', 'S4E27: Jerry Shirley')

#-------------------------------------------------------------------------------------------------------------------------------------
#Weather
        elif(response_text == 'Checking the weather right now in London'):
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            get_weather_data()



#-------------------------------------------------------------------------------------------------------------------------------------
#Playing_track

        elif(response_text == 'Sure, can you kindly teach me the title of the music and the name of the artist?'):

            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            # Create OAuth Object
            oauth_object = spotipy.SpotifyOAuth(client_id,client_secret,redirect_uri)

            # Create token
            token_dict = oauth_object.get_cached_token()
            token = token_dict['access_token']

            # Create Spotify Object
            spotifyObject = spotipy.Spotify(auth=token)

            # Create a Spotipy client with user authorization
            scope = 'user-read-playback-state,user-modify-playback-state'
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))


            record_audio()
            try:
                with open('audio.wav', 'rb') as audio:
                    response = speech_to_text.recognize(audio=audio, content_type='audio/wav')
                    track_information = response.result['results'][0]['alternatives'][0]['transcript']
                    #return text
                    track_name = track_information
                    results = sp.search(q=track_name, type='track', limit=1)


            except :
                print("Speech recognition could not understand audio.")

            # Extract the URI of the first track found
            if len(results['tracks']['items']) > 0:
                song_uri = results['tracks']['items'][0]['uri']
                print("Song URI:", song_uri)

                # Play the song
                devices = sp.devices()
                if len(devices['devices']) > 0:
                    device_id = devices['devices'][0]['id']
                    sp.start_playback(device_id=device_id, uris=[song_uri])
                    print("Playing the song...")
                    print(device_id)
                else:
                    print("No active devices found.")
            else:
                print("Song not found.")
            
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

    
            pause_text = "The audio is now paused"
            output_file = "output.wav"
            try:
                # Perform text to speech conversion
                response = text_to_speech.synthesize(pause_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()
                

                # Save the audio to a file
                with open(output_file, 'wb') as audio_file:
                    audio_file.write(response.content)

                print("Text to Speech conversion completed.")
                # Load the audio file
                audio = pydub.AudioSegment.from_wav(output_file)

                # Play the audio
                play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
                play_obj.wait_done()
                
            except Exception as e:
                #print("Error converting text to speech:", str(e))
                pass
#-------------------------------------------------------------------------------------------------------------------------------------
#Calendar
        #elif(response_text == "Calendar"):
        #    lastaudioinput = input_text
        #    break

#-------------------------------------------------------------------------------------------------------------------------------------
#News
        #elif(response_text == "News"):
        #    lastaudioinput = input_text
        #    break


#-------------------------------------------------------------------------------------------------------------------------------------
#Termination

        elif(response_text == "Bye Bye!"):
            # End the session
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()

            assistant.delete_session(draft_environment_id, session_id)
            sys.exit()
#-------------------------------------------------------------------------------------------------------------------------------------
        
        else:
            response_speech = text_to_speech.synthesize(response_text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()

            # Save the audio to a file
            output_file = "output.wav"
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response_speech.content)

            print("Text to Speech conversion completed.")
            # Load the audio file
            audio = pydub.AudioSegment.from_wav(output_file)

            # Play the audio
            play_obj = simpleaudio.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
            play_obj.wait_done()
            #sys.exit()

#-------------------------------------------------------------------------------------------------------------------------------------

watson_assistant()

