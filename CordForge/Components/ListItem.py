from PIL import Image as PillowImage
from ..Font import Font as CFFont

class ListItem:
    def __init__(_, Text:str, Image:PillowImage=None, Separation:int=4, Font:CFFont=None):
        _.Image = Image
        _.Text = Text
        _.Font = Font
        _.Separation = Separation