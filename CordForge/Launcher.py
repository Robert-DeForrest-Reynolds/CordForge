from sys import exit
from os import remove, getcwd
from os.path import join
from subprocess import *
from glob import glob
from sys import argv
from pathlib import Path


class Launcher:
    def __init__(_):
        _.Key = None
        _.Commands = {"start": _.Start,
                                  "restart": _.Restart,
                                  "exit": _.Exit,
                                  "stop": _.Stop,
                                  "//": _.Emergency_Stop,
                                  "clear logs": _.Clear_Logs}
        _.WorkingDirectory = getcwd()
        if len(argv) == 2:
            _.KeySelection = argv[1]
        else:
            print("No key chosen, finding first in Keys file.")
            _.KeySelection = Path(join(_.WorkingDirectory, "Keys")).read_text().split("\n")[0].split("=")[0]
        _.Settings = Path(join(_.WorkingDirectory, "Settings")).read_text().split("\n")
        _.VirtualEnvironmentPath = Path(_.Settings[0].split("=")[1])
        _.EntryPath = Path(_.Settings[1].split("=")[1])
        _.CallCommand = f"{_.VirtualEnvironmentPath} -B {_.EntryPath} {_.KeySelection}"
        
        _.User_Input()


    def User_Input(_):
        while True:
            admin_input = input()
            print("Input command: ", admin_input)
            try:
                _.Commands[admin_input.lower()]()
            except KeyError:
                print("Invalid command.")
    

    def BotExists(_):
        try:
            Bot
        except NameError:
            return False
        else:
            return True


    def Start(_):
        global Bot
        print("Starting Cord")
        Bot = Popen(_.CallCommand)


    def Restart(_):
        global Bot
        if _.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            Bot = Popen(_.CallCommand)
            print("Discord bot restarted")
        else:
            print("There isn't a running bot")

    def Exit(_):
        global Bot
        if _.BotExists() == False:
            exit()
        else:
            print("There is a running bot")


    def Stop(_):
        global Bot
        if _.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
        else:
            print("There isn't a running bot")


    def Emergency_Stop(_):
        global Bot
        if _.BotExists() == False:
            print("Bot is not running it seems, stopping altogether though.")
            exit()

        if _.BotExists():
            print("Discord bot stopped")
            Bot.kill()
            del Bot
            exit()


    def Clear_Logs(_):
        for File in glob("Source\\Logs\\*.log"):
            try:
                remove(File)
            except OSError:
                print("Error removing log files for some reason")