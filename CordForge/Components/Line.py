from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from cord import Cord

from .component import *


class Line(Component):
    def __init__(_, cord:Cord, x, y, start:Vector2, end:Vector2, parent:Component, fill_width:int, color:Color, curve:bool):
        super().__init__(cord=cord, x=x, y=y, parent=parent)
        _.start = start
        _.end = end
        _.fill_width = fill_width
        _.color = color
        _.curve = curve
    
    
    async def draw(_) -> Image:
        super().draw()
        _.drawing.line(xy=((_.start.x, _.start.y), (_.end.x, _.end.y)),
                     fill=_.color,
                     width=_.fill_width,
                     joint="curve" if _.curve else None)
        return _.image