Discord Bot Library - UI & Image Manipulation for Making Games

**Requires discord.py & Pillow**

**Will be a Python package on first full-release**

## Table of Contents
1. [Installation](#installation)
2. [Troubleshooting](#troubleshooting)
2. [Getting Help](#getting-help)


# Installation

### Prerequisites
- Python 3.13 or higher
- Discord Bot Token
- Discord.py 2.6.0 or higher
- Pillow 10.0.0 or higher

### Installing CordForge
*currently unsupported*
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
stuart~OTk3MDA...
```

### Basic Bot Setup
`bot.py`
```python
from CordForge import Cord

async def main_menu():
    """Your main dashboard function"""
    await Bot.New_Image()
    await Bot.Add_Button("Click Me!", button_callback, [])
    # Add more UI elements here

async def button_callback(interaction):
    """Handle button clicks"""
    await Bot.Reply(interaction)

# Create and start your bot
Bot = Cord("mybot", main_menu)
Bot.Start()
```

### Launch Bot
`cordforge bot_file.py token-key`
```bash
cordforge bot.py mybot
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
- Look at the [Examples](EXAMPLES.md) for more complex use cases
- Review the [API Reference](API_REFERENCE.md) for all available methods