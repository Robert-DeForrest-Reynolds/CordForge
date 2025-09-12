from os.path import join
from PIL import Image
from io import BytesIO
from discord import File as DiscordFile
from discord import ButtonStyle, Embed, Intents, Member, Interaction, Message
from discord.ext.commands import Command, Bot, Context
from discord.ui import Button, View
from sys import argv, path
from itertools import product
import asyncio
from typing import Callable, Any

from .components import *
from card import Card
from .colors import *
from .font import Font as CFFont
from .vector2 import Vector2
from .player import Player
from .data import Data


class Cord(Bot):
    Message:Message
    def __init__(_, dashboard_alias:str, entry:Callable, autosave:bool=False) -> None:
        _.dashboard_alias = dashboard_alias
        _._entry = entry
        _.autosave = autosave
        _._handle_alias()
        _.source_directory = path[0]
        _.instance_user:str = argv[1]
        _.user_dashboards:dict[str:Panel] = {}
        _.data = Data(_)
        _.players:dict[int:Player] = {}
        _.message:Message = None
        print("Discord Bot Initializing")
        super().__init__(command_prefix=_.prefix, intents=Intents.all())
    

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


    def launch(_) -> None:
        'Start Discord Bot'
        _.run(_._get_token(_.instance_user))


    async def new_card(_, user:Member, initial_context:Context) -> Card:
        user_card:Card = Card()
        player:Player = _.players[initial_context.author.id]


    async def reply(_, interaction:Interaction) -> None:
        _.base_view_frame = View(timeout=144000)
        await _._construct_view()

        if _.base_view_frame.total_children_count > 0 and _.image == None:
            await interaction.response.edit_message(embed=_.embed_frame, view=_.base_view_frame)
        elif _.image != None:
            await _._construct_components()
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
        await _._construct_view()
        
        if _.base_view_frame.total_children_count > 0 and _.image == None:
            _.message = await initial_context.send(embed=_.embed_frame, view=_.base_view_frame)
        elif _.image != None:
            await _._construct_components()
            _.embed_frame = Embed(title="")
            _.embed_frame.set_image(url="attachment://GameImage.png")
            await _.buffer_image()
            _.message = await initial_context.send(embed=_.embed_frame, view=_.base_view_frame, file=_.image_file)
        else:
            print("Your Dashboard has nothing on it.")