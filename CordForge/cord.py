from os.path import join
from PIL import Image
from discord.enums import ChannelType
from discord import ButtonStyle, Embed, Intents, Member, Interaction, Message, TextChannel, VoiceChannel
from discord.abc import GuildChannel
from discord.ext.commands import Command, Bot, Context
from sys import argv, path
from itertools import product
from asyncio import get_running_loop, run
from typing import Callable, Any

from .components import *
from .card import Card
from .colors import *
from .font import Font as CFFont
from .vector2 import Vector2
from .user import User
from .data import Data
from .font import Font


class Cord(Bot):
    def __init__(_, entry_command:str=None, autosave:bool=True) -> None:
        _.entry_command = entry_command
        _.entry:Callable = None
        _.setup:Callable = None
        _.autosave = autosave
        _.source_directory = path[0]
        _.instance_user:str = argv[1]
        _.user_dashboards:dict[str:Panel] = {}
        _.user_traits:list[list[str, Any]] = []
        _.user_profiles = {}
        _.message:Message = None
        _.font:Font = None
        _.data = Data(_)
        _._handle_alias()
        _._setup_user_traits()
        super().__init__(command_prefix=_.prefix, intents=Intents.all())
        

    def _handle_alias(_) -> None:
        _.prefix = [_.entry_command[0]]
        for prefix in _.prefix.copy():
            _.prefix.extend([variant for variant in _._all_case_variants(prefix, _.prefix)\
                                        if variant not in _.prefix])
        _.entry_command = [_.entry_command[1:]]
        for alias in _.entry_command.copy():
            _.entry_command.extend([variant for variant in _._all_case_variants(alias, _.entry_command)\
                                        if variant not in _.entry_command])


    def _all_case_variants(_, string: str, originals:list[str]):
        pools = [(character.lower(), character.upper()) for character in string]
        variants = []
        for variant in product(*pools):
            string = ''.join(variant)
            if string not in originals: variants.append(string)
        return variants


    def _get_token(_, key:str) -> str:
        with open(join(_.source_directory, "keys")) as key_file:
            for line in key_file:
                line_data = line.split("=")
                if key.lower() == line_data[0].lower():
                    return line_data[1].strip()
        return "Could Not Find Token"
    

    def _setup_user_traits(_) -> None:
        for [trait, value] in _.user_traits:
            User.add_trait(trait, value)
        

    def run_task(_, Task, *Arguments) -> Any:
        try: get_running_loop()
        except RuntimeError: return run(Task(*Arguments))
        raise RuntimeError("There is an existing loop. Run() is only used for setup before the Bot runs it's loop.")


    def launch(_, entry:Callable, setup:Callable=None) -> None:
        print("Launching...")
        'Start Discord Bot'
        _.entry = entry
        _.setup = setup
        _.run(_._get_token(_.instance_user))


    async def setup_hook(_):
        async def wrapper(initial_context): await _._send_initial_card(initial_context)
        _.add_command(Command(wrapper, aliases=_.entry_command))
        await super().setup_hook()


    async def on_ready(_):
        print("Bot is alive, and ready")
        print("Setting up...")
        if _.setup: await _.setup()
        print("Finished setup")
        await _.data.load_data()
        if _.autosave: await _.data.autosave()


    async def _send_initial_card(_, initial_context:Context) -> None:
        user:User = User(initial_context.author)
        if user.id not in _.user_profiles.keys():
            _.user_profiles.update({user.id:user})

        await initial_context.message.delete()
        
        if _.message is not None: await _.message.delete()

        user_card:Card = await _.new_card(user, initial_context)

        try:
            await _.entry(user_card)
        except Exception as e:
            print(f"Exception: {e}")

        await user_card.construct()
        if user_card.view_frame.total_children_count > 0 and user_card.image == None:
            user_card.message = await initial_context.send(embed=user_card.embed_frame,
                                                           view=user_card.view_frame)
        elif user_card.image != None:
            user_card.embed_frame = Embed(title="")
            user_card.embed_frame.set_image(url="attachment://GameImage.png")
            await user_card._buffer_image()
            user_card.message = await initial_context.send(embed=user_card.embed_frame,
                                                           view=user_card.view_frame,
                                                           file=user_card.image_file)
        else:
            print("Dashboard has nothing on it.")


    async def announce(_, channel:GuildChannel, message:str=None, card:Card=None) -> Message:
        if channel.type != ChannelType.text:print("announce() is only compatible with TextChannels")
        else:\
        channel:TextChannel = channel
        if message and not card:
            await channel.send(message)
        elif message and card:
            card.embed_frame = Embed(title="")
            card.embed_frame.set_image(url="attachment://GameImage.png")
            await card._buffer_image()
            await channel.send(message, embed=card.embed_frame,
                               view=card.view_frame,
                               file=card.image_file)
            

    async def new_card(_, user:Member=None, initial_context:Context=None) -> Card:
        '''
        Create new card to draw on.

        Returns instantiated Card
        '''
        user_card:Card = Card(user, initial_context)
        return user_card


    def load_image(_, image_path:str) -> Image:
        'Load image from file path into memory'
        return Image.open(image_path)


    async def reply(_, user_card:Card, interaction:Interaction) -> None:
        await user_card.construct()
        if user_card.view_frame.total_children_count > 0 and user_card.image == None:
            user_card.message = await interaction.response.edit_message(embed=user_card.embed_frame,
                                                                        view=user_card.view_frame)
        elif user_card.image != None:
            user_card.embed_frame = Embed(title="")
            user_card.embed_frame.set_image(url="attachment://GameImage.png")
            await user_card._buffer_image()
            user_card.message = await interaction.response.edit_message(embed=user_card.embed_frame,
                                                                        view=user_card.view_frame,
                                                                        attachments=[user_card.image_file])
        else:
            print("Dashboard has nothing on it.")


    async def home(_, user_card:Card, interaction:Interaction) -> None:
        '''
        Brings the user back to the entry() function card
        '''

        try:
            await _.entry(user_card)
        except Exception as e:
            print(f"Exception: {e}")

        await user_card.construct()
        if user_card.view_frame.total_children_count > 0 and user_card.image == None:
            user_card.message = await interaction.response.edit_message(embed=user_card.embed_frame,
                                                                        view=user_card.view_frame)
        elif user_card.image != None:
            user_card.embed_frame = Embed(title="")
            user_card.embed_frame.set_image(url="attachment://GameImage.png")
            await user_card._buffer_image()
            user_card.message = await interaction.response.edit_message(embed=user_card.embed_frame,
                                                                        view=user_card.view_frame,
                                                                        attachments=[user_card.image_file])
        else:
            print("Dashboard has nothing on it.")