from os.path import join
from PIL import Image as PillowImage
from io import BytesIO
from discord import File as DiscordFile
from discord import Message as DiscordMessage
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle, Embed, Intents, Member
from discord.ext.commands import Command
from discord.ui import Button, View
from discord.ext.commands import Bot, Context
from sys import argv, path
from itertools import product
import asyncio
from typing import Callable, Any

from .Components import *
from .Colors import *
from .Font import Font as CFFont
from .Vector2 import Vector2
from .Player import Player
from .Data import Data


class Cord(Bot):
    Message:DiscordMessage
    def __init__(_, dashboard_alias:str, entry:Callable, autosave:bool=False) -> None:
        _.dashboard_alias = dashboard_alias
        _._entry = entry
        _.autosave = autosave
        _._handle_alias()
        _.source_directory = path[0]
        _.instance_user:str = argv[1]
        _.base_view_frame = None
        _.embed_frame = None
        _.image = None
        _.image_components = []
        _.image_file = None
        _.view_content = []
        _.embed_content = []
        _.message = None
        _.dashboard_background = GRAY
        _.height = 640
        _.width = 640
        _.font = CFFont(24)
        _.data = Data(_)
        _.players:dict[int:Player] = {}
        print("Discord Bot Initializing")
        super().__init__(command_prefix=_.prefix, intents=Intents.all())


    @property
    def x_center(_): return _.width // 2
    @property
    def y_center(_): return _.height // 2
    @property
    def image_center(_): return Vector2(_.x_center, _.y_center)
    

    def run_task(_, Task, *Arguments) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(Task(*Arguments))
        raise RuntimeError("There is an existing loop.\n" \
                           "Run() is used for setup before the Bot runs it's loop.")


    def _handle_alias(_) -> None:
        _.prefix = [_.dashboard_alias[0]]
        for prefix in _.prefix.copy():
            _.prefix.extend([variant for variant in _._all_case_variants(prefix, _.prefix)\
                                        if variant not in _.prefix])
        _.dashboard_alias = [_.dashboard_alias[1:]]
        for alias in _.dashboard_alias.copy():
            _.dashboard_alias.extend([variant for variant in _._all_case_variants(alias, _.dashboard_alias)\
                                        if variant not in _.dashboard_alias])


    def _all_case_variants(_, string: str, originals:list[str]):
        pools = [(character.lower(), character.upper()) for character in string]
        variants = []
        for variant in product(*pools):
            string = ''.join(variant)
            if string not in originals: variants.append(string)
        return variants


    def _get_token(_, key:str) -> str:
        with open(join(_.source_directory, "Keys")) as key_file:
            for line in key_file:
                line_data = line.split("=")
                if key.lower() == line_data[0].lower():
                    return line_data[1].strip()
        return "Could Not Find Token"


    async def setup_hook(_):
        async def wrapper(context): await _.send_dashboard_command(context)
        _.add_command(Command(wrapper, aliases=_.dashboard_alias))
        await super().setup_hook()


    async def on_ready(_) -> None:
        print("Bot is alive.\n")
        await _.data.load_data()
        if _.autosave:
            await _.data.autosave()


    def launch(_) -> None: _.run(_._get_token(_.instance_user))


    def load_image(_, image_path:str) -> PillowImage:
        return PillowImage.open(image_path)


    async def new_image(_) -> PillowImage:
        _.image = PillowImage.new("RGBA",
                                  (_.height, _.width),
                                  color=_.dashboard_background)
        return _.image


    async def send_image(_, interaction:DiscordInteraction, image_path:str) -> None:
        _.image_file = DiscordFile(image_path, filename="GameImage.png")
        await _.reply(interaction)
    

    async def save_image(_, path:str="CordImage") -> None:
        if not hasattr(_, "image") or _.image is None:
            raise ValueError("No image found. Did you run Create_Image first?")
        _.image.save(path + ".PNG", format="PNG")
    
    
    async def buffer_image(_) -> DiscordFile:
        buffer = BytesIO()
        _.image.save(buffer, format="PNG")
        buffer.seek(0)
        _.image_file = DiscordFile(buffer, filename="GameImage.png")
        buffer.close()
        return _.image_file
    

    async def container(_, x:int=0, y:int=0, parent:Component|None=None,
                        width:int|None=None, height:int|None=None, 
                        background:Color=GRAY, border:bool=False) -> Component:
        '''
        Create a Container Component\n
        A container's height and width is by default the parent container if given one, elsewise it's the Cord object that is it is created with.
        '''
        new_container = Container(cord=_, x=x, y=y, parent=parent,
                                 width=width, height=height,
                                 background=background, border=border)
        if parent == None:
            _.image_components.append(new_container)
        else:
            parent.Children.append(new_container)
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
            parent.Children.append(new_line)
        return new_line


    async def list(_, x:int=0, y:int=0, parent:Component|None=None,
                   width:int|None=None, height:int|None=None,
                   items:list[str:ListItem] = [], font=None,
                   separation:int=4, horizontal:bool=False,
                   vertical_center:bool=False, horizontal_center:bool=False) -> None:
        new_list = List(cord=_, x=x, y=y, parent=parent,
                       width=width, height=height,
                       items=items, font=font,
                       separation=separation,
                       horizontal=horizontal, vertical_center=vertical_center,
                       horizontal_center=horizontal_center)
        if parent == None:
            _.image_components.append(new_list)
        else:
            parent.Children.append(new_list)
        return new_list
    

    async def text(_, content, position:List|Vector2|None=None, parent:Component|None=None,
                   color:Color=WHITE, background:Color=None, font:CFFont=None,
                   center:bool=False) -> Component:
        new_text = Text(cord=_, content=content, position=position, parent=parent, color=color, background=background, font=font, center=center)
        if parent == None:
            _.image_components.append(new_text)
        else:
            parent.Children.append(new_text)
        return new_text
    

    async def sprite(_, x:int=0, y:int=0, parent:Component|None=None,
                    sprite_image:PillowImage=None, path:str=None) -> None:
        new_sprite = Sprite(cord=_, x=x, y=y, parent=parent, sprite_image=sprite_image, path=path)
        if parent == None:
            _.image_components.append(new_sprite)
        else:
            parent.Children.append(new_sprite)
        return new_sprite


    async def debug(_, vertical_center:bool=False, horizontal_center:bool=False) -> None:
        if vertical_center:
            await _.line(start=Vector2(_.x_center, 0), end=Vector2(_.x_center, _.height), fill_width=3, color=DEBUG_COLOR)
        if horizontal_center:
            await _.line(start=Vector2(0, _.y_center), end=Vector2(_.width, _.y_center), fill_width=3, color=DEBUG_COLOR)


    async def add_button(_, label:str, callback:Callable, arguments:list) -> None:
        new_button = Button(label=label, style=ButtonStyle.grey)
        new_button.callback = lambda interaction: callback(interaction, *arguments)
        _.view_content.append(new_button)


    async def construct_components(_):
        print("Constructing Dashboard Components")
        image_component:Component
        for image_component in _.image_components:
            component_image:PillowImage = await image_component.draw()
            _.image.paste(im=component_image, box=(image_component.x, image_component.y), mask=component_image.split()[3])
        _.image_components = []


    async def construct_view(_) -> None:
        _.base_view_frame = View(timeout=144000)
        if len(_.view_content) > 0:
            for content in _.view_content:
                _.base_view_frame.add_item(content)
        _.view_content = []


    async def reply(_, interaction:DiscordInteraction) -> None:
        _.base_view_frame = View(timeout=144000)
        await _.construct_view()

        if _.base_view_frame.total_children_count > 0 and _.image == None:
            await interaction.response.edit_message(embed=_.embed_frame, view=_.base_view_frame)
        elif _.image != None:
            await _.construct_components()
            _.embed_frame = Embed(title="")
            _.embed_frame.set_image(url="attachment://GameImage.png")
            await _.buffer_image()
            await interaction.response.edit_message(embed=_.embed_frame, view=_.base_view_frame, attachments=[_.image_file])
            _.image_file = None
        else:
            print("Your Reply has nothing on it.")


    async def send_dashboard_command(_, initial_context:Context=None) -> None:
        if initial_context.author.id not in _.players.keys(): _.data.initial_cache(initial_context.author)

        await initial_context.message.delete()
        
        if _.message is not None: await _.message.delete()
        
        user:Player = _.players[initial_context.author.id]
        
        try:
            await _._entry(user)
        except TypeError as e:
            print("Entry needs to accept `user` as an argument")
        
        _.base_view_frame = View(timeout=144000)
        await _.construct_view()
        
        if _.base_view_frame.total_children_count > 0 and _.image == None:
            _.message = await initial_context.send(embed=_.embed_frame, view=_.base_view_frame)
        elif _.image != None:
            await _.construct_components()
            _.embed_frame = Embed(title="")
            _.embed_frame.set_image(url="attachment://GameImage.png")
            await _.buffer_image()
            _.message = await initial_context.send(embed=_.embed_frame, view=_.base_view_frame, file=_.image_file)
        else:
            print("Your Dashboard has nothing on it.")