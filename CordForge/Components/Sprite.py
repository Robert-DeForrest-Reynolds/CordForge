from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord
from .Component import *


class Sprite(Component):
    def __init__(_, Cord:Cord, X:int, Y:int, Parent:Component,
                 SpriteImage:PillowImage, Path:str) -> None:
        super().__init__(Cord=Cord, X=X, Y=Y, Parent=Parent,
                         Width=None, Height=None)
        _.SpriteImage = SpriteImage
        _.Path = Path
        if Path and SpriteImage is None:
            _.SpriteImage = PillowImage.open(Path)


    async def Draw(_):
        _.Image = PillowImage.new("RGBA", (_.Width, _.Height), color=_.Background)
        _.Image.paste(im=_.SpriteImage, box=(_.X, _.Y), mask=_.SpriteImage.split()[3])
        return _.Image