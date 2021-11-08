import time
import datetime 
import requests
import json


with open('/home/pi/Desktop/Scripts/VoiceAssistant/resources/api_keys.json') as f1:
    api_keys_file = json.load(f1)
    ip_geolocation_key = api_keys_file["ip_geolocation_key"]

with open('/home/pi/Desktop/Scripts/VoiceAssistant/resources/intents/date_time_keywords.json') as f2:
    keywords_file = json.load(f2)
        

"What time is it in Warsaw"

def take_command(command):
    if "time" in command and "in" in command:
        distinct_words = filter_command(command)
        city = distinct_words[0]
        country = distinct_words[1]
        time = get_time_in_city(city)#,distinct_words[1])

        return "In " +city+ " it is " + time
    elif "time" in command:
        return datetime.datetime.now()
    elif "":  
        pass  


def filter_command(command):
    filtered_command = []

    for word in command:
        if word in keywords_file:
            pass
        else:
            filtered_command.append(word)

    return filtered_command


def get_time_in_city(city):
    request = 'https://api.ipgeolocation.io/timezone?apiKey='+ip_geolocation_key+'&location=' + city
    response = requests.get(request)
    
    if(response.status_code == 200):
        return response.json("date_time_txt")
