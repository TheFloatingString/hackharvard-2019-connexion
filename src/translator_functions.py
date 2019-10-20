from googletrans import Translator
trans=Translator()
def translate_text(text,src):
    translated_text=trans.translate(text, dest="en", src=src)
    return translated_text.text

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Vrutik/Desktop/api-key.json"
def speech_to_text(lang):
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = "static/audio.wav"
    print(file_name)

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code=lang)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    text=""
    for result in response.results:
        text+=result.alternatives[0].transcript
        print(text)
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
    print("FINAL : ",text)
    return text
