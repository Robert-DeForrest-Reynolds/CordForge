from discord import Member


class Player:
    Account:Member
    Name:str
    Nickname:str
    ID:int

    def __init__(_, Account:Member) -> None:
        object.__setattr__(_, "Account", Account)
        object.__setattr__(_, "ID", Account.id)
        _.Name = Account.name
        _.Nickname = Account.nick
        _.Data = {}


    def __setattr__(_, Name, Value):
        if Name in ["Account", "ID"]:
            raise AttributeError(f"Cannot modify Player.{Name}. These are determined by the user's Discord profile,\
                                 and are used by CordForge for various validations, and utilities.")
        super().__setattr__(Name, Value)
        if Name not in  ["Name", "Nickname", "Data"]:
            _.Data.update({Name:Value})