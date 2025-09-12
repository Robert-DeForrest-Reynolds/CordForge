from discord import Member


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


    def __setattr__(_, name, value):
        if name in ["account", "id"]:
            raise AttributeError(f"Cannot modify Player.{name}. These are determined by the user's Discord profile,\
                                 and are used by CordForge for various validations, and utilities.")
        super().__setattr__(name, value)
        if name not in  ["name", "nickname", "data"]:
            _.data.update({name:value})