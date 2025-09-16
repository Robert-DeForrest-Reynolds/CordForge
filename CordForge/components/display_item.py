from PIL import Image as Image
from ..font import Font

class DisplayItem:
    def __init__(_, text:str, image:Image=None, separation:int=4, font:Font=None):
        _.image = image
        _.text = text
        _.font = font if font is not None else None
        _.separation = separation