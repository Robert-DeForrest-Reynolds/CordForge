# CordForge API Reference

This document provides a comprehensive reference for all classes, methods, and properties in the CordForge library.

## Table of Contents

1. [Cord Class](#cord-class)
2. [Component Classes](#component-classes)
3. [Utility Classes](#utility-classes)
4. [Constants](#constants)
5. [Type Definitions](#type-definitions)

## Cord Class

The main bot class that extends discord.py's Bot class with image-based UI capabilities.

### Constructor

```python
Cord(DashboardAlias: str, Entry: Callable) -> Cord
```

**Parameters:**
- `DashboardAlias` (str): The command prefix for your bot (e.g., "!mybot")
- `Entry` (Callable): Async function that defines your main dashboard

**Example:**
```python
async def main_menu():
    await Bot.New_Image()
    await Bot.Add_Button("Start Game", start_game, [])

Bot = Cord("game", main_menu)
```

### Properties

#### Image Properties

```python
@property
def XCenter() -> int
```
Returns the horizontal center coordinate of the image.

```python
@property
def YCenter() -> int
```
Returns the vertical center coordinate of the image.

```python
@property
def ImageCenter() -> Vector2
```
Returns the center point of the image as a Vector2 object.

#### Configuration Properties

```python
Width: int = 640
```
The width of the generated images (default: 640).

```python
Height: int = 640
```
The height of the generated images (default: 640).

```python
DashboardBackground: tuple[int,int,int,int] = GRAY
```
The default background color for new images.

```python
InstanceUser: str
```
The user identifier for token lookup.

```python
SourceDirectory: str
```
The directory containing the bot's source files.

### Image Management Methods

#### New_Image()

```python
async def New_Image() -> None
```

Creates a new blank image with the default background color.

**Example:**
```python
async def create_screen():
    await Bot.New_Image()
    # Now you can add components to the image
```

#### Save_Image()

```python
async def Save_Image(Path: str = "CordImage") -> None
```

Saves the current image to a file.

**Parameters:**
- `Path` (str): The file path to save the image (without extension)

**Example:**
```python
await Bot.Save_Image("my_screenshot")
# Saves as "my_screenshot.PNG"
```

#### Buffer_Image()

```python
async def Buffer_Image() -> DiscordFile
```

Converts the current image to a Discord file for sending.

**Returns:**
- `DiscordFile`: A Discord file object containing the image

**Example:**
```python
image_file = await Bot.Buffer_Image()
# Use image_file in Discord interactions
```

### UI Component Methods

#### Container()

```python
async def Container(X: int = 0, Y: int = 0, Parent: Component = None, 
                   Width: int = 0, Height: int = 0, 
                   Background: tuple[int,int,int,int] = GRAY) -> Component
```

Creates a container component for organizing other UI elements.

**Parameters:**
- `X` (int): X coordinate relative to parent
- `Y` (int): Y coordinate relative to parent
- `Parent` (Component): Parent component (optional)
- `Width` (int): Container width
- `Height` (int): Container height
- `Background` (tuple): Background color (RGBA)

**Returns:**
- `Container`: A new container component

**Example:**
```python
container = await Bot.Container(
    X=50, Y=50,
    Width=300, Height=200,
    Background=(100, 100, 100, 255)
)
container.Border = True
```

#### Line()

```python
async def Line(X: int = 0, Y: int = 0, Parent: Component = None,
               Start: Vector2 = Vector2(0,0), End: Vector2 = Vector2(0,0),
               Color: tuple[int,int,int,int] = WHITE, Width: int = 1,
               Curve: bool = False) -> None
```

Draws a line on the image.

**Parameters:**
- `X` (int): X coordinate relative to parent
- `Y` (int): Y coordinate relative to parent
- `Parent` (Component): Parent component (optional)
- `Start` (Vector2): Starting point of the line
- `End` (Vector2): Ending point of the line
- `Color` (tuple): Line color (RGBA)
- `Width` (int): Line width in pixels
- `Curve` (bool): Whether to use curved line joints

**Example:**
```python
await Bot.Line(
    Start=Vector2(0, 0),
    End=Vector2(100, 100),
    Color=(255, 0, 0, 255),
    Width=3
)
```

#### List()

```python
async def List(X: int = 0, Y: int = 0, Parent: Component = None,
               Items: list[str:ListItem] = [], Font = None,
               Separation: int = 4, Horizontal: bool = False,
               VerticalCenter: bool = True, HorizontalCenter: bool = True) -> None
```

Creates a list component for displaying text items.

**Parameters:**
- `X` (int): X coordinate relative to parent
- `Y` (int): Y coordinate relative to parent
- `Parent` (Component): Parent component (optional)
- `Items` (list): List of strings or ListItem objects
- `Font` (ImageFont): Font for text rendering (optional)
- `Separation` (int): Spacing between items
- `Horizontal` (bool): Whether to arrange items horizontally
- `VerticalCenter` (bool): Whether to center items vertically
- `HorizontalCenter` (bool): Whether to center items horizontally

**Example:**
```python
await Bot.List(
    Parent=container,
    Items=["Item 1", "Item 2", "Item 3"],
    Separation=10,
    VerticalCenter=True
)
```

### Interactive Elements

#### Add_Button()

```python
async def Add_Button(Label: str, Callback: Callable, Arguments: list) -> None
```

Adds an interactive button to the interface.

**Parameters:**
- `Label` (str): Button text
- `Callback` (Callable): Function to call when button is clicked
- `Arguments` (list): Arguments to pass to the callback function

**Example:**
```python
async def button_handler(interaction, arg1, arg2):
    print(f"Button clicked with args: {arg1}, {arg2}")
    await Bot.Reply(interaction)

await Bot.Add_Button("Click Me", button_handler, ["hello", "world"])
```

#### Reply()

```python
async def Reply(Interaction: DiscordInteraction) -> None
```

Sends the current interface as a reply to an interaction.

**Parameters:**
- `Interaction` (DiscordInteraction): The Discord interaction to reply to

**Example:**
```python
async def handle_button_click(interaction):
    await Bot.New_Image()
    await Bot.List(Items=["Button was clicked!"])
    await Bot.Reply(interaction)
```

### Utility Methods

#### _() (Setup Helper)

```python
def _(Task, *Arguments) -> Any
```

Helper method for running async functions during setup.

**Parameters:**
- `Task` (Callable): The async function to run
- `*Arguments`: Arguments to pass to the function

**Example:**
```python
# Run async function during setup
result = Bot._(async_function, arg1, arg2)
```

#### Debug()

```python
async def Debug(VerticalCenter: bool = False, HorizontalCenter: bool = False) -> None
```

Draws debug lines to help with positioning.

**Parameters:**
- `VerticalCenter` (bool): Whether to draw vertical center line
- `HorizontalCenter` (bool): Whether to draw horizontal center line

**Example:**
```python
await Bot.Debug(VerticalCenter=True, HorizontalCenter=True)
# Draws crosshairs at the center of the image
```

#### Construct_Components()

```python
async def Construct_Components() -> None
```

Renders all image components to the main image.

**Note:** This is called automatically by `Reply()` and `Send_Dashboard_Command()`.

#### Construct_View()

```python
async def Construct_View() -> None
```

Creates the Discord view with all added buttons.

**Note:** This is called automatically by `Reply()` and `Send_Dashboard_Command()`.

### Bot Lifecycle Methods

#### setup_hook()

```python
async def setup_hook() -> None
```

Called during bot setup. Registers the dashboard command.

#### on_ready()

```python
async def on_ready() -> None
```

Called when the bot is ready and connected to Discord.

#### Start()

```python
def Start() -> None
```

Starts the bot with the configured token.

#### Send_Dashboard_Command()

```python
async def Send_Dashboard_Command(InitialContext: Context = None) -> None
```

Handles the dashboard command and displays the main interface.

**Parameters:**
- `InitialContext` (Context): The Discord command context

## Component Classes

### Component (Base Class)

The base class for all UI components.

#### Constructor

```python
Component(Cord, X: int = 0, Y: int = 0, Width: int = 0, Height: int = 0, 
          Parent: "Component" = None, Background: tuple[int,int,int,int] = GRAY)
```

#### Properties

```python
Width: int
Height: int
X: int
Y: int
Background: tuple[int,int,int,int]
Border: bool = False
BorderColor: tuple[int,int,int,int] = WHITE
BorderWidth: int = 1
Parent: "Component"
Children: list["Component"]
Image: PillowImage
Font: ImageFont
```

#### Methods

```python
@property
def XCenter() -> int
```
Returns the horizontal center of the component.

```python
@property
def YCenter() -> int
```
Returns the vertical center of the component.

```python
@property
def ImageCenter() -> Vector2
```
Returns the center point of the component as a Vector2.

```python
async def Draw() -> PillowImage
```
Abstract method that must be implemented by subclasses.

```python
async def Construct_Components() -> None
```
Renders all child components.

```python
async def Get_Text_Width(Text, Font = None) -> int
```
Calculates the width of text with the given font.

### Container Component

A rectangular container that can hold other components.

#### Constructor

```python
Container(Cord, X: int, Y: int, Width: int, Height: int, Parent, Background)
```

#### Methods

```python
async def Draw() -> PillowImage
```
Renders the container with its background, border, and children.

### List Component

Displays a list of text items with optional images.

#### Constructor

```python
List(Cord, X: int, Y: int, Parent: Component, Items: list[str], Font, 
     Separation: int, Horizontal: bool, VerticalCenter: bool, HorizontalCenter: bool)
```

#### Properties

```python
Items: list[str]
Separation: int
Horizontal: bool
VerticalCenter: bool
HorizontalCenter: bool
```

#### Methods

```python
async def Draw() -> PillowImage
```
Renders the list with all items, handling text centering and image placement.

### Line Component

Draws lines on the image.

#### Constructor

```python
Line(Cord, X, Y, Start: Vector2, End: Vector2, Parent: Component, 
     Width: int, Color: tuple[int,int,int,int], Curve: bool)
```

#### Properties

```python
Start: Vector2
End: Vector2
Width: int
Color: tuple[int,int,int,int]
Curve: bool
ImageWidth: int
ImageHeight: int
```

#### Methods

```python
async def Draw() -> PillowImage
```
Renders the line with the specified properties.

## Utility Classes

### Vector2

A utility class for 2D coordinates and vector operations.

#### Constructor

```python
Vector2(X: int = 0, Y: int = 0)
```

#### Properties

```python
X: int
Y: int
```

#### Methods

```python
def __add__(Other: "Vector2") -> "Vector2"
```
Vector addition.

```python
def __sub__(Other: "Vector2") -> "Vector2"
```
Vector subtraction.

```python
def __mul__(Value: int) -> "Vector2"
```
Scalar multiplication.

```python
def __floordiv__(Value: int) -> "Vector2"
```
Integer division.

```python
def __eq__(Other: object) -> bool
```
Equality comparison.

```python
def __iter__() -> iter
```
Iterator for unpacking coordinates.

```python
def __repr__() -> str
```
String representation.

```python
def Copy() -> "Vector2"
```
Creates a copy of the vector.

### ListItem

Represents an item in a list component.

#### Constructor

```python
ListItem(Text: str, Image: PillowImage = None, Separation: int = 4)
```

#### Properties

```python
Text: str
Image: PillowImage
Separation: int
```

## Constants

### Colors

```python
WHITE = (255, 255, 255, 255)
GRAY = (30, 30, 30, 255)
DEBUG_COLOR = (255, 0, 255, 255)
TRANSPRENCY = (0, 0, 0, 0)
```

## Type Definitions

### Color Tuple

```python
tuple[int, int, int, int]  # RGBA values (0-255)
```

### Component Types

```python
Component = Union[Container, List, Line]
```

### Font Type

```python
ImageFont  # PIL ImageFont object
```

### Image Type

```python
PillowImage  # PIL Image object
```

## Error Handling

### Common Exceptions

#### ValueError
- Raised when trying to save an image that hasn't been created
- Raised when invalid parameters are provided

#### TypeError
- Raised when Vector2 operations receive non-integer values
- Raised when callback functions don't accept the required parameters

#### RuntimeError
- Raised when trying to use `_()` method in an existing event loop

### Best Practices for Error Handling

```python
async def safe_callback(interaction):
    try:
        await Bot.New_Image()
        await Bot.List(Items=["Processing..."])
        await Bot.Reply(interaction)
    except Exception as e:
        print(f"Error in callback: {e}")
        # Handle error gracefully
```

## Performance Considerations

### Memory Management

- Images are automatically cleaned up after sending
- Use `Buffer_Image()` for temporary image operations
- Avoid storing large images in memory unnecessarily

### Component Optimization

- Limit the number of components per screen
- Reuse components when possible
- Use efficient data structures for game state

### Async Operations

- All UI operations are async and should be awaited
- Use `Bot._()` for setup operations only
- Avoid blocking operations in callbacks

---

This API reference covers all public methods and properties of the CordForge library. For additional examples and tutorials, see the main documentation.
