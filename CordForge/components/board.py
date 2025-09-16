from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from cord import Cord

from decimal import Decimal, InvalidOperation

from .component import *
from .board_item import BoardItem

from ..utilities import format_numeric


class Board(Component):
    def __init__(_, cord:Cord, x:int, y:int, parent:Component,
                 width:int|None, height:int|None,
                 items:list[str], font:Font, separation:int,
                 horizontal:bool, vertical_center:bool, horizontal_center:bool) -> None:
        super().__init__(cord=cord, x=x, y=y, parent=parent, width=width, height=height)
        _.font = font if font is not None else _.font
        _.height = _.cord.height
        _.items = items
        _.separation = separation
        _.horizontal = horizontal
        _.vertical_center = vertical_center
        _.horizontal_center = horizontal_center


    async def draw(_) -> Image:
        await super().draw()
        if _.border:
            _.drawing.rectangle([0, 0, _.width-1, _.height-1], outline=_.border_color, width=_.border_width)
            
        total_height = sum(max((item.font.height if item.font else _.font.height),(item.image.height if item.image else 0)) + _.separation for item in _.items)
        if _.vertical_center:
            y = _.x_center - (total_height // 2) if _.vertical_center else _.y
        else:
            y = (total_height // 2) if _.vertical_center else _.y
        ruler = 0
        item:BoardItem
        for item in _.items:
            font = item.font if item.font is not None else _.font
            numeric = None
            try:numeric = await format_numeric(float(Decimal(item.text.replace(",",""))))
            except InvalidOperation: pass
            font_width = await _.get_text_width(numeric, font=font) if numeric else await _.get_text_width(item.text, font=font)
            if item.image:
                if _.horizontal_center:
                    image_x = _.x_center - font_width//2 - item.image.width + item.separation
                else:
                    image_x = font_width//2 - item.image.width + item.separation
                image_y = y + ruler
                _.image.paste(im=item.image, box=(image_x, image_y), mask=item.image)
            if _.horizontal_center:
                text_x = _.x_center - font_width//2 + ((item.image.width + item.separation)//2 if item.image else 0)
            else:
                text_x = font_width//2 + ((item.image.width + item.separation)//2 if item.image else 0)
            _.drawing.text((text_x, y + ruler),
                          numeric if numeric else item.text,
                          font=font.font,
                          fill=WHITE)
            ruler += font.height + _.separation
        return _.image