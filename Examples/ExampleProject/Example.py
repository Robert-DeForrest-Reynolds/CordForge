from CordForge import *


async def Entry() -> None:
    await Example.Add_Button(Label="Example Button", Callback=Report, Arguments=[])
    await Example.New_Image()


async def Report(Interaction) -> None:
    await Example.Add_Button(Label="Example Button", Callback=Report, Arguments=[])
    await Example.New_Image()
    LeftHand:Panel = await Example.Container(Width=Example.XCenter, Height=Example.Height)
    LeftHand.Border = True
    await Example.display(Parent=LeftHand,
                   Items=[DisplayItem(Text="Health"),
                          DisplayItem(Text="Level"),],
                   VerticalCenter=True)
    await Example.reply(Interaction)


Example = Cord("Example", Entry)
Example.Start()