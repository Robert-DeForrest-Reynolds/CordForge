from .Cord import Cord
from .Vector2 import Vector2
from .ListItem import ListItem
from typing import Any
import asyncio
from .UI import *

# Get token, and run the bot
# Create images

async def Format_Numeric(_, Numeric: int | float) -> str:
    Suffixes = [
        (1_000_000_000_000_000, "Q"),
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    AbsValue = abs(Numeric)

    for Threshold, Suffix in Suffixes:
        if AbsValue >= Threshold:
            Value = Numeric / Threshold
            return f"{Value:.0f}{Suffix}" if Value.is_integer() else f"{Value:.1f}{Suffix}"
    return str(Numeric)