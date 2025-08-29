from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from asyncio import sleep
from os.path import exists, join
from os import mkdir

from discord import Member
from .Player import Player


class Data:
    Cord:Cord
    AutosaveInterval:int
    def __init__(_, Cord:Cord):
        object.__setattr__(_, "Cord", Cord)
        _.AutosaveInterval = 15
        if not exists("Data"):
            mkdir("Data")


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
            Player:Player
            for Player in _.Cord.Players.values():
                with open(join("Data", f"{Player.ID}.cf"), "w") as File:
                    DataString = ""
                    for Name, Value in Player.Data.items():
                        DataString += f"{Name}={Value}"
                    File.write(DataString)

            Name:str
            DataDict:dict
            for Name, DataDict in _.__dict__.items():
                if Name not in ["Cord", "AutosaveInterval"]:
                    with open(join("Data", f"{Name}.cf")) as File:
                        DataString = ""
                        for Name, Value in DataDict.items():
                            DataString += f"{Name}={Value}"
                        File.write(DataString)


    async def Load_Data(_) -> None:
        ...