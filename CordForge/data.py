from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from .cord import Cord

from asyncio import sleep
from os.path import exists, join
from os import mkdir, listdir, remove

from discord import Member
from .user import User
from .object import Object

users_directory = join("data", "users")

class Data:
    cord:Cord
    autosave_interval:int
    def __init__(_, cord:Cord):
        object.__setattr__(_, "cord", cord)
        _.autosave_interval = 15
        if not exists("data"):
            mkdir("data")
        if not exists(users_directory):
            mkdir(users_directory)


    def __setattr__(_, name, value):
        if name == "cord":
            raise AttributeError(f"Cannot modify Data.cord.")
        
        if isinstance(value, dict) or name in ["autosave_interval"]:
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Data attributes can only be dictonaries")


    async def autosave(_) -> None:
        print("Starting autosave loop...")
        while True:
            await sleep(_.autosave_interval)
            print("Autosaving...")
            user:User
            for user in _.cord.user_profiles.values():
                with open(join(users_directory, f"{user.id}.cf"), "w") as file:
                    data_string = ""
                    for name, value in user.data.items():
                        data_string += f"{name}={value}\n"
                    data_string = data_string[:-1]
                    file.write(data_string)

            name:str
            object:Object
            with open(join("data", f"objects.cf"), "w") as file:
                for object_name, object in _.cord.objects.items():
                    data_string = ""
                    data_string += f"{object_name}:"
                    for name, value in object.data.items():
                        data_string += f"{name}={value}~"
                    data_string = data_string[:-1] + "\n"
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
            print("Finished autosaving")


    async def load_data(_) -> None:
        print("Loading data...")
        for file in listdir(users_directory):
            print(file)
            id = int(file[:-3])
            with open(join(users_directory, file), 'r') as file:
                contents = [line.strip() for line in file.readlines() if line != ""]
                for guild in _.cord.guilds:
                    member = guild.get_member(id)

                if member:
                    user = User(member)
                    _.cord.user_profiles.update({id:user})
                    for line in contents:
                        name, value = line.split("=")
                        if value.replace(".", "").isdecimal():
                            value = float(value)
                        elif value.isdecimal():
                            value = int(value)
                        user.__setattr__(name, value)
                    print(f"Loaded {member.name}'s Data")
        print("All data loaded")


    async def reset_user(_, user:User) -> None:
        user_file_path = join(users_directory, f"{user.id}.cf")
        if exists(user_file_path):
            remove(user_file_path)
            print("Reset User")
        else:
            print("Tried to reset a user's file that did not exist.")