from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from cord import Cord
from .component import *


class Text(Component):
    def __init__(_, cord:Cord, position:list|Vector2|None, parent:Component,
                 content:str, color:Color, background:Color,
                 font:Font, center:bool):
        super().__init__(cord=cord, parent=parent, width=None, height=None, color=color, font=font, background=background)
        _.content = content
        _.center = center
        if type(position) is list:
            _.position = Vector2(position[0], position[1])
        else:
            _.position = position
        _.color = color
        _.font = font if font is not None else _.cord.font


    async def draw(_) -> Image:
        super().draw()
        if _.center:
            _.content_width = await _.get_text_width(_.content)
            if _.position != None:
                raise("Text component cannot be given a position, and be centered.")
            _.position = Vector2()
            if _.parent:
                _.position.x = _.parent.width//2 - _.content_width//2
                _.position.y = _.parent.height//2 - _.font.height//2
            else:
                _.position.x = _.cord.width//2 - _.content_width//2
                _.position.y = _.cord.height//2 - _.font.height//2
        _.drawing.text(text=_.content,
                     xy=(_.position.x, _.position.y),
                     fill=_.color,
                     font=_.font.font)
        return _.image