from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING: from Cord import Cord

from PIL import Image as PillowImage
from PIL import ImageDraw, ImageFont

from ..Vector2 import Vector2
from ..Colors import *
from ..Font import Font

class Component:
    width:int
    height:int
    x:int
    y:int
    background:Color
    color:Color
    border:bool
    border_color:Color
    border_width:int
    parent:"Component"
    children:list["Component"]
    image:PillowImage
    font:Font
    drawing:ImageDraw


    def __init__(_, cord:Cord=None, x:int=0, y:int=0, parent:"Component"=None,
                 width:int|None=0, height:int|None=0,
                 color:Color=None,background:Color=GRAY, font:Font=None,
                 border:bool=False):
        _.cord = cord
        _.parent = parent
        _.color = color
        _.background = background
        _.border = border
        _.border_color = WHITE
        _.border_width = 1
        _.children = []
        _.font = font if font else (parent.font if parent else _.cord.font)
        _.x = x
        _.y = y
        _.width = _.cord.width if width is None else width
        _.height = _.cord.height if height is None else height
        _.image_width = _.cord.width if not _.parent else _.parent.width
        _.image_height = _.cord.height if not _.parent else _.parent.height
        _._determine_dimensions()
        _.path = _.parent.path + f".{_.__class__.__name__}" if parent else _.__class__.__name__
        _.drawing = None


    @property
    def x_center(_): return _.width // 2
    @property
    def y_center(_): return _.height // 2
    @property
    def image_center(_): return Vector2(_.x_center, _.y_center)


    def __str__(_): return _.path


    def _determine_dimensions(_) -> None:
        if _.parent:
            if _.parent.border:
                _.x = _.parent.x + _.x + _.parent.border_width
                _.y = _.parent.y + _.y + _.parent.border_width
                _.width = _.parent.width - _.parent.border_width * 2
                _.height = _.parent.height - _.parent.border_width * 2
            else:
                _.x = _.x + _.parent.x
                _.y = _.y + _.parent.y
                _.width = _.parent.width
                _.height = _.parent.height



    async def debug(_, vertical_center:bool=False, horizontal_center:bool=False) -> None:
        if vertical_center:
            await _.cord.Line(parent=_, start=Vector2(_.x_center, 0), end=Vector2(_.x_center, _.height), fill_width=3, color=DEBUG_COLOR)
        if horizontal_center:
            await _.cord.Line(parent=_, start=Vector2(0, _.y_center), end=Vector2(_.width, _.y_center), fill_width=3, color=DEBUG_COLOR)


    async def draw(_) -> None:
        print("Drawing Base")
        _.image = PillowImage.new("RGBA", (_.width, _.height), color=_.background)
        _.drawing = ImageDraw.Draw(_.image)
        await _.construct_components()


    async def construct_components(_):
        print(f"Constructing {_} Components")
        child:Component
        for child in _.children:
            child_image = await child.draw()
            _.image.paste(child_image, (child.x, child.y), mask=child_image.split()[3])


    async def get_text_width(_, text:str, font:Font=None) -> int:
        test_font:Font = font if font is not None else _.cord.font
        measuring_image = PillowImage.new("RGBA", (10, 10))
        drawing = ImageDraw.Draw(measuring_image)
        return int(drawing.textlength(text, font=test_font.font))
