# Generalized imports for dev utility
from PIL import Image
from discord import Interaction, Message
from discord.ext.commands import Context
from discord.abc import GuildChannel
from asyncio import sleep, create_task
from asyncio import run as run_async

# CordForge specific
from .cord import Cord
from .card import Card
from .object import Object
from .vector2 import Vector2
from .colors import *
from .font import Font
from .components import *
from .utilities import *
from .user import User
from .data import Data

from sys import stdout

import logging

logging.basicConfig(
    level=logging.INFO,
    stream=stdout, # force everything to stdout
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s"
)