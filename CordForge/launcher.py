from sys import exit, executable
from os import remove, getcwd
from os.path import join
from subprocess import  Popen, PIPE, STDOUT
from asyncio import run, sleep, CancelledError
from glob import glob
from sys import argv, stdout

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import logging


class Launcher:
    def __init__(_):
        _.headless = False
        
        _.logger = logging.getLogger("Launcher")
        _.logger.setLevel(logging.INFO)
        _.logger.propagate = False  # don’t bubble up to root

        # Attach your custom handler
        _.handler = logging.Handler()
        _.handler.emit = _.log_emit
        _.handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        _.logger.addHandler(_.handler)

        _.bot = None
        _.key = None
        _.working_directory = getcwd()
        _.commands = {"start": _.start,
                      "restart": _.restart,
                      "exit": _.exit,
                      "stop": _.stop,
                      "//": _.emergency_stop,
                      "clear logs": _.clear_logs}
        _.toggle = True
        
        if len(argv) >= 2:
            _.key_selection = argv[1]
            if len(argv) == 3:
                if argv[2] == 'h': _.headless = True
        else:
            _.logger.info("No key chosen, finding first in Keys file.")
            with open(join(_.working_directory, "keys"), 'r') as keys:
                _.key_selection = keys.readlines()[0].split("=")[0].strip()

        _.python = executable
        _.call_command = [_.python, "-u", "-B", "entry.py", _.key_selection]

        if _.headless:
            from curses import wrapper
            wrapper(lambda stdscr: run(_.curses_main(stdscr)))
        else:
            _.construct_window()


    def construct_window(_) -> None:
        _.root = tk.Tk()
        _.root.title("")

        _.root.protocol("WM_DELETE_WINDOW", _.close_window)

        _.frame = tk.Frame(_.root, bg="grey")
        _.frame.pack(fill="both", padx=5, pady=5)

        _.text = ScrolledText(_.frame, bg="#e2e2e2", state="disabled", wrap="word")
        _.text.tag_config("first", background="#858585")
        _.text.tag_config("second", background="#A8A8A8")
        _.text.pack(fill="both", expand=True)

        _.entry = tk.Entry(_.frame, bg="lightgrey")
        _.entry.pack(fill="both", expand=True)
        _.entry.bind("<Return>", _.send_input)
        _.root.mainloop()


    def send_input(_, event):
        user_input = _.entry.get()
        if user_input in _.commands.keys():
            _.append_text(f">{user_input}\n")
            _.commands[user_input]()
        elif _.bot:
            _.bot.stdin.write(user_input + "\n")
            _.bot.stdin.flush()
        _.entry.delete(0, "end")


    def close_window(_) -> None:
        if _.bot:
            _.logger.warning("Bot is running, killing before closing")
            _.bot.kill()
        _.root.quit()


    def curses_log(_, message: str):
        from curses import error
        lines = message.rstrip().split("\n")
        _.output_lines.extend(lines)
        if len(_.output_lines) > _.output_height - 1:
            _.output_lines = _.output_lines[-(_.output_height-1):]
        if hasattr(_, "output_win"):
            _.output_win.erase()
            for idx, line in enumerate(_.output_lines):
                try:
                    _.output_win.addstr(idx, 0, line[:_.output_win.getmaxyx()[1]-1])
                except error:
                    pass
            _.output_win.refresh()


    async def curses_main(_, stdscr):
        import curses
        try:
            curses.curs_set(1)
            stdscr.clear()
            stdscr.refresh()

            _.output_height = curses.LINES - 1
            _.output_win = curses.newwin(_.output_height, curses.COLS, 0, 0)
            _.input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)

            _.output_lines = []
            user_input = ""

            while True:
                _.output_win.erase()
                for idx, line in enumerate(_.output_lines):
                    _.output_win.addstr(idx, 0, line[:curses.COLS - 1])
                _.output_win.refresh()

                _.input_win.erase()
                _.input_win.addstr(0, 0, "~" + user_input)
                _.input_win.clrtoeol()
                _.input_win.refresh()

                # Non-blocking input
                _.input_win.nodelay(True)
                try:
                    key = _.input_win.getch()
                except curses.error:
                    key = -1

                if key != -1:
                    if key in (curses.KEY_ENTER, 10, 13):
                        command = user_input.strip()
                        if command in _.commands.keys():
                            _.curses_log(f"{command}\n")
                            _.commands[command]()
                        user_input = ""
                    elif key in (curses.KEY_BACKSPACE, 127):
                        user_input = user_input[:-1]
                    elif 32 <= key < 127:
                        user_input += chr(key)

                await sleep(0.05)

        except CancelledError:
            # Task was cancelled — exit gracefully
            return


    def read_stream(_, stream, tag):
        for line in stream:
            if _.headless:
                _.curses_log(f"[{tag}] {line}")
            else:
                _.append_text(f"[{tag}] {line}")

            
    def append_text(_, msg: str):
        tag = "first" if _.toggle else "second"
        _.toggle = not _.toggle
        raw_message = msg[9:]
        if msg.startswith("[stdout]"): msg = raw_message
        if not msg.endswith("\n"): msg += "\n"

        _.root.after(0, lambda: _._append_text_safe(msg, tag))


    def _append_text_safe(_, msg: str, tag:str):
        _.text.configure(state="normal")
        _.text.insert("end", msg, tag)
        _.text.see("end")
        _.text.configure(state="disabled")


    def log_emit(_, record):
        try:
            msg = _.handler.format(record)
            if _.headless:
                _.curses_log(msg)
            else:
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