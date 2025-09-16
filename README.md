Discord Bot Library for Writing Discord Bots with in Python 

A wrapper over discord.py and Pillow for bot management, image manipulation, easy data persistence, and more for making gameplay focused discord bots, but capable of making pretty much any kind of discord bot
Provides:
 - Image creation with a UI system, and sprite management
 - Out-of-the-box persistent data management for players with extensibility to handle anything
 - Various utilities for testing, and debugging to assist in development

## Table of Contents
1. [Installation](#installation)
2. [Troubleshooting](#troubleshooting)
2. [Getting Help](#getting-help)


# Installation
Requires Python 3.13+
discord.py
pillow

### Installing CordForge
```bash
py -m venv .venv
<activate venv>
pip install cordforge
```

Or install from source:
```bash
git clone https://github.com/Robert-DeForrest-Reynolds/CordForge
cd CordForge
py -m venv .venv
<activate venv>
pip install -e .
```

### Create Your Bot Token
First, create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications).

### Set Up Your Project
Create a `keys` file in your project directory:
`key_name~your_discord_bot_token_here`
```
dev_name=OTk3MDA...
```

Create a `settings` file in your project directory
```
Env=.venv/Scripts/python
Entry=bot.py
```

### Basic Bot Setup
`bot.py`
```python
from CordForge import *


# Initial send of dashboard, all other functions are replys/edits of the sent message
async def entry(user_card:Card) -> Card:
    await user_card.new_image()
    panel:Panel = await user_card.panel(border=True)
    await user_card.text("Hello", Vector2(5, 5), parent=panel)
    await user_card.add_button("Some other thing", some_other_card, [])


async def some_other_card(user_card:Card, interaction) -> None:
    await user_card.new_image()
    await user_card.add_button("Home", roc.home, [])
    await roc.reply(user_card, interaction)


bot = Cord(entry_command="cmd", entry=entry)
# any necessary setup, loading images into memory, data management, etc.
bot.launch()
```

### Launch & Use Bot
```bash
cordforge dev_name
```

Type `cmd` into the Discord server where Bot is a member.

Use `stop` to stop the bot completely.
Use `restart` to restart the Discord bot, implementing any changes in scripts.
Use `exit` to exit the launcher. The launcher will not let you exit with a running bot.
Use `//` to emergency stop the bot. Easy to type in cases of wild loops, or other problems.

### Player Data & Persistence
A players profile is created, and saved as soon as they use their first panel. You can add traits to their `Player` object, and they will automatically be saved and reloaded.

```python
from CordForge import *


# Initial send of dashboard, all other functions are replys/edits of the sent message
async def entry(user_card:Card) -> Card:
    await user_card.add_button(f"Money: {user_card.user.wallet}", give_money, [])


async def give_money(user_card:Card, interaction) -> None:
    user_card.user.wallet += 1
    await bot.home(user_card, interaction)


player_traits = [
    # [trait name, trait value]
    ["wallet", 0.00],
]
bot = Cord(entry_command="cmd",
           entry=entry,
           player_traits=player_traits)
bot.launch()
```

### More Information
Cord inherits from discord.py's `Bot` class, so you could add commands, cogs, and whatnot as you might normally.
The `Card` class `_.image` is a pillow image, and you can use all of it's variables, and functions.
Anything that CordForge can't do, can easily be implemented alongside it.

[Discord channel for any help](https://discord.gg/GGt4wZpujH)

### Version Control Recommendation
Ensure your `Keys` file is hidden, here is a recommend .gitignore for example:
```
__pycache__
.venv
Keys
Data
```