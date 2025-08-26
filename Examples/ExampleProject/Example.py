from CordForge import *


async def Entry() -> None:
    await Example.Add_Button(Label="Example Button", Callback=Report, Arguments=[])
    await Example.New_Image()


async def Report(Interaction) -> None:
    await Example.Add_Button(Label="Example Button", Callback=Report, Arguments=[])
    await Example.New_Image()
    LeftHand:Container = await Example.Container(Width=Example.XCenter, Height=Example.Height)
    LeftHand.Border = True
    await Example.List(Parent=LeftHand,
                   Items=[ListItem(Text="Health"),
                          ListItem(Text="Level"),],
                   VerticalCenter=True)
    await Example.Reply(Interaction)


Example = Cord("Example", Entry)
Example.Start()