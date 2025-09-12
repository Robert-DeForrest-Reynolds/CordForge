from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from PIL import Image as PillowImage
from PIL import ImageDraw, ImageFont

from ..Vector2 import Vector2
from ..Colors import *
from ..Font import Font

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
    Font:Font
    Drawing:ImageDraw


    def __init__(_, Cord:Cord=None, X:int=0, Y:int=0, Parent:"Component"=None,
                 Width:int|None=0, Height:int|None=0,
                 Color:Color=None,Background:Color=GRAY, Font:Font=None,
                 Border:bool=False):
        _.Cord = Cord
        _.Parent = Parent
        _.Color = Color
        _.Background = Background
        _.Border = Border
        _.BorderColor = WHITE
        _.BorderWidth = 1
        _.Children = []
        _.Font = Font if Font else (Parent.Font if Parent else _.Cord.Font)
        _.X = X
        _.Y = Y
        _.Width = _.Cord.Width if Width is None else Width
        _.Height = _.Cord.Height if Height is None else Height
        _.ImageWidth = _.Cord.Width if not _.Parent else _.Parent.Width
        _.ImageHeight = _.Cord.Height if not _.Parent else _.Parent.Height
        _._Determine_Dimensions()
        _.Path = _.Parent.Path + f".{_.__class__.__name__}" if Parent else _.__class__.__name__
        _.Drawing = None


    @property
    def XCenter(_): return _.Width // 2
    @property
    def YCenter(_): return _.Height // 2
    @property
    def ImageCenter(_): return Vector2(_.XCenter, _.YCenter)


    def __str__(_): return _.Path


    def _Determine_Dimensions(_) -> None:
        if _.Parent:
            if _.Parent.Border:
                _.X = _.Parent.X + _.X + _.Parent.BorderWidth
                _.Y = _.Parent.Y + _.Y + _.Parent.BorderWidth
                _.Width = _.Parent.Width - _.Parent.BorderWidth * 2
                _.Height = _.Parent.Height - _.Parent.BorderWidth * 2
            else:
                _.X = _.X + _.Parent.X
                _.Y = _.Y + _.Parent.Y
                _.Width = _.Parent.Width
                _.Height = _.Parent.Height



    async def Debug(_, VerticalCenter:bool=False, HorizontalCenter:bool=False) -> None:
        if VerticalCenter:
            await _.Cord.Line(Parent=_, Start=Vector2(_.XCenter, 0), End=Vector2(_.XCenter, _.Height), Width=3, Color=DEBUG_COLOR)
        if HorizontalCenter:
            await _.Cord.Line(Parent=_, Start=Vector2(0, _.YCenter), End=Vector2(_.Width, _.YCenter), Width=3, Color=DEBUG_COLOR)


    async def Draw(_) -> None:
        print("Drawing Base")
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=_.Background)
        _.Drawing = ImageDraw.Draw(_.Image)
        await _.Construct_Components()


    async def Construct_Components(_):
        print(f"Constructing {_} Components")
        Child:Component
        for Child in _.Children:
            ChildImage = await Child.Draw()
            _.Image.paste(ChildImage, (Child.X, Child.Y), mask=ChildImage.split()[3])


    async def Get_Text_Width(_, Text:str, Font:Font=None) -> int:
        TestFont:Font = Font if Font is not None else _.Cord.Font
        MeasuringImage = PillowImage.new("RGBA", (10, 10))
        Drawing = ImageDraw.Draw(MeasuringImage)
        return int(Drawing.textlength(Text, font=TestFont.Font))
