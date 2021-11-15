import pvporcupine
import pyaudio
import struct
import os
import json
import playsound
from tempfile import TemporaryFile

from gtts import gTTS
from io import BytesIO

from mpg123 import Mpg123, Out123
from pydub import AudioSegment
from pydub.playback import play

import online_recognizer
import intent_manager

# print(pvporcupine.KEYWORDS)
path_to_sounds_folder = "./resources/sound_files/"


def create_mp3_file_from_text(text, file_format):
    tts = gTTS(text=text, lang="en", tld="ca")
    tts.save(path_to_sounds_folder + text + file_format)


def speak_from_saved_file(name_of_file):
    filename = path_to_sounds_folder + name_of_file
    playsound.playsound(filename)


def speak(text):
    tts = gTTS(text=text, lang="en", tld="ca")
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


# przetestowac czy ktoras z tych 3 linii nie produkuje false positivow -> przesunac ponizej speak()
handle = pvporcupine.create(keywords=["picovoice", "alexa"])
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=handle.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=handle.frame_length,
)

speak_from_saved_file("notification_ambient.wav")
# speak_from_saved_file("starting_voice.mp3")

# create_mp3_file_from_text("Hi I'm your alexa, what can i do for you?","mp3")
# speak_from_saved_file("Today happened: - In Sudan, a military coup deposes the government under Prime Minister Abdalla Hamdok. Ahead of Barbados becoming a republic, Sandra Mason (pictured) is elected as the country's first president.")
# onlineRecognizer = online_recognizer.OnlineRecognizer
# time.sleep(5)

command = "What is the "

sentence = intent_manager.process_command(command)
print(sentence)


# main loop
# while True:
#     pcm = audio_stream.read(handle.frame_length)
#     pcm = struct.unpack_from("h" * handle.frame_length, pcm)

#     keyword_index = handle.process(pcm)
#     if keyword_index >= 0:
#         # detection event logic/callback
#         print("Hey google")
#         speak("To your service!")
#         speak_from_saved_file("state-change_confirm-down.wav")

#         command = online_recognizer.listen_for_command()

#         sentence = intent_manager.process_command(command)
#         speak(sentence)


# handle.delete()       <-this might be useful for echo effect
