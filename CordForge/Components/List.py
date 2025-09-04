from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from decimal import Decimal, InvalidOperation

from .Component import *
from .ListItem import ListItem

from ..Utilities import Format_Numeric


class List(Component):
    def __init__(_, Cord:Cord, X:int, Y:int, Parent:Component,
                 Width:int|None, Height:int|None,
                 Items:list[str], Font:CFFont, Separation:int,
                 Horizontal:bool, VerticalCenter:bool, HorizontalCenter:bool) -> None:
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent, Width=Width, Height=Height)
        _.Font = Font if Font is not None else None
        _.Font = _.Parent.Font if _.Parent else _.Cord.Font
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
            
        TotalHeight = sum(max((Item.Font.Height if Item.Font else _.Font.Height),(Item.Image.height if Item.Image else 0)) + _.Separation for Item in _.Items)
        if _.VerticalCenter:
            Y = _.YCenter - (TotalHeight // 2) if _.VerticalCenter else _.Y
        else:
            Y = (TotalHeight // 2) if _.VerticalCenter else _.Y
        Ruler = 0
        Item:ListItem
        for Item in _.Items:
            Font = Item.Font if Item.Font else _.Font
            Numeric = None
            try:Numeric = await Format_Numeric(float(Decimal(Item.Text.replace(",",""))))
            except InvalidOperation: pass
            FontWidth = await _.Get_Text_Width(Numeric, Font=Font) if Numeric else await _.Get_Text_Width(Item.Text, Font=Font)
            if Item.Image:
                if _.HorizontalCenter:
                    ImageX = _.XCenter - FontWidth//2 - Item.Image.width + Item.Separation
                else:
                    ImageX = FontWidth//2 - Item.Image.width + Item.Separation
                ImageY = Y + Ruler + Item.Image.height//2
                _.Image.paste(im=Item.Image, box=(ImageX, ImageY), mask=Item.Image)
            if _.HorizontalCenter:
                TextX = _.XCenter - FontWidth//2 + ((Item.Image.width + Item.Separation)//2 if Item.Image else 0)
            else:
                TextX = FontWidth//2 + ((Item.Image.width + Item.Separation)//2 if Item.Image else 0)
            Drawing.text((TextX, Y + Ruler),
                          Numeric if Numeric else Item.Text,
                          font=Font.Font,
                          fill=WHITE)
            Ruler += Font.Height + _.Separation
        return _.Image