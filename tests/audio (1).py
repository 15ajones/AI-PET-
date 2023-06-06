import pyaudio
import wave
import speech_recognition as sr

def record_audio():
    # Set the sample rate, channels, and chunk size
    sample_rate = 44100
    chans = 1
    chunk = 1024
    filename = 'audio.wav'
    duration = 3
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


    #return frames, sample_rate

def save_audio_to_file(frames, sample_rate, filename):
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
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the recognizer to perform speech recognition on the audio file
    try:
        with sr.AudioFile('audio.wav') as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Set the duration for audio recording (in seconds)
#recording_duration = 10

# Record audio
#frames, sample_rate = record_audio(recording_duration)
record_audio()

# Save audio to a file
#filename = 'audio.wav'
#save_audio_to_file(frames, sample_rate, filename)

# Convert audio file to text
text = convert_audio_to_text()

# Print the recognized text
print("Recognized Text:")
print(text)
