#  "keywords": "what, what's, time, day, weather, what, in, today, tell, me, look, play, on, youtube, spotify, add, at, am., pm."
import sys

sys.path.append("./services")
import date_time_service
import wikipedia_service
import json


path_to_intents = "./resources/intents/"

with open(path_to_intents + "intents.json") as f:
    intents_base = json.load(f)
    intents = intents_base
    print(intents)


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
    l = command.split(" ")

    print("after trasformation: " + command)
    for word in l:
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
                if "*" in intents:
                    intents = intents["*"]
            except:
                return "I don't know how to respond to that"

    print("intents before service: ")
    print(intents)
    print(l)
    return launch_appropriate_service(intents, l)
