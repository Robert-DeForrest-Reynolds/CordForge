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
    panel = await user_card.panel(border=True)
    await user_card.text("Hello", Vector2(5, 5), parent=panel)
    await user_card.add_button("Some other thing", some_other_card, [])


async def some_other_card(user_card:Card, interaction) -> None:
    await user_card.new_image()
    await user_card.add_button("Home", roc.home, [])
    await roc.reply(user_card, interaction)


roc = Cord("roc", entry)
# any necessary setup, loading images into memory, data management, etc.
roc.launch()
```

### Launch Bot
`cordforge bot_file.py token-key`
```bash
cordforge bot.py dev_name
```

### Next Steps

Now that you have a basic bot running, here are some ideas to expand it:

1. **Add more screens** - Create different sections for your bot
2. **Use containers** - Organize your UI with containers and borders
3. **Add images** - Use ListItem with images for richer content
4. **Create games** - Build simple games like tic-tac-toe or number guessing
5. **Add persistence** - Save user data to files or databases


### Version Control
Ensure your `Keys` file is hidden, here is a recommend .gitignore for example:
```
__pycache__
.venv
Keys
Data
```

# Troubleshooting

### Bot doesn't respond
- Check that your bot token is correct in the `Keys` file
- Make sure your bot is invited to the server with proper permissions
- Verify the bot is online (check the console output)

### Images don't appear
- Always call `await Bot.New_Image()` before adding components
- Make sure to call `await Bot.Reply(interaction)` to send the interface

### Buttons don't work
- Ensure your callback functions accept an `interaction` parameter
- Check that you're calling `await Bot.Reply(interaction)` in your callbacks

### Common Errors
- **"No image found"**: Call `await Bot.New_Image()` first
- **"Token not found"**: Check your `Keys` file format
- **"Invalid command"**: Make sure your bot prefix matches what you type

# Getting Help
- Look at the [Examples](EXAMPLES.md) for more complex use cases.
- Review the [API Reference](API_REFERENCE.md) for all available functionality.