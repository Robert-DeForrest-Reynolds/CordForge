from os.path import join
from PIL import Image as PillowImage
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
import asyncio
from typing import Callable, Any

from .Components import *
from .Colors import *
from .Font import Font as CFFont
from .Vector2 import Vector2
from .Player import Player
from .Data import Data


class Cord(Bot):
    Message:DiscordMessage
    def __init__(_, DashboardAlias:str, Entry:Callable, Autosave:bool=False) -> None:
        _.DashboardAlias = DashboardAlias
        _._Entry = Entry
        _.Autosave = Autosave
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
        _.Font = CFFont(24)
        _.Data = Data(_)
        _.Players:dict[int:Player] = {}
        print("Discord Bot Initializing")
        super().__init__(command_prefix=_.Prefix, intents=Intents.all())


    @property
    def XCenter(_): return _.Width // 2
    @property
    def YCenter(_): return _.Height // 2
    @property
    def ImageCenter(_): return Vector2(_.XCenter, _.YCenter)
    

    def Run(_, Task, *Arguments) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(Task(*Arguments))
        raise RuntimeError("There is an existing loop.\n" \
                           "Run() is used for setup before the Bot runs it's loop.")


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
        async def Wrapper(Context): await _.Send_Dashboard_Command(Context)
        _.add_command(Command(Wrapper, aliases=_.DashboardAlias))
        await super().setup_hook()


    async def on_ready(_) -> None:
        print("Bot is alive.\n")
        _.Guilds = _.guilds
        await _.Data.Load_Data()
        if _.Autosave:
            await _.Data.Autosave()


    def Start(_) -> None: _.run(_._Get_Token(_.InstanceUser))


    def Load_Image(_, ImagePath:str) -> PillowImage:
        return PillowImage.open(ImagePath)


    async def New_Image(_) -> PillowImage:
        _.Image = PillowImage.new("RGBA",
                                  (_.Height, _.Width),
                                  color=_.DashboardBackground)
        return _.Image


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
    

    async def Container(_, X:int=0, Y:int=0, Parent:Component|None=None,
                        Width:int|None=None, Height:int|None=None, 
                        Background:Color=GRAY, Border:bool=False) -> Component:
        '''
        Create a Container Component\n
        A container's height and width is by default the parent container if given one, elsewise it's the Cord object that is it is created with.
        '''
        NewContainer = Container(Cord=_, X=X, Y=Y, Parent=Parent,
                                 Width=Width, Height=Height,
                                 Background=Background, Border=Border)
        if Parent == None:
            _.ImageComponents.append(NewContainer)
        else:
            Parent.Children.append(NewContainer)
        return NewContainer


    async def Line(_, X:int=0, Y:int=0, Parent:Component|None=None,
                   Start:Vector2=Vector2(0,0), End:Vector2=Vector2(0,0),
                   Color:Color=WHITE, FillWidth:int=1,
                   Curve:bool=False) -> None:
        NewLine = Line(Cord=_, X=X, Y=Y, Parent=Parent,
                       Start=Start, End=End,
                       FillWidth=FillWidth, Color=Color, Curve=Curve)
        if Parent == None:
            _.ImageComponents.append(NewLine)
        else:
            Parent.Children.append(NewLine)
        return NewLine


    async def List(_, X:int=0, Y:int=0, Parent:Component|None=None,
                   Width:int|None=None, Height:int|None=None,
                   Items:list[str:ListItem] = [], Font=None,
                   Separation:int=4, Horizontal:bool=False,
                   VerticalCenter:bool=False, HorizontalCenter:bool=False) -> None:
        NewList = List(Cord=_, X=X, Y=Y, Parent=Parent,
                       Width=Width, Height=Height,
                       Items=Items, Font=Font,
                       Separation=Separation,
                       Horizontal=Horizontal, VerticalCenter=VerticalCenter,
                       HorizontalCenter=HorizontalCenter)
        if Parent == None:
            _.ImageComponents.append(NewList)
        else:
            Parent.Children.append(NewList)
        return NewList
    

    async def Text(_, Content, Position:list|Vector2|None=None, Parent:Component|None=None,
                   Color:Color=WHITE, Background:Color=None, Font:CFFont=None,
                   Center:bool=False) -> Component:
        NewText = Text(Cord=_, Content=Content, Position=Position, Parent=Parent, Color=Color, Background=Background, Font=Font, Center=Center)
        if Parent == None:
            _.ImageComponents.append(NewText)
        else:
            Parent.Children.append(NewText)
        return NewText
    

    async def Sprite(_, X:int=0, Y:int=0, Parent:Component|None=None,
                    SpriteImage:PillowImage=None, Path:str=None) -> None:
        NewSprite = Sprite(Cord=_, X=X, Y=Y, Parent=Parent, SpriteImage=SpriteImage, Path=Path)
        if Parent == None:
            _.ImageComponents.append(NewSprite)
        else:
            Parent.Children.append(NewSprite)
        return NewSprite


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
        print("Constructing Dashboard Components")
        ImageComponent:Component
        for ImageComponent in _.ImageComponents:
            ComponentImage:PillowImage = await ImageComponent.Draw()
            _.Image.paste(im=ComponentImage, box=(ImageComponent.X, ImageComponent.Y), mask=ComponentImage.split()[3])
        _.ImageComponents = []


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
        if InitialContext.author.id not in _.Players.keys(): _.Data.Initial_Cache(InitialContext.author)

        await InitialContext.message.delete()
        
        if _.Message is not None: await _.Message.delete()
        
        User:Player = _.Players[InitialContext.author.id]
        
        try:
            await _._Entry(User)
        except TypeError as E:
            print("Entry needs to accept `user` as an argument")
        
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