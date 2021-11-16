from ctypes import sizeof
from requests.api import options
import wikipedia
import json

from wikipedia.exceptions import DisambiguationError, PageError

with open("./resources/intents/wikipedia_keywords.json") as f:
    keywords_file = json.load(f)


def take_command_and_return_info(command):
    # print("x")
    keywords = filter_command(command)
    query = " ".join(keywords)
    information = find_information_about(query)

    return information


def filter_command(command):
    filtered_command = []

    for word in command:

        if word in keywords_file:
            for i in range(command.index(word) + 1, len(command) - 1):
                filtered_command.append(command[i])
                # print(command[i])
            break

    return filtered_command


# https://wikipedia.readthedocs.io/en/latest/code.html#module-wikipedia.exceptions  <- list of all wiki exceptions


def find_information_about(phrase):
    print("Phrase: " + phrase)
    try:
        query = wikipedia.search(phrase)

        if query:
            information = wikipedia.summary(
                query[0], sentences=1, auto_suggest=False, redirect=True
            )
            return "Here's what I found about: " + phrase + ". " + information
        else:
            return "Sorry I couldn't find any info about " + phrase
    except DisambiguationError as e:
        # API wasn't sure which result is the best; returning top 3
        max_number_of_results = min(len(e.options), 3)

        response = "Here are top three matching results for term: " + phrase + ". "

        for i in range(max_number_of_results):
            response += e.options[i] + ", "

        return response
    except PageError:
        return (
            "Sorry. The phrase is not precise enough. Could you put it in other words?"
        )
    except:
        return "Sorry, I can't respond to that, there is something wrong with my whistle-blower."
