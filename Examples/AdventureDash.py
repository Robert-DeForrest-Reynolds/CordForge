# my_dashboard_project.py
from CordForge import *

# --- Screen Builders ---
async def MainMenu():
    """Initial dashboard screen."""
    await Bot.New_Image()
    
    # Left container: Player info
    left = await Bot.Container(Width=Bot.XCenter, Height=Bot.Height)
    left.Border = True
    await Bot.List(Parent=left, Items=[
        ListItem("Player Name: Alice"),
        ListItem("Level: 12"),
        ListItem("XP: 540 / 800")
    ])
    
    # Right container: Resources
    right = await Bot.Container(Width=Bot.XCenter, Height=Bot.Height, X=left.Width)
    right.Border = True
    await Bot.List(Parent=right, Items=[
        ListItem("Gold: 420"),
        ListItem("Food: 120"),
        ListItem("Wood: 300")
    ])
    
    # Add action buttons
    await Bot.Add_Button("Inventory", ShowInventory, [])
    await Bot.Add_Button("Stats", ShowStats, [])

# Example secondary screen: Inventory
async def ShowInventory(Interaction):
    await Bot.New_Image()
    
    container = await Bot.Container(Width=Bot.Width, Height=Bot.Height)
    container.Border = True
    await Bot.List(Parent=container, Items=[
        ListItem("Sword x1"),
        ListItem("Shield x1"),
        ListItem("Potion x5")
    ])
    
    # Return to main menu
    await Bot.Add_Button("Back", MainMenuCallback, [])
    
    await Bot.Reply(Interaction)

# Example secondary screen: Stats
async def ShowStats(Interaction):
    await Bot.New_Image()
    
    container = await Bot.Container(Width=Bot.Width, Height=Bot.Height)
    container.Border = True
    await Bot.List(Parent=container, Items=[
        ListItem("Attack: 250"),
        ListItem("Defense: 180"),
        ListItem("Speed: 75")
    ])
    
    # Return to main menu
    await Bot.Add_Button("Back", MainMenuCallback, [])
    
    await Bot.Reply(Interaction)

# Callback to return to main menu
async def MainMenuCallback(Interaction):
    await MainMenu()
    await Bot.Reply(Interaction)

# --- Bot Setup ---
Bot = Cord("AdventureDash", MainMenu)
Bot.Start()
