from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from .Component import *


class Container(Component):
    def __init__(_, Cord:Cord, X:int, Y:int, Parent:Component,
                 Width:int, Height:int, Background:Color,
                 Border:bool):
        super().__init__(Cord=Cord, X=X, Y=Y, Width=Width, Height=Height, Parent=Parent, Background=Background, Border=Border)


    async def Draw(_) -> PillowImage:
        await super().Draw()
        if _.Border:
            _.Drawing.rectangle([0, 0, _.Width-1, _.Height-1], outline=_.BorderColor, width=_.BorderWidth)
        return _.Image