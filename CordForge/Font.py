from PIL import ImageFont

class Font:
    def __init__(_, FontPath:str|None=None, Size:int=24) -> None:
        _.Size = Size
        if isinstance(FontPath, str):
            _.Font = ImageFont.truetype(FontPath)
        else:
            _.Font = ImageFont.load_default(_.Size)
        _.Ascent, _.Descent = _.Font.getmetrics()
        _.Height = _.Ascent + _.Descent