from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord
from .Component import *


class Sprite(Component):
    def __init__(_, cord:Cord, x:int, y:int, parent:Component,
                 sprite_image:PillowImage, path:str) -> None:
        super().__init__(cord=cord, x=x, y=y, parent=parent,
                         width=None, height=None)
        _.sprite_image = sprite_image
        _.path = path
        if path and sprite_image is None:
            _.sprite_image = PillowImage.open(path)


    async def draw(_) -> PillowImage:
        _.image = PillowImage.new("RGBA", (_.width, _.height), color=_.background)
        _.image.paste(im=_.sprite_image, box=(_.x, _.y), mask=_.sprite_image.split()[3])
        return _.image