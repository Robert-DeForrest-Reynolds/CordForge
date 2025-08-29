from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from .Component import *


class Line(Component):
    def __init__(_, Cord:Cord, X, Y, Start:Vector2, End:Vector2, Parent:Component, FillWidth:int, Color:Color, Curve:bool):
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent)
        _.Start = Start
        _.End = End
        _.FillWidth = FillWidth
        _.Color = Color
        _.Curve = Curve
    
    
    async def Draw(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA", (_.ImageWidth, _.ImageHeight), color=TRANSPRENCY)
        Drawing = ImageDraw.Draw(_.Image)
        Drawing.line(xy=((_.Start.X, _.Start.Y), (_.End.X, _.End.Y)),
                     fill=_.Color,
                     width=_.FillWidth,
                     joint="curve" if _.Curve else None)
        return _.Image