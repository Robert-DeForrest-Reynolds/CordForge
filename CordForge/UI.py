from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Cord import Cord

from PIL import Image as PillowImage
from PIL import ImageDraw, ImageFont
from decimal import Decimal, InvalidOperation

from .Colors import *
from .ListItem import ListItem
from .Vector2 import Vector2
from .Utilities import Format_Numeric
from .Font import Font as CFFont


class Component:
    Width:int
    Height:int
    X:int
    Y:int
    Background:Color
    Color:Color
    Border:bool
    BorderColor:Color
    BorderWidth:int
    Parent:"Component"
    Children:list["Component"]
    Image:PillowImage
    Font:CFFont


    def __init__(_, Cord:Cord=None, X:int=0, Y:int=0, Parent:"Component"=None,
                 Width:int=0, Height:int=0, Color:Color=None, Background:Color=GRAY, Font:CFFont=None):
        _.Cord = Cord
        if Parent:
            if Parent.Border:
                _.X = Parent.X + X + Parent.BorderWidth
                _.Y = Parent.Y + Y + Parent.BorderWidth
                _.Width = Parent.Width - Parent.BorderWidth * 2
                _.Height = Parent.Height - Parent.BorderWidth * 2
            else:
                _.X = X + Parent.X
                _.Y = Y + Parent.Y
                _.Width = Parent.Width
                _.Height = Parent.Height
        else:
            _.X = X
            _.Y = Y
            _.Width = _.Cord.Width
            _.Height = _.Cord.Height
        _.Parent = Parent
        _.Color = Color
        _.Background = Background
        _.Border = False
        _.BorderColor = WHITE
        _.BorderWidth = 1
        _.Children = []
        _.Font = _.Cord.Font if not Parent else Font
        _.ImageWidth = _.Cord.Width if not Parent else Parent.Width
        _.ImageHeight = _.Cord.Height if not Parent else Parent.Height


    @property
    def XCenter(_): return _.Width // 2
    @property
    def YCenter(_): return _.Height // 2
    @property
    def ImageCenter(_): return Vector2(_.XCenter, _.YCenter)


    async def Draw() -> PillowImage:...


    async def Construct_Components(_):
        Child:Component
        for Child in _.Children:
            ChildImage = await Child.Draw()
            _.Image.paste(ChildImage, (Child.X, Child.Y), mask=ChildImage.split()[3])


    async def Get_Text_Width(_, Text, Font=None) -> list:
        _.Font = Font if Font is not None else _.Cord.Font
        MeasuringImage = PillowImage.new("RGBA", (10, 10))
        Drawing = ImageDraw.Draw(MeasuringImage)
        return int(Drawing.textlength(Text, font=_.Font.Font))


class Container(Component):
    def __init__(_, Cord:Cord, X:int, Y:int, Parent:Component,
                 Width:int, Height:int, Background:Color):
        super().__init__(Cord=Cord, X=X, Y=Y, Width=Width, Height=Height, Parent=Parent, Background=Background)


    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=_.Background)
        await _.Construct_Components()
        if _.Border:
            Drawing = ImageDraw.Draw(_.Image)
            Drawing.rectangle([0, 0, _.Width-1, _.Height-1], outline=_.BorderColor, width=_.BorderWidth)
        return _.Image


class List(Component):
    def __init__(_, Cord:Cord, X:int, Y:int, Parent:Component,
                 Items:list[str], Font:CFFont, Separation:int,
                 Horizontal:bool, VerticalCenter:bool, HorizontalCenter:bool) -> None:
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent)
        _.Font = Font if Font is not None else Cord.Font
        _.Height = _.Cord.Height
        _.Items = Items
        _.Separation = Separation
        _.Horizontal = Horizontal
        _.VerticalCenter = VerticalCenter
        _.HorizontalCenter = HorizontalCenter


    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=TRANSPRENCY)
        Drawing = ImageDraw.Draw(_.Image)
        if _.Border:
            Drawing.rectangle([0, 0, _.Width-1, _.Height-1], outline=_.BorderColor, width=_.BorderWidth)
        Y = _.YCenter - ((_.Font.Height + _.Separation) * len(_.Items) // 2) if _.VerticalCenter else _.Y
        TotalHeight = 0
        Item:ListItem
        for Item in _.Items:
            Numeric = None
            try:Numeric = await Format_Numeric(float(Decimal(Item.Text.replace(",",""))))
            except InvalidOperation: pass
            FontWidth = await _.Get_Text_Width(Numeric) if Numeric else await _.Get_Text_Width(Item.Text)
            if Item.Image:
                ImageX = _.XCenter - FontWidth//2 - Item.Image.width + Item.Separation
                _.Image.paste(im=Item.Image, box=(ImageX, Y + TotalHeight), mask=Item.Image)
            TextX = _.XCenter - FontWidth//2 + ((Item.Image.width + Item.Separation)//2 if Item.Image else 0)
            Drawing.text((TextX, Y + TotalHeight),
                            Numeric if Numeric else Item.Text,
                            font=_.Font.Font,
                            fill=WHITE)
            TotalHeight += _.Font.Height + _.Separation
        return _.Image


class Line(Component):
    def __init__(_, Cord:Cord, X, Y, Start:Vector2, End:Vector2, Parent:Component, Width:int, Color:Color, Curve:bool):
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent, Width=Width)
        _.Start = Start
        _.End = End
        _.Width = Width
        _.Color = Color
        _.Curve = Curve
    
    
    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.ImageWidth, _.ImageHeight), color=TRANSPRENCY)
        Drawing = ImageDraw.Draw(_.Image)
        Drawing.line(xy=((_.Start.X, _.Start.Y), (_.End.X, _.End.Y)),
                     fill=_.Color,
                     width=_.Width,
                     joint="curve" if _.Curve else None)
        return _.Image


class Text(Component):
    def __init__(_, Cord:Cord, Position:list|Vector2, Parent:"Component",
                 Content:str, Color:Color, Background:Color,
                 Font:CFFont, Center:bool):
        super().__init__(Cord=Cord, Parent=Parent, Color=Color, Font=Font, Background=Background)
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