from os.path import join
from PIL import Image
from discord.enums import ChannelType
from discord import ButtonStyle, Embed, Intents, Member, Interaction, Message, TextChannel, VoiceChannel
from discord.abc import GuildChannel
from discord.ext.commands import Command, Bot, Context
from sys import argv, path, stdin, stdout, stderr
from itertools import product
from asyncio import get_running_loop, run
from typing import Callable, Any
import threading

from .card import Card
from .object import Object
from .user import User
from .data import Data
from .font import Font

import logging

class Cord(Bot):
    def __init__(_, entry_command: str = None, autosave: bool = True) -> None:
        _.logger = logging.getLogger("CordForge")
        _.logger.setLevel(logging.DEBUG)  # or INFO
        if not _.logger.hasHandlers():
            handler = logging.StreamHandler()  # default to stdout
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
            handler.setFormatter(formatter)
            _.logger.addHandler(handler)
        _.entry_command = entry_command
        _.entry:Callable = None
        _.setup:Callable = None
        _.autosave = autosave
        _.source_directory = path[0]
        _.instance_user:str = argv[1]
        _.user_traits:list[list[str, Any]] = []
        _.user_profiles = {}
        _.message:Message = None
        _.font:Font = None
        _.objects:dict[str:Object] = {}
        _.data = Data(_)

        _._handle_alias() # required before handing _.prefix to Bot.__init__()
        super().__init__(command_prefix=_.prefix, intents=Intents.all())
        threading.Thread(target=_.sync_stdin_listener, args=(), daemon=True).start()
        

    def __setattr__(_, name, value):
        return super().__setattr__(name, value)


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

            
    def sync_stdin_listener(_):
        _.logger.info("Listening for input from launcher...")
        for line in stdin:
            line = line.strip()
            _.logger.info(f"Input: {line}")
        

    def run_task(_, Task, *Arguments) -> Any:
        try: get_running_loop()
        except RuntimeError: return run(Task(*Arguments))
        raise RuntimeError("There is an existing loop. Run() is only used for setup before the Bot runs it's loop.")


    async def setup_hook(_):
        async def wrapper(initial_context): await _._send_initial_card(initial_context)
        _.add_command(Command(wrapper, aliases=_.entry_command))
        await super().setup_hook()


    async def on_ready(_):
        _.logger.info("Bot is alive, and ready")

        _.logger.info("Setting up...")
        _._setup_user_traits()
        if _.setup: await _.setup()
        _.logger.info("Finished setup")
        
        await _.data.load_data()
        if _.autosave: await _.data.autosave()


    async def _send_initial_card(_, initial_context:Context) -> None:
        user:User = User(initial_context.author)
        user_card:Card = await _.new_card(user)

        try:
            await _.entry(user_card)
        except Exception as e:
            _.logger.info(f"Exception: {e}")

        if user.id not in _.user_profiles.keys():
            _.user_profiles.update({user.id:user})

        await initial_context.message.delete()

        # this needs to be fixed, only handles a single player currently
        if _.message is not None: await _.message.delete()

        await user_card._construct()
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
            _.logger.info("Dashboard has nothing on it.")



    def launch(_, entry:Callable, setup:Callable=None) -> None:
        'Start Discord Bot'
        _.logger.info("Launching...")
        _.entry = entry
        _.setup = setup
        _.run(_._get_token(_.instance_user))


    def determine(_, dictionary:dict, callable:Callable=None) -> Any:
        '''
        Uses the chosen key to determine which dictonary item is selected,\
        can optionally provide callback to is on determine.
        '''
        selection = dictionary[_.instance_user]
        if callable:
            selection = callable(selection)
        return selection


    async def announce(_, channel:GuildChannel, message:str=None, card:Card=None) -> Message:
        'Send a message, or Card to a specific channel'
        if channel.type != ChannelType.text:_.logger.info("announce() is only compatible with TextChannels")
        else:\
        channel:TextChannel = channel
        if message and not card:
            await channel.send(message)
        elif message and card:
            card.embed_frame = Embed(title="")
            card.embed_frame.set_image(url="attachment://GameImage.png")
            await card._construct()
            await card._buffer_image()
            await channel.send(message, embed=card.embed_frame,
                               view=card.view_frame,
                               file=card.image_file)
            

    async def new_card(_, user:Member=None) -> Card:
        '''
        Create new card to draw on.

        Returns instantiated Card
        '''
        user_card:Card = Card(user)
        return user_card


    def load_image(_, image_path:str) -> Image:
        'Load image from file path into memory'
        return Image.open(image_path)


    async def reply(_, user_card:Card, interaction:Interaction) -> None:
        'Send a card to a user as a result of an interaction'
        await user_card._construct()
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
            _.logger.info("Dashboard has nothing on it.")


    async def home(_, user_card:Card, interaction:Interaction) -> None:
        'Brings the user back to the entry() function card'
        try:
            await _.entry(user_card)
        except Exception as e:
            _.logger.info(f"Exception: {e}")

        await user_card._construct()
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
            _.logger.info("Dashboard has nothing on it.")