from discord import Member


class Player:
    Account:Member
    Name:str
    Nickname:str
    ID:int

    def __init__(_, Account:Member) -> None:
        _.Account = Account
        _.Name = Account.name
        _.Nickname = Account.nick
        _.ID = Account.id
        _.Data = {}