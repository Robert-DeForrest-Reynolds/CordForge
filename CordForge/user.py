from discord import Member
from .object import Object
from typing import Any


class User(Object):
    account:Member
    id:int
    name:str
    nickname:str


    def __init__(_, account:Member) -> None:
        super().__init__()
        if account:
            _.account = account
            _.id = account.id
            _.name = account.name
            _.nickname = account.nick
            _._immutables.extend(["account", "id", "name"])
            print(_._immutables)
            _._builtins = ["nickname", "add_trait"].append(_._immutables)
        else:
            print("User instantiation not supplied with Member")


    def __setattr__(_, name, value):
        if name in _._immutables:
            raise AttributeError(f"Cannot modify Player.{name}. These are determined by the user's Discord profile,\
                                 and are used by CordForge for various validations, and utilities.")
        super().__setattr__(name, value)
        _.data.update({name:value})


    @staticmethod
    def add_trait(trait_name:str, value:Any) -> None:    
        if not hasattr(User, trait_name):
            print(f"Adding trait {trait_name}")
            setattr(User, trait_name, value)