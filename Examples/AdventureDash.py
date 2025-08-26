# my_dashboard_project.py
from CordForge import Cord, Colors

# --- Screen Builders ---
async def MainMenu():
    """Initial dashboard screen."""
    await Bot.New_Image()
    
    # Left container: Player info
    left = await Bot.Container(Width=Bot.XCenter, Height=Bot.ImageHeight)
    left.Border = True
    await Bot.Vertical_List(Parent=left, Items=[
        "Player Name: Alice",
        "Level: 12",
        "XP: 540 / 800"
    ])
    
    # Right container: Resources
    right = await Bot.Container(Width=Bot.XCenter, Height=Bot.ImageHeight, X=left.Width)
    right.Border = True
    await Bot.Vertical_List(Parent=right, Items=[
        "Gold: 420",
        "Food: 120",
        "Wood: 300"
    ])
    
    # Add action buttons
    await Bot.Add_Button("Inventory", ShowInventory, [])
    await Bot.Add_Button("Stats", ShowStats, [])

# Example secondary screen: Inventory
async def ShowInventory(Interaction):
    await Bot.New_Image()
    
    container = await Bot.Container(Width=Bot.ImageWidth, Height=Bot.ImageHeight)
    container.Border = True
    await Bot.Vertical_List(Parent=container, Items=[
        "Sword x1",
        "Shield x1",
        "Potion x5"
    ])
    
    # Return to main menu
    await Bot.Add_Button("Back", MainMenuCallback, [])
    
    await Bot.Reply(Interaction)

# Example secondary screen: Stats
async def ShowStats(Interaction):
    await Bot.New_Image()
    
    container = await Bot.Container(Width=Bot.ImageWidth, Height=Bot.ImageHeight)
    container.Border = True
    await Bot.Vertical_List(Parent=container, Items=[
        "Attack: 250",
        "Defense: 180",
        "Speed: 75"
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
