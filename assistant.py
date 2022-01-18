import pvporcupine
import pyaudio
import struct
import json
import playsound
from tempfile import TemporaryFile
import time
import sys


from gtts import gTTS
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

import online_recognizer
import intent_manager

# print(pvporcupine.KEYWORDS)
path_to_sounds_folder = "modules/MMM-VoiceAssistant/resources/sound_files/"


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

speak_from_saved_file("boot_sound.wav")
# speak_from_saved_file("starting_voice.mp3")


def send_to_node(status, assistant_response):
    try:
        if assistant_response != "":
            data = {"status": status, "assistant_response": assistant_response}
        else:
            data = {"status": status}

        print(json.dumps(data))
    except Exception:
        print("Error while trying to send message to node")
    sys.stdout.flush()


# main loop
while True:
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        # detection event logic/callback
        send_to_node("ASSISTANT_ACTIVATED", "")
        print("Hey google")
        speak("To your service!")
        speak_from_saved_file("state-change_confirm-down.wav")

        command = online_recognizer.listen_for_command()

        sentence = intent_manager.process_command(command)
        if sentence != None:
            send_to_node("COMMAND_SENT", sentence)
            speak(sentence)
            time.sleep(5)
        else:
            speak("Please try again")

        send_to_node("ASSISTANT_DEACTIVATED", "")


# handle.delete()       <-this might be useful for echo effect
