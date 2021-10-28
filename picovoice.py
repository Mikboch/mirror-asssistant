import pvporcupine
import pyaudio
import struct
import os
import time
import playsound
from tempfile import TemporaryFile

from gtts import gTTS
from io import BytesIO

from mpg123 import Mpg123, Out123
from pydub import AudioSegment
from pydub.playback import play

import online_recognizer

# print(pvporcupine.KEYWORDS)


handle = pvporcupine.create(keywords = ['picovoice', 'alexa'])

pa = pyaudio.PyAudio()

audio_stream = pa.open(
                rate=handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=handle.frame_length)

def speak_from_saved_file(text):
    # tts = gTTS(text=text, lang="en")
    filename = "request.mp3"

    # tts.save(filename)
    playsound.playsound(filename)

def speak(text):
    tts = gTTS(text=text, lang="en", tld='ca')
    f = BytesIO()
    tts.write_to_fp(f)
    f.seek(0)


    transcribed_sentence = AudioSegment.from_file(f, format="mp3")
    play(transcribed_sentence)
    

    # mp3 = Mpg123()
    # mp3.feed(f.read())
    # out = Out123()
    
    # for frame in mp3.iter_frames(out.start):
    #     out.play(frame)



speak("Hi I'm your alexa, what can i do for you?")
# speak_from_saved_file("Today happened: - In Sudan, a military coup deposes the government under Prime Minister Abdalla Hamdok. Ahead of Barbados becoming a republic, Sandra Mason (pictured) is elected as the country's first president.")
# onlineRecognizer = online_recognizer.OnlineRecognizer

time.sleep(5)
# main loop
while True:
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        # detection event logic/callback
        print("Hey google")
        speak("To your service!")
        online_recognizer.listen_for_command()

        
       
        


# handle.delete()


# from picovoice import Picovoice
 
# keyword_path = ...
 
# def wake_word_callback():
#     pass
 
# context_path = ...
 
# def inference_callback(inference):
#     # `inference` exposes three immutable fields:
#     # (1) `is_understood`
#     # (2) `intent`
#     # (3) `slots`
#     pass
 
# handle = Picovoice(
#         keyword_path=keyword_path,
#         wake_word_callback=wake_word_callback,
#         context_path=context_path,
#         inference_callback=inference_callback)
        
# while True:
#     handle.process(get_next_audio_frame())
# # handle.delete()