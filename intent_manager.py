#  "keywords": "what, what's, time, day, weather, what, in, today, tell, me, look, play, on, youtube, spotify, add, at, am., pm."
import sys

sys.path.append("modules/MMM-VoiceAssistant/services")
import date_time_service
import wikipedia_service
import json


path_to_intents = "modules/MMM-VoiceAssistant/resources/intents/"

with open(path_to_intents + "intents.json") as f:
    intents_base = json.load(f)
    intents = intents_base


def launch_appropriate_service(service_name, command):
    if service_name == "date_time_service":
        data = date_time_service.take_command_and_return_info(command)
        return data
    elif service_name == "wikipedia_service":
        data = wikipedia_service.take_command_and_return_info(command)
        return data
    # elif service_name=="":
    # elif service_name=="":


def process_command(command):
    command = command + "#"
    command = command.lower()
    formatted = command.split(" ")

    # print("after trasformation: " + command)
    for word in formatted:
        global intents
        print("entered through: " + word)

        try:
            if word == "#":
                intents = intents["#"]
                break

            if intents[word] == "-":
                intents = intents["-"]
                break

            # print("blob")
            # if intents[word] == None:
            #     print("nic")
            #     break
            intents = intents[word]
        except:
            try:
                intents = intents["*"]
                break
            except:
                return "I don't know how to respond to that"

    print("intents before service: ")
    # print(intents)
    # print(formatted)
    return launch_appropriate_service(intents, formatted)
