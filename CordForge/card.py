from discord import File as DiscordFile
from discord import ButtonStyle, Embed, Intents, Member, Interaction, Message
from discord.ui import Button, View
from discord.ext.commands import Context
from PIL import Image
from io import BytesIO
from typing import Callable, Any

from .components import *
from .colors import *
from .vector2 import Vector2
from .font import Font
from .user import User

class Card:
    def __init__(_, user:User=None) -> None:
        _.user = user
        _.view_frame:View = None
        _.embed_frame:Embed = None
        _.image:Image = None
        _.image_components:list[Component] = []
        _.image_file:DiscordFile = None
        _.view_content = []
        _.embed_content = []
        _.dashboard_background = GRAY
        _.height = 640
        _.width = 640
        _.font = Font(24)
        _.message:Message = None


    async def construct(_) -> "Card":
        await _._construct_view()
        await _._construct_components()
        return _


    async def _construct_components(_):
        image_component:Component
        for image_component in _.image_components:
            component_image:Image = await image_component.draw()
            _.image.paste(im=component_image, box=(image_component.x, image_component.y), mask=component_image.split()[3])
        _.image_components = []


    async def _construct_view(_) -> None:
        _.view_frame = View(timeout=144000)
        if len(_.view_content) > 0:
            for content in _.view_content:
                _.view_frame.add_item(content)
        _.view_content = []
    
    
    async def _buffer_image(_) -> DiscordFile:
        buffer = BytesIO()
        _.image.save(buffer, format="PNG")
        buffer.seek(0)
        _.image_file = DiscordFile(buffer, filename="GameImage.png")
        buffer.close()
        return _.image_file


    async def new_image(_) -> Image:
        'Create new image'
        _.image = Image.new("RGBA",
                                    (_.height, _.width),
                                    color=_.dashboard_background)
        return _.image


    async def send_image(_, interaction:Interaction, image_path:str) -> None:
        _.image_file = DiscordFile(image_path, filename="GameImage.png")
        await _.reply(interaction)
    

    async def save_image(_, path:str="CordImage") -> None:
        if not hasattr(_, "image") or _.image is None:
            raise ValueError("No image found. Did you run Create_Image first?")
        _.image.save(path + ".PNG", format="PNG")


    async def add_button(_, label:str, callback:Callable, arguments:list) -> None:
        new_button = Button(label=label, style=ButtonStyle.grey)
        new_button.callback = lambda interaction: callback(_, interaction, *arguments)
        _.view_content.append(new_button)
    

    async def panel(_, x:int=0, y:int=0, parent:Component|None=None,
                    width:int|None=None, height:int|None=None, 
                    background:Color=GRAY, border:bool=False) -> Component:
        '''
        Create a Container Component\n
        A container's height and width is by default the parent container if given one, elsewise it's the Cord object that is it is created with.
        '''
        new_container = Panel(cord=_, x=x, y=y, parent=parent,
                                width=width, height=height,
                                background=background, border=border)
        if parent == None:
            _.image_components.append(new_container)
        else:
            parent.children.append(new_container)
        return new_container


    async def line(_, x:int=0, y:int=0, parent:Component|None=None,
                   start:Vector2=Vector2(0,0), end:Vector2=Vector2(0,0),
                   color:Color=WHITE, fill_width:int=1,
                   curve:bool=False) -> None:
        new_line = Line(cord=_, x=x, y=y, parent=parent,
                       start=start, end=end,
                       fill_width=fill_width, color=color, curve=curve)
        if parent == None:
            _.image_components.append(new_line)
        else:
            parent.children.append(new_line)
        return new_line


    async def display(_, x:int=0, y:int=0, parent:Component|None=None,
                   width:int|None=None, height:int|None=None,
                   items:list[str:display_item] = [], font=None,
                   separation:int=4, horizontal:bool=False,
                   vertical_center:bool=False, horizontal_center:bool=False) -> None:
        new_display = Display(cord=_, x=x, y=y, parent=parent,
                       width=width, height=height,
                       items=items, font=font,
                       separation=separation,
                       horizontal=horizontal, vertical_center=vertical_center,
                       horizontal_center=horizontal_center)
        if parent == None:
            _.image_components.append(new_display)
        else:
            parent.children.append(new_display)
        return new_display
    

    async def text(_, content, position:list[int,int]|Vector2|None=None, parent:Component|None=None,
                   color:Color=WHITE, background:Color=None, font:Font=None,
                   center:bool=False) -> Component:
        new_text = Text(cord=_, content=content, position=position, parent=parent, color=color, background=background, font=font, center=center)
        if parent == None:
            _.image_components.append(new_text)
        else:
            parent.children.append(new_text)
        return new_text
    

    async def sprite(_, x:int=0, y:int=0, parent:Component|None=None,
                    sprite_image:Image=None, path:str=None) -> None:
        new_sprite = Sprite(cord=_, x=x, y=y, parent=parent, sprite_image=sprite_image, path=path)
        if parent == None:
            _.image_components.append(new_sprite)
        else:
            parent.children.append(new_sprite)
        return new_sprite


    async def debug(_, vertical_center:bool=False, horizontal_center:bool=False) -> None:
        if vertical_center:
            await _.line(start=Vector2(_.x_center, 0), end=Vector2(_.x_center, _.height), fill_width=3, color=DEBUG_COLOR)
        if horizontal_center:
            await _.line(start=Vector2(0, _.y_center), end=Vector2(_.width, _.y_center), fill_width=3, color=DEBUG_COLOR)