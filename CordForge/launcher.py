from sys import exit, executable
from os import remove, getcwd
from os.path import join
from subprocess import  Popen, PIPE, STDOUT
from glob import glob
from sys import argv, stdout

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import logging


class Launcher:
    def __init__(_):
        logging.basicConfig(
            level=logging.INFO,
            stream=stdout,
            format="%(levelname)s:%(name)s:%(message)s"
        )
        _.logger = logging.getLogger("Launcher")
        _.handler = logging.Handler()
        _.handler.emit = _.log_emit
        _.handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logging.getLogger().addHandler(_.handler)

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
            _.logger.info("No key chosen, finding first in Keys file.")
            with open(join(_.working_directory, "keys"), 'r') as keys:
                _.key_selection = keys.readlines()[0].split("=")[0].strip()

        _.python = executable
        _.call_command = [_.python, "-u", "-B", "entry.py", _.key_selection]

        _.construct_window()


    def construct_window(_) -> None:
        _.root = tk.Tk()
        _.root.title("")

        _.root.protocol("WM_DELETE_WINDOW", _.close_window)

        _.frame = tk.Frame(_.root, bg="grey")
        _.frame.pack(fill="both", padx=5, pady=5)

        _.text = ScrolledText(_.frame, bg="#e2e2e2", state="disabled", wrap="word")
        _.text.pack(fill="both", expand=True)

        _.entry = tk.Entry(_.frame, bg="lightgrey")
        _.entry.pack(fill="both", expand=True)
        _.entry.bind("<Return>", _.send_input)
        _.root.mainloop()


    def close_window(_) -> None:
        if _.bot:
            _.logger.warning("Bot is running, killing before closing")
            _.bot.kill()
        _.root.quit()


    def read_stream(_, stream, tag):
        for line in stream:
            _.append_text(f"[{tag}] {line}")

            
    def append_text(_, msg: str):
        raw_message = msg[9:]
        if msg.startswith("[stdout]"): msg = raw_message
        if not msg.endswith("\n"): msg += "\n"

        # schedule the GUI update on the main thread
        _.root.after(0, lambda: _._append_text_safe(msg))


    def _append_text_safe(_, msg: str):
        _.text.configure(state="normal")
        _.text.insert("end", msg)
        _.text.see("end")
        _.text.configure(state="disabled")


    def send_input(_, event):
        user_input = _.entry.get()
        if user_input in _.commands.keys():
            _.append_text(f"Input: {user_input}\n")
            _.commands[user_input]()
        elif _.bot:
            _.bot.stdin.write(user_input + "\n")
            _.bot.stdin.flush()
        _.entry.delete(0, "end")


    def log_emit(_, record):
        try:
            msg = _.handler.format(record)
            _.append_text(msg)
        except Exception:
            _.handler.handleError(record)


    def start(_):
        _.logger.info("Starting Bot...")
        _.bot = Popen(_.call_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1)

        threading.Thread(target=_.read_stream, args=(_.bot.stdout, "stdout"), daemon=True).start()


    def restart(_):
        if _.bot:
            _.logger.info("Restarting Discord bot...")
            _.bot = _.bot.kill()
            _.start()
            _.logger.info("Discord bot restarted")
        else:
            _.logger.warning("There isn't a running bot")


    def exit(_):
        if not _.bot:
            exit()
        else:
            _.logger.warning("There is a running bot")


    def stop(_):
        if _.bot:
            _.logger.info("Discord bot stopped")
            _.bot = _.bot.kill()
        else:
            _.logger.info("There isn't a running bot")


    def emergency_stop(_):
        if not _.bot:
            _.logger.warning("Bot is not running it seems, stopping altogether though.")
            exit()

        if _.bot:
            _.logger.info("Discord bot stopped")
            _.bot = _.bot.kill()
            exit()


    def clear_logs(_):
        for file in glob("Source\\Logs\\*.log"):
            try:
                remove(file)
            except OSError:
                _.logger.warning("Error removing log files for some reason")


if __name__ == "__main__":
    Launcher()