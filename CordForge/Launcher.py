from sys import exit
from os import remove, getcwd
from os.path import join
from subprocess import *
from glob import glob
from sys import argv
from pathlib import Path


class Launcher:
    def __init__(_):
        _.key = None
        _.commands = {"start": _.start,
                      "restart": _.restart,
                      "exit": _.exit,
                      "stop": _.stop,
                      "//": _.emergency_stop,
                      "clear logs": _.clear_logs}
        _.working_directory = getcwd()
        if len(argv) == 2:
            _.key_selection = argv[1]
        else:
            print("No key chosen, finding first in Keys file.")
            _.key_selection = Path(join(_.working_directory, "keys")).read_text().split("\n")[0].split("=")[0]
        _.settings = Path(join(_.working_directory, "settings")).read_text().split("\n")
        _.virtual_environment_path = Path(_.settings[0].split("=")[1])
        _.entry_path = Path(_.settings[1].split("=")[1])
        _.call_command = f"{_.virtual_environment_path} -B {_.entry_path} {_.key_selection}"
        
        _.user_input()


    def user_input(_):
        while True:
            admin_input = input()
            print("Input command: ", admin_input)
            try:
                _.commands[admin_input.lower()]()
            except KeyError:
                print("Invalid command.")
    

    def bot_exists(_):
        try:
            Bot
        except NameError:
            return False
        else:
            return True


    def start(_):
        global Bot
        print("Starting Cord")
        Bot = Popen(_.call_command)


    def restart(_):
        global Bot
        if _.bot_exists():
            print("Restarting Discord bot")
            Bot.kill()
            _.start()
            print("Discord bot restarted")
        else:
            print("There isn't a running bot")

    def exit(_):
        global Bot
        if _.bot_exists() == False:
            exit()
        else:
            print("There is a running bot")


    def stop(_):
        global Bot
        if _.bot_exists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
        else:
            print("There isn't a running bot")


    def emergency_stop(_):
        global Bot
        if _.bot_exists() == False:
            print("Bot is not running it seems, stopping altogether though.")
            exit()

        if _.bot_exists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
            exit()


    def clear_logs(_):
        for file in glob("Source\\Logs\\*.log"):
            try:
                remove(file)
            except OSError:
                print("Error removing log files for some reason")