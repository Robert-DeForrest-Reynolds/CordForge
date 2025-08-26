# CordForge Examples Guide

This guide provides comprehensive examples of how to use CordForge for various types of Discord bot applications, from simple dashboards to complex games.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Game Examples](#game-examples)
3. [Dashboard Examples](#dashboard-examples)
4. [Interactive Examples](#interactive-examples)
5. [Advanced Examples](#advanced-examples)
6. [Pattern Examples](#pattern-examples)

## Basic Examples

### 1. Simple Hello World

```python
from CordForge import Cord

async def hello_world():
    await Bot.New_Image()
    await Bot.List(Items=["Hello, World!"])

Bot = Cord("hello", hello_world)
Bot.Start()
```

### 2. Basic Button Interaction

```python
from CordForge import Cord

async def main_screen():
    await Bot.New_Image()
    await Bot.List(Items=["Click the button below!"])
    await Bot.Add_Button("Click Me!", button_clicked, [])

async def button_clicked(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Button was clicked!"])
    await Bot.Add_Button("Go Back", main_screen, [])
    await Bot.Reply(interaction)

Bot = Cord("button", main_screen)
Bot.Start()
```

### 3. Simple Counter

```python
from CordForge import Cord

counter = 0

async def counter_screen():
    global counter
    await Bot.New_Image()
    await Bot.List(Items=[f"Count: {counter}"])
    await Bot.Add_Button("Increment", increment_counter, [])
    await Bot.Add_Button("Reset", reset_counter, [])

async def increment_counter(interaction):
    global counter
    counter += 1
    await counter_screen()
    await Bot.Reply(interaction)

async def reset_counter(interaction):
    global counter
    counter = 0
    await counter_screen()
    await Bot.Reply(interaction)

Bot = Cord("counter", counter_screen)
Bot.Start()
```

## Game Examples

### 4. Simple Tic-Tac-Toe

```python
from CordForge import Cord, Vector2

# Game state
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False

async def draw_board():
    await Bot.New_Image()
    
    # Draw grid lines
    for i in range(1, 3):
        # Vertical lines
        await Bot.Line(
            Start=Vector2(i * 200, 0),
            End=Vector2(i * 200, 600),
            Color=(255, 255, 255, 255),
            Width=3
        )
        # Horizontal lines
        await Bot.Line(
            Start=Vector2(0, i * 200),
            End=Vector2(600, i * 200),
            Color=(255, 255, 255, 255),
            Width=3
        )
    
    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                # Draw X
                x, y = col * 200 + 100, row * 200 + 100
                await Bot.Line(
                    Start=Vector2(x - 50, y - 50),
                    End=Vector2(x + 50, y + 50),
                    Color=(255, 0, 0, 255),
                    Width=5
                )
                await Bot.Line(
                    Start=Vector2(x + 50, y - 50),
                    End=Vector2(x - 50, y + 50),
                    Color=(255, 0, 0, 255),
                    Width=5
                )
            elif board[row][col] == "O":
                # Draw O (simplified as a line)
                x, y = col * 200 + 100, row * 200 + 100
                await Bot.Line(
                    Start=Vector2(x - 50, y),
                    End=Vector2(x + 50, y),
                    Color=(0, 0, 255, 255),
                    Width=10
                )
    
    # Add game info
    if not game_over:
        await Bot.List(
            Items=[f"Current Player: {current_player}"],
            X=10, Y=10
        )
    else:
        await Bot.List(
            Items=["Game Over!"],
            X=10, Y=10
        )

async def make_move(interaction, row, col):
    global board, current_player, game_over
    
    if game_over or board[row][col] != "":
        return
    
    board[row][col] = current_player
    
    # Check for winner
    if check_winner():
        game_over = True
    elif all(board[i][j] != "" for i in range(3) for j in range(3)):
        game_over = True
    else:
        current_player = "O" if current_player == "X" else "X"
    
    await draw_board()
    await Bot.Reply(interaction)

def check_winner():
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True
    
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True
    
    return False

async def reset_game(interaction):
    global board, current_player, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    await draw_board()
    await Bot.Reply(interaction)

# Create buttons for each cell
async def create_game_buttons():
    for row in range(3):
        for col in range(3):
            await Bot.Add_Button(
                f"{row},{col}",
                make_move,
                [row, col]
            )
    await Bot.Add_Button("Reset", reset_game, [])

async def game_screen():
    await draw_board()
    await create_game_buttons()

Bot = Cord("tictactoe", game_screen)
Bot.Start()
```

### 5. Simple RPG Character Sheet

```python
from CordForge import Cord, ListItem

class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.exp = 0
        self.exp_to_next = 100
        self.gold = 50
        self.inventory = ["Basic Sword", "Health Potion"]

character = Character("Hero")

async def character_sheet():
    await Bot.New_Image()
    
    # Create main container
    main_container = await Bot.Container(
        X=20, Y=20,
        Width=600, Height=600,
        Background=(40, 40, 40, 255)
    )
    main_container.Border = True
    main_container.BorderColor = (255, 255, 255, 255)
    
    # Character stats
    await Bot.List(
        Parent=main_container,
        Items=[
            f"Name: {character.name}",
            f"Level: {character.level}",
            f"HP: {character.hp}/{character.max_hp}",
            f"EXP: {character.exp}/{character.exp_to_next}",
            f"Gold: {character.gold}"
        ],
        X=20, Y=20,
        Separation=15
    )
    
    # Inventory section
    inventory_container = await Bot.Container(
        X=20, Y=200,
        Width=560, Height=200,
        Background=(60, 60, 60, 255),
        Parent=main_container
    )
    inventory_container.Border = True
    
    await Bot.List(
        Parent=inventory_container,
        Items=["Inventory:"] + character.inventory,
        X=10, Y=10,
        Separation=10
    )
    
    # Action buttons
    await Bot.Add_Button("Heal", heal_character, [])
    await Bot.Add_Button("Level Up", level_up, [])
    await Bot.Add_Button("Add Item", add_item, [])

async def heal_character(interaction):
    if character.gold >= 10:
        character.gold -= 10
        character.hp = min(character.max_hp, character.hp + 25)
        await character_sheet()
        await Bot.Reply(interaction)
    else:
        await Bot.New_Image()
        await Bot.List(Items=["Not enough gold! Need 10 gold to heal."])
        await Bot.Add_Button("Back", character_sheet, [])
        await Bot.Reply(interaction)

async def level_up(interaction):
    if character.exp >= character.exp_to_next:
        character.level += 1
        character.exp -= character.exp_to_next
        character.exp_to_next = int(character.exp_to_next * 1.5)
        character.max_hp += 20
        character.hp = character.max_hp
        await character_sheet()
        await Bot.Reply(interaction)
    else:
        await Bot.New_Image()
        await Bot.List(Items=["Not enough experience to level up!"])
        await Bot.Add_Button("Back", character_sheet, [])
        await Bot.Reply(interaction)

async def add_item(interaction):
    import random
    items = ["Magic Sword", "Shield", "Potion", "Scroll", "Ring"]
    new_item = random.choice(items)
    character.inventory.append(new_item)
    await character_sheet()
    await Bot.Reply(interaction)

Bot = Cord("rpg", character_sheet)
Bot.Start()
```

## Dashboard Examples

### 6. Server Statistics Dashboard

```python
from CordForge import Cord, Vector2

async def server_stats():
    await Bot.New_Image()
    
    # Header
    header_container = await Bot.Container(
        X=0, Y=0,
        Width=640, Height=100,
        Background=(50, 50, 50, 255)
    )
    header_container.Border = True
    
    await Bot.List(
        Parent=header_container,
        Items=["Server Statistics Dashboard"],
        X=20, Y=20,
        Separation=5
    )
    
    # Stats grid
    stats_container = await Bot.Container(
        X=20, Y=120,
        Width=600, Height=400,
        Background=(30, 30, 30, 255)
    )
    
    # Create stat boxes
    stat_boxes = [
        ("Members", "1,234"),
        ("Online", "567"),
        ("Channels", "25"),
        ("Roles", "15"),
        ("Messages Today", "2,847"),
        ("Active Users", "89")
    ]
    
    for i, (label, value) in enumerate(stat_boxes):
        row = i // 3
        col = i % 3
        
        box = await Bot.Container(
            X=col * 190 + 10,
            Y=row * 120 + 10,
            Width=180, Height=110,
            Background=(60, 60, 60, 255),
            Parent=stats_container
        )
        box.Border = True
        box.BorderColor = (100, 100, 100, 255)
        
        await Bot.List(
            Parent=box,
            Items=[label, value],
            X=10, Y=10,
            Separation=5
        )
    
    # Action buttons
    await Bot.Add_Button("Refresh", refresh_stats, [])
    await Bot.Add_Button("Export", export_stats, [])

async def refresh_stats(interaction):
    # Simulate refreshing stats
    await server_stats()
    await Bot.Reply(interaction)

async def export_stats(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Statistics exported to file!"])
    await Bot.Add_Button("Back", server_stats, [])
    await Bot.Reply(interaction)

Bot = Cord("stats", server_stats)
Bot.Start()
```

### 7. User Profile Dashboard

```python
from CordForge import Cord

class UserProfile:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.reputation = 0
        self.join_date = "2024-01-01"
        self.posts = 0
        self.achievements = ["First Post", "Helpful Member"]

user = UserProfile("DiscordUser")

async def profile_dashboard():
    await Bot.New_Image()
    
    # Profile header
    header = await Bot.Container(
        X=20, Y=20,
        Width=600, Height=120,
        Background=(70, 70, 70, 255)
    )
    header.Border = True
    
    await Bot.List(
        Parent=header,
        Items=[
            f"Username: {user.username}",
            f"Level: {user.level}",
            f"Reputation: {user.reputation}"
        ],
        X=20, Y=20,
        Separation=10
    )
    
    # Stats section
    stats = await Bot.Container(
        X=20, Y=160,
        Width=290, Height=200,
        Background=(50, 50, 50, 255),
        Parent=None
    )
    stats.Border = True
    
    await Bot.List(
        Parent=stats,
        Items=[
            "Statistics:",
            f"Join Date: {user.join_date}",
            f"Total Posts: {user.posts}",
            f"Member for: 30 days"
        ],
        X=20, Y=20,
        Separation=8
    )
    
    # Achievements section
    achievements = await Bot.Container(
        X=330, Y=160,
        Width=290, Height=200,
        Background=(50, 50, 50, 255),
        Parent=None
    )
    achievements.Border = True
    
    await Bot.List(
        Parent=achievements,
        Items=["Achievements:"] + user.achievements,
        X=20, Y=20,
        Separation=8
    )
    
    # Action buttons
    await Bot.Add_Button("Edit Profile", edit_profile, [])
    await Bot.Add_Button("View Posts", view_posts, [])
    await Bot.Add_Button("Settings", settings, [])

async def edit_profile(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Profile editing not implemented yet."])
    await Bot.Add_Button("Back", profile_dashboard, [])
    await Bot.Reply(interaction)

async def view_posts(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Recent Posts:", "Post 1: Hello World", "Post 2: How are you?"])
    await Bot.Add_Button("Back", profile_dashboard, [])
    await Bot.Reply(interaction)

async def settings(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Settings:", "Notifications: ON", "Privacy: Public", "Theme: Dark"])
    await Bot.Add_Button("Back", profile_dashboard, [])
    await Bot.Reply(interaction)

Bot = Cord("profile", profile_dashboard)
Bot.Start()
```

## Interactive Examples

### 8. Poll/Voting System

```python
from CordForge import Cord

class Poll:
    def __init__(self, question, options):
        self.question = question
        self.options = options
        self.votes = {option: 0 for option in options}
        self.voters = set()

poll = Poll("What's your favorite color?", ["Red", "Blue", "Green", "Yellow"])

async def poll_dashboard():
    await Bot.New_Image()
    
    # Question
    question_container = await Bot.Container(
        X=20, Y=20,
        Width=600, Height=80,
        Background=(60, 60, 60, 255)
    )
    question_container.Border = True
    
    await Bot.List(
        Parent=question_container,
        Items=[f"Poll: {poll.question}"],
        X=20, Y=20,
        Separation=5
    )
    
    # Results
    results_container = await Bot.Container(
        X=20, Y=120,
        Width=600, Height=400,
        Background=(40, 40, 40, 255)
    )
    
    total_votes = sum(poll.votes.values())
    
    for i, option in enumerate(poll.options):
        votes = poll.votes[option]
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        
        option_container = await Bot.Container(
            X=20, Y=i * 80 + 20,
            Width=560, Height=60,
            Background=(50, 50, 50, 255),
            Parent=results_container
        )
        option_container.Border = True
        
        await Bot.List(
            Parent=option_container,
            Items=[f"{option}: {votes} votes ({percentage:.1f}%)"],
            X=20, Y=15,
            Separation=5
        )
    
    # Vote buttons
    for option in poll.options:
        await Bot.Add_Button(f"Vote {option}", vote, [option])
    
    await Bot.Add_Button("Reset Poll", reset_poll, [])

async def vote(interaction, option):
    # In a real implementation, you'd check the user ID
    user_id = str(interaction.user.id)
    
    if user_id in poll.voters:
        await Bot.New_Image()
        await Bot.List(Items=["You have already voted!"])
        await Bot.Add_Button("Back", poll_dashboard, [])
        await Bot.Reply(interaction)
        return
    
    poll.votes[option] += 1
    poll.voters.add(user_id)
    
    await poll_dashboard()
    await Bot.Reply(interaction)

async def reset_poll(interaction):
    poll.votes = {option: 0 for option in poll.options}
    poll.voters.clear()
    await poll_dashboard()
    await Bot.Reply(interaction)

Bot = Cord("poll", poll_dashboard)
Bot.Start()
```

### 9. Simple Calculator

```python
from CordForge import Cord

class Calculator:
    def __init__(self):
        self.display = "0"
        self.memory = 0
        self.operation = None
        self.new_number = True

calc = Calculator()

async def calculator_interface():
    await Bot.New_Image()
    
    # Display
    display_container = await Bot.Container(
        X=20, Y=20,
        Width=600, Height=80,
        Background=(20, 20, 20, 255)
    )
    display_container.Border = True
    display_container.BorderColor = (100, 100, 100, 255)
    
    await Bot.List(
        Parent=display_container,
        Items=[calc.display],
        X=20, Y=20,
        Separation=5
    )
    
    # Number buttons
    numbers = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["0", ".", "C"]
    ]
    
    for row_idx, row in enumerate(numbers):
        for col_idx, num in enumerate(row):
            x = 20 + col_idx * 150
            y = 120 + row_idx * 80
            
            if num == "C":
                await Bot.Add_Button(num, clear_calculator, [])
            else:
                await Bot.Add_Button(num, press_number, [num])
    
    # Operation buttons
    operations = ["+", "-", "*", "/", "="]
    for i, op in enumerate(operations):
        await Bot.Add_Button(op, press_operation, [op])

async def press_number(interaction, number):
    if calc.new_number:
        calc.display = number
        calc.new_number = False
    else:
        if number == "." and "." not in calc.display:
            calc.display += number
        elif number != ".":
            calc.display += number
    
    await calculator_interface()
    await Bot.Reply(interaction)

async def press_operation(interaction, operation):
    if operation == "=":
        try:
            if calc.operation:
                expression = f"{calc.memory}{calc.operation}{calc.display}"
                calc.display = str(eval(expression))
                calc.operation = None
                calc.memory = 0
        except:
            calc.display = "Error"
    else:
        calc.memory = float(calc.display)
        calc.operation = operation
        calc.new_number = True
    
    await calculator_interface()
    await Bot.Reply(interaction)

async def clear_calculator(interaction):
    calc.display = "0"
    calc.memory = 0
    calc.operation = None
    calc.new_number = True
    await calculator_interface()
    await Bot.Reply(interaction)

Bot = Cord("calc", calculator_interface)
Bot.Start()
```

## Advanced Examples

### 10. Multi-Screen Navigation System

```python
from CordForge import Cord

class NavigationSystem:
    def __init__(self):
        self.current_screen = "main"
        self.screen_history = []
        self.user_data = {
            "name": "User",
            "preferences": {},
            "saved_data": []
        }

nav = NavigationSystem()

async def main_menu():
    nav.current_screen = "main"
    await Bot.New_Image()
    
    # Welcome message
    welcome_container = await Bot.Container(
        X=20, Y=20,
        Width=600, Height=100,
        Background=(60, 60, 60, 255)
    )
    welcome_container.Border = True
    
    await Bot.List(
        Parent=welcome_container,
        Items=[f"Welcome, {nav.user_data['name']}!", "Select an option below:"],
        X=20, Y=20,
        Separation=10
    )
    
    # Menu options
    await Bot.Add_Button("Profile", navigate_to, ["profile"])
    await Bot.Add_Button("Settings", navigate_to, ["settings"])
    await Bot.Add_Button("Games", navigate_to, ["games"])
    await Bot.Add_Button("Help", navigate_to, ["help"])

async def profile_screen():
    nav.current_screen = "profile"
    await Bot.New_Image()
    
    await Bot.List(Items=[
        "Profile Screen",
        f"Name: {nav.user_data['name']}",
        "Edit your profile information"
    ])
    
    await Bot.Add_Button("Edit Name", edit_name, [])
    await Bot.Add_Button("Back", navigate_to, ["main"])

async def settings_screen():
    nav.current_screen = "settings"
    await Bot.New_Image()
    
    await Bot.List(Items=[
        "Settings Screen",
        "Configure your preferences",
        "Theme: Dark",
        "Notifications: ON"
    ])
    
    await Bot.Add_Button("Toggle Theme", toggle_theme, [])
    await Bot.Add_Button("Back", navigate_to, ["main"])

async def games_screen():
    nav.current_screen = "games"
    await Bot.New_Image()
    
    await Bot.List(Items=[
        "Games Menu",
        "Available games:",
        "1. Tic-Tac-Toe",
        "2. Calculator",
        "3. Poll System"
    ])
    
    await Bot.Add_Button("Tic-Tac-Toe", navigate_to, ["tictactoe"])
    await Bot.Add_Button("Calculator", navigate_to, ["calculator"])
    await Bot.Add_Button("Back", navigate_to, ["main"])

async def help_screen():
    nav.current_screen = "help"
    await Bot.New_Image()
    
    await Bot.List(Items=[
        "Help & Support",
        "How to use this bot:",
        "1. Use buttons to navigate",
        "2. Each screen has different features",
        "3. Use 'Back' to return to previous screen"
    ])
    
    await Bot.Add_Button("Back", navigate_to, ["main"])

async def navigate_to(interaction, screen):
    nav.screen_history.append(nav.current_screen)
    
    if screen == "main":
        await main_menu()
    elif screen == "profile":
        await profile_screen()
    elif screen == "settings":
        await settings_screen()
    elif screen == "games":
        await games_screen()
    elif screen == "help":
        await help_screen()
    elif screen == "tictactoe":
        await tictactoe_screen()
    elif screen == "calculator":
        await calculator_screen()
    
    await Bot.Reply(interaction)

async def edit_name(interaction):
    # In a real implementation, you'd prompt for input
    nav.user_data['name'] = "Updated User"
    await profile_screen()
    await Bot.Reply(interaction)

async def toggle_theme(interaction):
    # Simulate theme toggle
    await Bot.New_Image()
    await Bot.List(Items=["Theme toggled! (This would change the UI colors)"])
    await Bot.Add_Button("Back", navigate_to, ["settings"])
    await Bot.Reply(interaction)

async def tictactoe_screen(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Tic-Tac-Toe game would start here..."])
    await Bot.Add_Button("Back", navigate_to, ["games"])
    await Bot.Reply(interaction)

async def calculator_screen(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Calculator would start here..."])
    await Bot.Add_Button("Back", navigate_to, ["games"])
    await Bot.Reply(interaction)

Bot = Cord("nav", main_menu)
Bot.Start()
```

## Pattern Examples

### 11. State Management Pattern

```python
from CordForge import Cord
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppState:
    current_screen: str = "main"
    user_data: Dict[str, Any] = None
    game_state: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.user_data is None:
            self.user_data = {}
        if self.game_state is None:
            self.game_state = {}

# Global state
state = AppState()

class StateManager:
    @staticmethod
    def update_screen(new_screen: str):
        state.current_screen = new_screen
    
    @staticmethod
    def update_user_data(key: str, value: Any):
        state.user_data[key] = value
    
    @staticmethod
    def update_game_state(key: str, value: Any):
        state.game_state[key] = value
    
    @staticmethod
    def get_screen() -> str:
        return state.current_screen
    
    @staticmethod
    def get_user_data(key: str, default=None):
        return state.user_data.get(key, default)
    
    @staticmethod
    def get_game_state(key: str, default=None):
        return state.game_state.get(key, default)

# Screen functions
async def main_screen():
    StateManager.update_screen("main")
    await Bot.New_Image()
    
    username = StateManager.get_user_data("username", "Guest")
    score = StateManager.get_user_data("score", 0)
    
    await Bot.List(Items=[
        f"Welcome, {username}!",
        f"Your score: {score}",
        "Select an option:"
    ])
    
    await Bot.Add_Button("Play Game", play_game, [])
    await Bot.Add_Button("Settings", settings_screen, [])

async def play_game(interaction):
    StateManager.update_screen("game")
    StateManager.update_game_state("level", 1)
    StateManager.update_game_state("lives", 3)
    
    await Bot.New_Image()
    
    level = StateManager.get_game_state("level")
    lives = StateManager.get_game_state("lives")
    
    await Bot.List(Items=[
        f"Level: {level}",
        f"Lives: {lives}",
        "Game in progress..."
    ])
    
    await Bot.Add_Button("Next Level", next_level, [])
    await Bot.Add_Button("Main Menu", main_screen, [])
    await Bot.Reply(interaction)

async def next_level(interaction):
    current_level = StateManager.get_game_state("level")
    StateManager.update_game_state("level", current_level + 1)
    
    # Update user score
    current_score = StateManager.get_user_data("score", 0)
    StateManager.update_user_data("score", current_score + 100)
    
    await play_game(interaction)

async def settings_screen(interaction):
    StateManager.update_screen("settings")
    await Bot.New_Image()
    
    await Bot.List(Items=[
        "Settings",
        "Configure your preferences"
    ])
    
    await Bot.Add_Button("Change Username", change_username, [])
    await Bot.Add_Button("Main Menu", main_screen, [])
    await Bot.Reply(interaction)

async def change_username(interaction):
    # Simulate username change
    StateManager.update_user_data("username", "NewUser")
    await settings_screen(interaction)

Bot = Cord("state", main_screen)
Bot.Start()
```

### 12. Component Factory Pattern

```python
from CordForge import Cord
from typing import List, Dict, Any

class ComponentFactory:
    @staticmethod
    async def create_header(title: str, subtitle: str = None):
        container = await Bot.Container(
            X=20, Y=20,
            Width=600, Height=80,
            Background=(60, 60, 60, 255)
        )
        container.Border = True
        
        items = [title]
        if subtitle:
            items.append(subtitle)
        
        await Bot.List(
            Parent=container,
            Items=items,
            X=20, Y=20,
            Separation=5
        )
        return container
    
    @staticmethod
    async def create_info_panel(items: List[str], title: str = "Information"):
        container = await Bot.Container(
            X=20, Y=120,
            Width=600, Height=200,
            Background=(40, 40, 40, 255)
        )
        container.Border = True
        
        await Bot.List(
            Parent=container,
            Items=[title] + items,
            X=20, Y=20,
            Separation=8
        )
        return container
    
    @staticmethod
    async def create_button_grid(buttons: List[Dict[str, Any]]):
        """Create a grid of buttons from a list of button definitions"""
        for button in buttons:
            await Bot.Add_Button(
                button["label"],
                button["callback"],
                button.get("args", [])
            )

# Example usage
async def factory_example():
    await Bot.New_Image()
    
    # Create header
    await ComponentFactory.create_header(
        "Component Factory Example",
        "Demonstrating reusable components"
    )
    
    # Create info panel
    await ComponentFactory.create_info_panel([
        "This screen uses the factory pattern",
        "Components are created by factory methods",
        "Makes code more modular and reusable"
    ])
    
    # Create button grid
    buttons = [
        {
            "label": "Action 1",
            "callback": action_one,
            "args": []
        },
        {
            "label": "Action 2", 
            "callback": action_two,
            "args": ["param1"]
        },
        {
            "label": "Back",
            "callback": go_back,
            "args": []
        }
    ]
    
    await ComponentFactory.create_button_grid(buttons)

async def action_one(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Action 1 executed!"])
    await Bot.Add_Button("Back", factory_example, [])
    await Bot.Reply(interaction)

async def action_two(interaction, param):
    await Bot.New_Image()
    await Bot.List(Items=[f"Action 2 executed with parameter: {param}"])
    await Bot.Add_Button("Back", factory_example, [])
    await Bot.Reply(interaction)

async def go_back(interaction):
    await factory_example()
    await Bot.Reply(interaction)

Bot = Cord("factory", factory_example)
Bot.Start()
```

---

These examples demonstrate various patterns and use cases for CordForge. You can use these as starting points and adapt them to your specific needs. Remember to:

1. **Handle errors gracefully** - Always wrap your callbacks in try-catch blocks
2. **Manage state properly** - Use classes or data structures to maintain application state
3. **Keep components modular** - Create reusable functions for common UI patterns
4. **Test thoroughly** - Test your bot with different user interactions
5. **Document your code** - Add comments and docstrings to explain complex logic

For more advanced examples and patterns, check the main documentation and API reference.
