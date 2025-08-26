Discord Bot Library - UI & Image Manipulation for Making Games

**Requires discord.py & Pillow**
**Will be a Python package on first full-release**

Save your tokens to a file named `Keys` within the same folder as your bot. Pro tip: make sure your key is hidden from whatever version control you may be using. All keys are read in as lower case by the launcher. Example `Keys` file:
```
stuart stuart's_token
marie marie's_token
official official_token
```

Very minimal example:
```python
from CordForge import *

async def Entry() -> None:
    await Bot.Add_Button(Label="Some Action", Callback=Some_Action, Arguments=[])
    await Bot.New_Image()

async def Some_Action(Interaction) -> None:
    await Bot.Reply(Interaction)

Bot = Cord("cmd", Entry)
Bot.Start()
```


### Important Things to Document
`_` could also be thought of as `setup`, function that runs async functions during setup
