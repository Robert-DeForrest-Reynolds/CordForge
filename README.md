Discord Bot Library - UI & Image Manipulation for Making Games
Essentially just a wrapper over discord.py and Pillow to make life a little easier for image-based, and gameplay focused Discord bots.
Provides:
 - Image creation with a UI system, and sprite management
 - Out-of-the-box persistent data management for players with extensibility to handle anything
 - Various utilities for testing, and debugging to assist in development

## Table of Contents
1. [Installation](#installation)
2. [Troubleshooting](#troubleshooting)
2. [Getting Help](#getting-help)


# Installation

### Installing CordForge
```bash
pip install cordforge
```

Or install from source:
```bash
git clone https://github.com/Robert-DeForrest-Reynolds/CordForge
cd CordForge
pip install -e .
```

### Create Your Bot Token
First, create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications).

### Set Up Your Project
Create a `Keys` file in your project directory:
`key_name~your_discord_bot_token_here`
```
dev_name=OTk3MDA...
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

### Launch Bot
`cordforge bot_file.py token-key`
```bash
cordforge bot.py dev_name
```


### Version Control
Ensure your `Keys` file is hidden, here is a recommend .gitignore for example:
```
__pycache__
.venv
Keys
Data
```

# Getting Help
- Look at the [Examples](EXAMPLES.md) for more complex use cases.
- Review the [API Reference](API_REFERENCE.md) for all available functionality.