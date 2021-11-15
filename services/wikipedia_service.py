import wikipedia
import json

with open("./resources/intents/wikipedia_keywords.json") as f:
    keywords_file = json.load(f)


def take_command_and_return_info(command):
    # print("x")
    keywords = filter_command(command)

    return "Wikipedia launched"


def filter_command(command):
    filtered_command = []

    for word in command:
        if word in keywords_file:
            pass
        else:
            filtered_command.append(word)

    return filtered_command
