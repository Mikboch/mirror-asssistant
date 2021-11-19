import re
import time
import datetime
import requests
import json

# from datetime import datetime, date
import calendar

with open("/home/pi/Desktop/Scripts/VoiceAssistant/resources/api_keys.json") as f1:
    api_keys_file = json.load(f1)
    ip_geolocation_key = api_keys_file["ip_geolocation_key"]

with open(
    "/home/pi/Desktop/Scripts/VoiceAssistant/resources/intents/date_time_keywords.json"
) as f2:
    keywords_file = json.load(f2)


def take_command_and_return_info(command):
    print("Command taken, entering function")

    if "time" in command and "in" in command:
        distinct_words = filter_command(command)
        print(distinct_words)
        city = ""

        if len(distinct_words) > 0:
            str = " ".join(distinct_words)
            city += str

        time = get_time_in_city(city)

        if time is not None:
            return "In " + city + " it is " + time
        else:
            return "Sorry I couln't find info about time in " + city
    elif "time" in command:
        now = datetime.datetime.now()
        time = str(now.strftime("%I:%M %p"))
        print("Time")
        return "It's currently " + time
    elif "day" in command and "is" in command:
        distinct_words = filter_command(command)
        day = get_day_of_week(distinct_words)

        return day
    elif "date" in command:
        distinct_words = filter_command(command)
        date = get_date()

        return date


def filter_command(command):
    filtered_command = []

    for word in command:
        if word in keywords_file:
            pass
        else:
            filtered_command.append(word)

    return filtered_command


def get_time_in_city(city):
    request = (
        "https://api.ipgeolocation.io/timezone?apiKey="
        + ip_geolocation_key
        + "&location="
        + city
    )
    response = requests.get(request)

    if response.status_code == 200:
        date_unprocessed = response.json()["date_time_txt"]
        day = date_unprocessed.split(",")[0]

        hours_unprocessed = response.json()["time_12"]
        str1 = hours_unprocessed[:-6]
        str2 = hours_unprocessed[-3:]
        hours = str1 + str2

        return day + ", " + hours


def get_date():
    current_date = datetime.date.today()
    day_of_week = current_date.strftime("%A")
    date = current_date.strftime("%B %d %Y")

    return "It's " + day_of_week + ", " + date


def get_day_of_week(when):
    WEEK_DAYS = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    if "today" in when or not when:
        day_index = int(datetime.date.today().strftime("%w"))
        return "Today is " + WEEK_DAYS[day_index]
    elif "tomorrow" in when:
        day_index = int(datetime.date.today().strftime("%w")) + 1
        return "Tomorrow is " + WEEK_DAYS[day_index]
