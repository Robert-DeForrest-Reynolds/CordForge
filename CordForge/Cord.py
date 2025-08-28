from os import mkdir, listdir
from os.path import join, exists
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord import File as DiscordFile
from discord import Message as DiscordMessage
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle, Embed, Intents, Member
from discord.ext.commands import Command
from discord.ui import Button, View
from discord.ext.commands import Bot, Context
from sys import argv, path
from itertools import product
from typing import Callable, Any
from .Vector2 import Vector2
from .ListItem import ListItem
from .UI import *
from .Colors import *
import asyncio


class Cord(Bot):
    Message:DiscordMessage
    def __init__(_, DashboardAlias:str, Entry) -> None:
        _.DashboardAlias = DashboardAlias
        _._Handle_Alias()
        _.SourceDirectory = path[0]
        _.InstanceUser:str = argv[1]
        _.BaseViewFrame = None
        _.EmbedFrame = None
        _.Image = None
        _.ImageComponents = []
        _.ImageFile = None
        _.ViewContent = []
        _.EmbedContent = []
        _.Message = None
        _.DashboardBackground = GRAY
        _.Height = 640
        _.Width = 640
        _._Entry = Entry
        print("Discord Bot Initializing")
        super().__init__(command_prefix=_.Prefix, intents=Intents.all())


    @property
    def XCenter(_): return _.Width // 2
    @property
    def YCenter(_): return _.Height // 2
    @property
    def ImageCenter(_): return Vector2(_.XCenter, _.YCenter)


    # This is a "pre-run async" hook essentially
    # For running setup functions before the Bot starts it's loop
    # This makes it so the user can make their async functions reusable for setup, and runtime
    # And to use built-in async functions before the Bot's running loop
    # Like testing images outside of discord
    def _(_, Task, *Arguments) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(Task(*Arguments))
        raise RuntimeError("There is an existing loop.\n" \
                        "Await() is used for setup before the Bot runs it's loop.")


    def _Handle_Alias(_) -> None:
        _.Prefix = [_.DashboardAlias[0]]
        for Prefix in _.Prefix.copy():
            _.Prefix.extend([Variant for Variant in _._All_Case_Variants(Prefix, _.Prefix)\
                                        if Variant not in _.Prefix])
        _.DashboardAlias = [_.DashboardAlias[1:]]
        for Alias in _.DashboardAlias.copy():
            _.DashboardAlias.extend([Variant for Variant in _._All_Case_Variants(Alias, _.DashboardAlias)\
                                        if Variant not in _.DashboardAlias])


    def _All_Case_Variants(_, String: str, Originals:list[str]):
        Pools = [(Character.lower(), Character.upper()) for Character in String]
        Variants = []
        for Variant in product(*Pools):
            String = ''.join(Variant)
            if String not in Originals: Variants.append(String)
        return Variants


    def _Get_Token(_, Key:str) -> str:
        with open(join(_.SourceDirectory, "Keys")) as KeyFile:
            for Line in KeyFile:
                LineData = Line.split("=")
                if Key.lower() == LineData[0].lower():
                    return LineData[1].strip()
        return "Could Not Find Token"


    async def setup_hook(_):
        print(_.commands)
        async def Wrapper(Context): await _.Send_Dashboard_Command(Context)
        _.add_command(Command(Wrapper, aliases=_.DashboardAlias))
        await super().setup_hook()


    async def on_ready(_) -> None:
        print("Bot is alive.\n")


    def Start(_) -> None: _.run(_._Get_Token(_.InstanceUser))


    async def New_Image(_) -> None:
        _.Image = Image.new("RGBA",
                            (_.Height, _.Width),
                            color=_.DashboardBackground)


    async def Send_Image(_, Interaction:DiscordInteraction, ImagePath:str) -> None:
        _.ImageFile = DiscordFile(ImagePath, filename="GameImage.png")
        await _.Reply(Interaction)
    

    async def Save_Image(_, Path:str="CordImage") -> None:
        if not hasattr(_, "Image") or _.Image is None:
            raise ValueError("No image found. Did you run Create_Image first?")
        _.Image.save(Path + ".PNG", format="PNG")
    
    
    async def Buffer_Image(_) -> DiscordFile:
        Buffer = BytesIO()
        _.Image.save(Buffer, format="PNG")
        Buffer.seek(0)
        _.ImageFile = DiscordFile(Buffer, filename="GameImage.png")
        Buffer.close()
        return _.ImageFile
    

    async def Container(_, X:int=0, Y:int=0, Parent=None, Width:int=0, Height:int=0,  Background:tuple[int,int,int,int]=GRAY) -> Component:
        NewContainer = Container(Cord=_, X=X, Y=Y, Parent=Parent, Width=Width, Height=Height, Background=Background)
        _.ImageComponents.append(NewContainer)
        return NewContainer


    async def Line(_, X:int=0, Y:int=0, Parent:Component=None,
                   Start:Vector2=Vector2(0,0), End:Vector2=Vector2(0,0),
                   Color:tuple[int,int,int,int]=WHITE, Width:int=1,
                   Curve:bool=False) -> None:
        NewLine = Line(Cord=_, X=X, Y=Y, Parent=Parent, Start=Start, End=End, Width=Width, Color=Color, Curve=Curve)
        if Parent == None:
            _.ImageComponents.append(NewLine)
        else:
            Parent.Children.append(NewLine)


    async def List(_, X:int=0, Y:int=0, Parent:Component=None,
                   Items:list[str:ListItem] = [], Font=None,
                   Separation:int=4, Horizontal:bool=False,
                   VerticalCenter:bool=True, HorizontalCenter:bool=True) -> None:
        NewList = List(Cord=_, X=X, Y=Y, Parent=Parent,
                       Items=Items, Font=Font,
                       Separation=Separation,
                       Horizontal=Horizontal, VerticalCenter=VerticalCenter,
                       HorizontalCenter=HorizontalCenter)
        if Parent == None:
            _.ImageComponents.append(NewList)
        else:
            Parent.Children.append(NewList)


    async def Debug(_, VerticalCenter:bool=False, HorizontalCenter:bool=False) -> None:
        if VerticalCenter:
            await _.Line(Start=Vector2(_.XCenter, 0), End=Vector2(_.XCenter, _.Height), Width=3, Color=DEBUG_COLOR)
        if HorizontalCenter:
            await _.Line(Start=Vector2(0, _.YCenter), End=Vector2(_.Width, _.YCenter), Width=3, Color=DEBUG_COLOR)


    async def Add_Button(_, Label:str, Callback:Callable, Arguments:list) -> None:
        NewButton = Button(label=Label, style=ButtonStyle.grey)
        NewButton.callback = lambda Interaction: Callback(Interaction, *Arguments)
        _.ViewContent.append(NewButton)


    async def Construct_Components(_):
        ImageComponent:Component
        for ImageComponent in _.ImageComponents:
            ComponentImage:Image = await ImageComponent.Draw()
            _.Image.paste(im=ComponentImage, box=(ImageComponent.X, ImageComponent.Y), mask=ComponentImage.split()[3])


    async def Construct_View(_) -> None:
        _.BaseViewFrame = View(timeout=144000)
        if len(_.ViewContent) > 0:
            for Content in _.ViewContent:
                _.BaseViewFrame.add_item(Content)
        _.ViewContent = []


    async def Reply(_, Interaction:DiscordInteraction) -> None:
        _.BaseViewFrame = View(timeout=144000)
        await _.Construct_View()
        if _.BaseViewFrame.total_children_count > 0 and _.Image == None:
            await Interaction.response.edit_message(embed=_.EmbedFrame, view=_.BaseViewFrame)
        elif _.Image != None:
            await _.Construct_Components()
            _.EmbedFrame = Embed(title="")
            _.EmbedFrame.set_image(url="attachment://GameImage.png")
            await _.Buffer_Image()
            await Interaction.response.edit_message(embed=_.EmbedFrame, view=_.BaseViewFrame, attachments=[_.ImageFile])
            _.ImageFile = None
        else:
            print("Your Reply has nothing on it.")


    async def Send_Dashboard_Command(_, InitialContext:Context=None) -> None:
        await InitialContext.message.delete()
        if _.Message is not None: _.Message.delete()
        await _._Entry()
        _.BaseViewFrame = View(timeout=144000)
        await _.Construct_View()
        if _.BaseViewFrame.total_children_count > 0 and _.Image == None:
            _.Message = await InitialContext.send(embed=_.EmbedFrame, view=_.BaseViewFrame)
        elif _.Image != None:
            await _.Construct_Components()
            _.EmbedFrame = Embed(title="")
            _.EmbedFrame.set_image(url="attachment://GameImage.png")
            await _.Buffer_Image()
            _.Message = await InitialContext.send(embed=_.EmbedFrame, view=_.BaseViewFrame, file=_.ImageFile)
        else:
            print("Your Dashboard has nothing on it.")