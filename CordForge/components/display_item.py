from PIL import Image as Image
from ..font import Font as CFFont

class DisplayItem:
    def __init__(_, text:str, image:Image=None, separation:int=4, font:CFFont=None):
        _.image = image
        _.text = text
        _.font = font
        _.separation = separation