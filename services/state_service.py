import json
import os


def execute_command(command):
    if command[0] == "stop":
        os.system("sudo shutdown now")
    elif command[0] == "restart":
        if command[1] == "#":
            os.system("sudo reboot now")
        else:
            os.system("pm2 restart mm")
