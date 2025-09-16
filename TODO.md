# Currently
 - Load necessary profiles so that user can have a development bot and server, and a official bot and server(s)
the profiles will need to hold:
 - servers
 - channels

 - profiles will be decided using the chosen key

# Components to Implements:
 - VerticalContainer
 - HorizontalContainer
 - Book (multi-page image)

# Features
 - Fields
 - Selection Menus
 - Modals
 - Slash Commands
 - Basic Role Management
 - Confirmation Dialogue
 - Toggle Buttons
 - Passwords
 - Date/Time Formatting
 - Logging


### Errors to Handle Gracefully

```python
from CordForge import *


async def Entry(User:Player) -> None:
    await RoC.New_Image()
    User.Health = 50
    await RoC.Sprite(X=50, Y=50, SpriteImage=PopulationImage)
    await RoC.Text(f"{User.Name}", Color=Color(15, 195, 195), Center=True)
    await RoC.Add_Button("Scavenge", Scavenge_Report, [])


async def Scavenge_Report(Interaction) -> None:
    await RoC.Add_Button("Scavenge", Scavenge_Report, [])
    await RoC.New_Image()
    LeftHand:Container = await RoC.Container(Width=RoC.XCenter, Height=RoC.Height)
    LeftHand.Border = True
    await RoC.List(Parent=LeftHand,
                   Items=[ListItem(Text="1,000,000,000,000"),
                          ListItem(Text="Offense"),
                          ListItem(Text="Defense")],
                   VerticalCenter=True)
    await RoC.Reply(Interaction)


RoC = Cord("RoC", Entry, Autosave=True)
PopulationImage = RoC.Load_Image("C:\\Users\\rldre\\Documents\\GitHub\\Project-RoC\\Assets\\Icons\\Population.png")
RoC.Start()
```
```bash
  File "C:\Users\rldre\Documents\GitHub\CordForge\CordForge\Cord.py", line 246, in Send_Dashboard_Command
    await _._Entry(User)
  File "C:\Users\rldre\Documents\GitHub\CordForge\Test.py", line 7, in Entry
    await RoC.Sprite(X=50, Y=50, Path=PopulationImage)
  File "C:\Users\rldre\Documents\GitHub\CordForge\CordForge\Cord.py", line 191, in Sprite
    NewSprite = Sprite(Cord=_, X=X, Y=Y, Parent=Parent, SpriteImage=SpriteImage, Path=Path)
  File "C:\Users\rldre\Documents\GitHub\CordForge\CordForge\Components\Sprite.py", line 15, in __init__
    _.SpriteImage = PillowImage.open(Path)
                    ~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Users\rldre\Documents\GitHub\CordForge\TestVenv\Lib\site-packages\PIL\Image.py", line 3524, in open
    prefix = fp.read(16)
             ^^^^^^^
AttributeError: 'PngImageFile' object has no attribute 'read'
```