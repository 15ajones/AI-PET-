import requests
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import wave
import pydub
import simpleaudio

# Set up the Text to Speech service
apikey = 'RL8bEBwfNsNhJ8uzZWGVWIWKZi_sIe2eptFqcGdytYXH'
url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/5da2b1e5-0bde-4a8c-bd7a-ebb249bb968b'
authenticator = IAMAuthenticator(apikey)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url)

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

get_weather_data()
