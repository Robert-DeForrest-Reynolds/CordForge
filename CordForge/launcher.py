import asyncio
import curses
from sys import exit, platform, argv
from os import remove, getcwd
from os.path import join
from pathlib import Path
from glob import glob


class Launcher:
    def __init__(_):
        _.bot = None
        _.commands = {
            "start": _.start,
            "restart": _.restart,
            "exit": _.exit_launcher,
            "stop": _.stop,
            "//": _.emergency_stop,
            "clear logs": _.clear_logs,
        }

        _.working_directory = getcwd()
        if len(argv) == 2:
            _.key_selection = argv[1]
        else:
            print("No key chosen, finding first in Keys file.")
            _.key_selection = Path(join(_.working_directory, "keys")).read_text().split("\n")[0].split("=")[0]

        _.settings = Path(join(_.working_directory, "settings")).read_text().split("\n")
        _.virtual_environment_path = Path(_.settings[0].split("=")[1])
        _.entry_path = Path(_.settings[1].split("=")[1])

        if platform.startswith("win"):
            _.call_command = [_.virtual_environment_path, "-B", _.entry_path, _.key_selection]
        elif platform.startswith("linux"):
            _.call_command = [_.virtual_environment_path, "-B", _.entry_path, _.key_selection]

        
        curses.wrapper(lambda stdscr: asyncio.run(_.curses_main(stdscr)))


    def log(_, message: str):
        _.output_lines.append(message.rstrip())
        if len(_.output_lines) > _.output_height - 1:
            _.output_lines.pop(0)


    async def curses_main(_, stdscr):
        try:
            curses.curs_set(1)
            stdscr.clear()
            stdscr.refresh()

            _.output_height = curses.LINES - 2
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
                        _.log(f"> {command}")
                        _.handle_command(command)
                        user_input = ""
                    elif key in (curses.KEY_BACKSPACE, 127):
                        user_input = user_input[:-1]
                    elif 32 <= key < 127:
                        user_input += chr(key)

                await asyncio.sleep(0.05)

        except asyncio.CancelledError:
            # Task was cancelled — exit gracefully
            return


    def handle_command(_, cmd: str):
        if not cmd:
            return
        try:
            asyncio.create_task(_.commands[cmd.lower()]())
        except KeyError:
            _.log("Invalid command.")


    def bot_exists(_):
        return _.bot is not None
    

    def kill_bot(_):
        try:
            _.bot.kill()
        except ProcessLookupError as e: pass
        _.bot = None



    async def start(_):
        _.log("Starting Bot...")
        _.bot = await asyncio.create_subprocess_exec(
            *_.call_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        asyncio.create_task(_.read_stream(_.bot.stdout))
        asyncio.create_task(_.read_stream(_.bot.stderr))


    async def read_stream(_, stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            _.log(line.decode(errors="ignore"))


    async def restart(_):
        if _.bot_exists():
            _.log("Restarting Discord bot...")
            _.kill_bot()
            await _.start()
            _.log("Discord bot restarted")
        else:
            _.log("There isn't a running bot")


    async def exit_launcher(_):
        if _.bot_exists() is False:
            curses.endwin()
            try:
                loop = asyncio.get_running_loop()
                tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
                for t in tasks:
                    t.cancel()
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                loop.stop()
                loop.close()
            except RuntimeError:
                pass  # no loop running
        else:
            _.log("There is a running bot")


    async def stop(_):
        if _.bot_exists():
            _.log("Discord bot stopped")
            _.kill_bot()
        else:
            _.log("There isn't a running bot")


    async def emergency_stop(_):
        if _.bot_exists():
            _.kill_bot()
        await _.exit_launcher()


    async def clear_logs(_):
        for file in glob("Source\\Logs\\*.log"):
            try:
                remove(file)
                _.log(f"Removed log: {file}")
            except OSError:
                _.log("Error removing log files.")
