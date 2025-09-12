from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from asyncio import sleep
from os.path import exists, join
from os import mkdir, listdir, remove

from discord import Member
from .Player import Player

PlayersDirectory = join("Data", "Players")

class Data:
    cord:Cord
    autosave_interval:int
    def __init__(_, cord:Cord):
        object.__setattr__(_, "cord", cord)
        _.autosave_interval = 15
        if not exists("Data"):
            mkdir("Data")
        if not exists(PlayersDirectory):
            mkdir(PlayersDirectory)


    def __setattr__(_, name, value):
        if name == "cord":
            raise AttributeError(f"Cannot modify Data.cord.")
        
        if isinstance(value, dict) or name in ["autosave_interval"]:
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Data attributes can only be dictonaries")


    def initial_cache(_, user:Member) -> None:
        _.cord.players.update({user.id:Player(user)})


    async def autosave(_) -> None:
        while True:
            await sleep(_.autosave_interval)
            print("Autosaving")
            user:Player
            for user in _.cord.players.values():
                with open(join(PlayersDirectory, f"{user.id}.cf"), "w") as file:
                    data_string = ""
                    for name, value in user.data.items():
                        data_string += f"{name}={value}\n"
                    data_string = data_string[:-1]
                    file.write(data_string)

            name:str
            data_dict:dict
            for name, data_dict in _.__dict__.items():
                if name not in ["cord", "autosave_interval"]:
                    with open(join("Data", f"{name}.cf")) as file:
                        data_string = ""
                        for name, value in data_dict.items():
                            data_string += f"{name}={value}\n"
                        data_string = data_string[:-1]
                        file.write(data_string)


    async def load_data(_) -> None:
        print("Loading data")
        for file in listdir(PlayersDirectory):
            id = int(file[:-3])
            with open(join(PlayersDirectory, file), 'r') as file:
                contents = [line.strip() for line in file.readlines() if line != ""]
                for guild in _.cord.guilds:
                    member = guild.get_member(id)
                
                if member:
                    user = Player(member)
                    _.cord.players.update({id:user})
                    for line in contents:
                        name, value = line.split("=")
                        user.__setattr__(name, value)
                    print(f"Loaded {member.name}'s Data")


    async def reset_user(_, user:Player) -> None:
        player_file_path = join(PlayersDirectory, f"{user.id}.cf")
        if exists(player_file_path):
            remove(player_file_path)
            print("Reset User")
        else:
            print("Tried to reset a user's file that did not exist.")