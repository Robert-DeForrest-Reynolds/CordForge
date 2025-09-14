from discord import Member
from typing import Any


class Player:
    account:Member
    name:str
    nickname:str
    id:int

    def __init__(_, account:Member) -> None:
        object.__setattr__(_, "account", account)
        object.__setattr__(_, "id", account.id)
        _.name = account.name
        _.nickname = account.nick
        _.data = {}

        for key, value in Player.__dict__.items():
            if not key.startswith("__") and key not in ["account", "id", "name", "nickname", "data", "add_player_trait"]:
                _.data[key] = value


    def __setattr__(_, name, value):
        if name in ["account", "id"]:
            raise AttributeError(f"Cannot modify Player.{name}. These are determined by the user's Discord profile,\
                                 and are used by CordForge for various validations, and utilities.")
        super().__setattr__(name, value)
        if name not in  ["name", "nickname", "data"]:
            print(name)
            _.data.update({name:value})


    @staticmethod
    def add_player_trait(trait_name:str, value:Any) -> None:    
        if not hasattr(Player, trait_name):
            print(f"Adding trait {trait_name}")
            setattr(Player, trait_name, value)