from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord
from .Component import *


class Text(Component):
    def __init__(_, Cord:Cord, Position:list|Vector2|None, Parent:"Component",
                 Content:str, Color:Color, Background:Color,
                 Font:CFFont, Center:bool):
        super().__init__(Cord=Cord, Parent=Parent, Width=None, Height=None, Color=Color, Font=Font, Background=Background)
        _.Content = Content
        _.Center = Center
        if type(Position) is list:
            _.Position = Vector2(Position[0], Position[1])
        else:
            _.Position = Position
        _.Color = Color
        _.Font = Font if Font is not None else Cord.Font


    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=TRANSPRENCY)
        Drawing = ImageDraw.Draw(_.Image)
        if _.Center:
            _.ContentWidth = await _.Get_Text_Width(_.Content)
            if _.Position != None:
                raise("Text Component cannot be given a position, and be centered.")
            _.Position = Vector2()
            if _.Parent:
                _.Position.X = _.Parent.Width//2 - _.ContentWidth//2
                _.Position.Y = _.Parent.Height//2 - _.Font.Height//2
            else:
                _.Position.X = _.Cord.Width//2 - _.ContentWidth//2
                _.Position.Y = _.Cord.Height//2 - _.Font.Height//2
        Drawing.text(text=_.Content,
                     xy=(_.Position.X, _.Position.Y),
                     fill=_.Color,
                     font=_.Font.Font)
        return _.Image