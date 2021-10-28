from typing import Any
from google.auth import credentials
import speech_recognition
import json
import os



filename = '/home/pi/Desktop/Scripts/VoiceAssistant/key2.json'


def open_credentials_file(filename):
    with open(filename, "r") as file:
        credentials_file = json.load(file)
    return credentials_file
    

# print(type(json.dumps(credentials_file)))
credentials_file = open_credentials_file(filename=filename)
recognizer = speech_recognition.Recognizer()
speech = speech_recognition.Microphone()

def listen_for_command():
    
    with speech as source:
        print("Tell me, what I'm supposed to do")
        audio = recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        # recog = r.recognize_google(audio, language = 'en-US')
        sentence = recognizer.recognize_google_cloud(audio,json.dumps(credentials_file),language = 'en-US')

        print("You said: " + sentence)
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except speech_recognition.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



 