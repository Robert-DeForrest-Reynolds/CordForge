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
    Cord:Cord
    AutosaveInterval:int
    def __init__(_, Cord:Cord):
        object.__setattr__(_, "Cord", Cord)
        _.AutosaveInterval = 15
        if not exists("Data"):
            mkdir("Data")
        if not exists(PlayersDirectory):
            mkdir(PlayersDirectory)


    def __setattr__(_, Name, Value):
        if Name == "Cord":
            raise AttributeError(f"Cannot modify Data.Cord.")
        
        if isinstance(Value, dict) or Name in ["AutosaveInterval"]:
            super().__setattr__(Name, Value)
        else:
            raise AttributeError(f"Data attributes can only be dictonaries")


    def Initial_Cache(_, User:Member) -> None:
        _.Cord.Players.update({User.id:Player(User)})


    async def Autosave(_) -> None:
        while True:
            await sleep(_.AutosaveInterval)
            print("Autosaving")
            User:Player
            for User in _.Cord.Players.values():
                with open(join(PlayersDirectory, f"{User.ID}.cf"), "w") as File:
                    DataString = ""
                    for Name, Value in User.Data.items():
                        DataString += f"{Name}={Value}\n"
                    DataString = DataString[:-1]
                    File.write(DataString)

            Name:str
            DataDict:dict
            for Name, DataDict in _.__dict__.items():
                if Name not in ["Cord", "AutosaveInterval"]:
                    with open(join("Data", f"{Name}.cf")) as File:
                        DataString = ""
                        for Name, Value in DataDict.items():
                            DataString += f"{Name}={Value}\n"
                        DataString = DataString[:-1]
                        File.write(DataString)


    async def Load_Data(_) -> None:
        print("Loading data")
        for File in listdir(PlayersDirectory):
            ID = int(File[:-3])
            with open(join(PlayersDirectory, File), 'r') as File:
                Contents = [Line.strip() for Line in File.readlines() if Line != ""]
                for Guild in _.Cord.Guilds:
                    Member = Guild.get_member(ID)
                
                if Member:
                    User = Player(Member)
                    _.Cord.Players.update({ID:User})
                    for Line in Contents:
                        Name, Value = Line.split("=")
                        User.__setattr__(Name, Value)
                    print(f"Loaded {Member.name}'s Data")


    async def Reset_User(_, User:Player) -> None:
        PlayerFilePath = join(PlayersDirectory, f"{User.ID}.cf")
        if exists(PlayerFilePath):
            remove(PlayerFilePath)
            print("Reset User")
        else:
            print("Tried to reset a user's file that did not exist.")