import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import wave

# Set up the Speech to Text service
apikey = 'vIC0cr98ZS3tO7FxgceuzsjCrhDUjiMc2IbSEtSdEzjv'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/cbab904d-34fb-41dc-a0fd-40cca19ff9e6'
authenticator = IAMAuthenticator(apikey)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

def record_audio():
    # Set the sample rate, channels, and chunk size
    sample_rate = 44100
    channels = 1
    chunk = 1024
    filename = 'audio.wav'
    duration = 10

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

def convert_audio_to_text():

    try:
        with open('audio.wav', 'rb') as audio:
            response = speech_to_text.recognize(audio=audio, content_type='audio/wav')
            text = response.result['results'][0]['alternatives'][0]['transcript']
            return text
    except :
        print("Speech recognition could not understand audio.")


#record_audio()
#text = convert_audio_to_text()
# Print the recognized text
#print("Recognized Text:")
#print(text)
