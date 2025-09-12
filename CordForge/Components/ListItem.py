from PIL import Image as PillowImage
from ..Font import Font as CFFont

class ListItem:
    def __init__(_, text:str, image:PillowImage=None, separation:int=4, font:CFFont=None):
        _.image = image
        _.text = text
        _.font = font
        _.separation = separation