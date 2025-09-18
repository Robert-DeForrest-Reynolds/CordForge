from sys import exit, platform, executable
from os import remove, getcwd
from os.path import join
from subprocess import  Popen, PIPE
from glob import glob
from sys import argv
from asyncio import run as async_run

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class Launcher:
    def __init__(_):
        _.bot = None
        _.key = None
        _.working_directory = getcwd()
        _.commands = {"start": _.start,
                      "restart": _.restart,
                      "exit": _.exit,
                      "stop": _.stop,
                      "//": _.emergency_stop,
                      "clear logs": _.clear_logs}
        
        if len(argv) == 2:
            _.key_selection = argv[1]
        else:
            print("No key chosen, finding first in Keys file.")
            with open(join(_.working_directory, "keys"), 'r') as keys:
                _.key_selection = keys.readlines()[0].split("=")[0].strip()

        _.python = executable
        _.call_command = [_.python, "-B", "entry.py", _.key_selection]

        _.construct_window()


    def construct_window(_) -> None:
        _.root = tk.Tk()
        _.root.title(f"{_.working_directory}")

        _.root.protocol("WM_DELETE_WINDOW", _.close_window)

        _.frame = tk.Frame(_.root, bg="grey")
        _.frame.pack(fill="both", padx=5, pady=5)

        # Output area
        _.text = ScrolledText(_.frame, bg="grey", state="disabled", wrap="word")
        _.text.pack(fill="both", expand=True)

        # Input field
        _.entry = tk.Entry(_.frame, bg="lightgrey")
        _.entry.pack(fill="both", expand=True)
        _.entry.bind("<Return>", _.send_input)
        _.root.mainloop()


    def close_window(_) -> None:
        if _.bot:
            print("Bot is running, killing before closing")
            _.bot.kill()
        _.root.quit()


    def read_stream(_, stream, tag):
        for line in stream:
            _.append_text(f"[{tag}] {line}")


    def append_text(_, msg:str):
        raw_message = msg[9:]
        if msg.startswith("[stdout]"): msg = raw_message
        elif msg.startswith("[stderr]"): msg = "Error:" + raw_message
        
        if not msg.endswith("\n"): msg += "\n"

        _.text.configure(state="normal")
        _.text.insert("end", msg)
        _.text.see("end")
        _.text.configure(state="disabled")


    def send_input(_, event):
        user_input = _.entry.get()
        _.append_text(f"Input: {user_input}\n")
        if user_input in _.commands.keys():
            _.commands[user_input]()
        _.entry.delete(0, "end")


    def start(_):
        _.append_text("\n\nStarting Bot...")
        _.bot = Popen(_.call_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True, bufsize=1)

        threading.Thread(target=_.read_stream, args=(_.bot.stdout, "stdout"), daemon=True).start()
        threading.Thread(target=_.read_stream, args=(_.bot.stderr, "stderr"), daemon=True).start()


    def restart(_):
        if _.bot:
            _.append_text("Restarting Discord bot...")
            _.bot = _.bot.kill()
            _.start()
            _.append_text("Discord bot restarted")
        else:
            _.append_text("There isn't a running bot")


    def exit(_):
        if not _.bot:
            exit()
        else:
            _.append_text("There is a running bot")


    def stop(_):
        if _.bot:
            _.append_text("Discord bot stopped")
            _.bot = _.bot.kill()
        else:
            print("There isn't a running bot")


    def emergency_stop(_):
        if not _.bot:
            _.append_text("Bot is not running it seems, stopping altogether though.")
            exit()

        if _.bot:
            _.append_text("Discord bot stopped")
            _.bot = _.bot.kill()
            exit()


    def clear_logs(_):
        for file in glob("Source\\Logs\\*.log"):
            try:
                remove(file)
            except OSError:
                print("Error removing log files for some reason")


if __name__ == "__main__":
    Launcher()