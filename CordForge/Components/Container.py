from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from .Component import *


class Container(Component):
    def __init__(_, cord:Cord, x:int, y:int, parent:Component,
                 width:int, height:int, background:Color,
                 border:bool):
        super().__init__(cord=cord, x=x, y=y, width=width, height=height, parent=parent, background=background, border=border)


    async def draw(_) -> PillowImage:
        await super().draw()
        if _.border:
            _.drawing.rectangle([0, 0, _.width-1, _.height-1], outline=_.border_color, width=_.border_width)
        return _.image