from PIL import Image as PillowImage
from PIL import ImageDraw, ImageFont
from .Colors import *
from .ListItem import ListItem
from .Vector2 import Vector2
from decimal import Decimal, InvalidOperation
from .Utilities import Format_Numeric


class Component:
    Width:int
    Height:int
    X:int
    Y:int
    Background:tuple[int,int,int,int]
    Border:bool
    BorderColor:tuple[int,int,int,int]
    BorderWidth:int
    Parent:"Component"
    Children:list["Component"]
    Image:PillowImage
    Font:ImageFont


    def __init__(_, Cord, X:int=0, Y:int=0, Width:int=0, Height:int=0, Parent:"Component"=None, Background:tuple[int,int,int,int]=GRAY):
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
            _.Width = Width
            _.Height = Height
        _.Cord = Cord
        _.Parent = Parent
        _.Background = Background
        _.Border = False
        _.BorderColor = WHITE
        _.BorderWidth = 1
        _.Children = []
        _.Font = ImageFont.load_default(24)
        _.Ascent, _.Descent = _.Font.getmetrics()
        _.FontHeight = _.Ascent + _.Descent


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
        if Font is None:
            Font = _.Font
        MeasuringImage = PillowImage.new("RGBA", (10, 10))
        Drawing = ImageDraw.Draw(MeasuringImage)
        return int(Drawing.textlength(Text, font=Font))


class Container(Component):
    def __init__(_, Cord, X:int, Y:int, Width:int, Height:int, Parent, Background):
        super().__init__(Cord=Cord, X=X, Y=Y, Width=Width, Height=Height, Parent=Parent, Background=Background)


    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=_.Background)
        await _.Construct_Components()
        if _.Border:
            Drawing = ImageDraw.Draw(_.Image)
            Drawing.rectangle([0, 0, _.Width-1, _.Height-1], outline=_.BorderColor, width=_.BorderWidth)
        return _.Image


class List(Component):
    def __init__(_, Cord, X:int, Y:int, Parent:Component,
                 Items:list[str], Font, Separation:int,
                 Horizontal:bool, VerticalCenter:bool, HorizontalCenter:bool) -> None:
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent)
        if Font != None: _.Font = Font
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
        Y = _.YCenter - ((_.FontHeight + _.Separation) * len(_.Items) // 2) if _.VerticalCenter else _.Y
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
                            font=_.Font,
                            fill=WHITE)
            TotalHeight += _.FontHeight + _.Separation
        return _.Image


class Line(Component):
    def __init__(_, Cord, X, Y, Start:Vector2, End:Vector2, Parent:Component, Width:int, Color:tuple[int,int,int,int], Curve:bool):
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent, Width=Width)
        _.Start = Start
        _.End = End
        _.Width = Width
        _.Color = Color
        _.Curve = Curve
        _.ImageWidth = _.Cord.Width if not Parent else Parent.Width
        _.ImageHeight = _.Cord.Height if not Parent else Parent.Height
    
    
    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.ImageWidth, _.ImageHeight), color=TRANSPRENCY)
        Drawing = ImageDraw.Draw(_.Image)
        Drawing.line(xy=((_.Start.X, _.Start.Y), (_.End.X, _.End.Y)),
                     fill=_.Color,
                     width=_.Width,
                     joint="curve" if _.Curve else None)
        return _.Image
