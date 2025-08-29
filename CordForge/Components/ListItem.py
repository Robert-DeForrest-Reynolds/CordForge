from PIL import Image as PillowImage

class ListItem:
    def __init__(_, Text:str, Image:PillowImage=None, Separation:int=4):
        _.Image = Image
        _.Text = Text
        _.Separation = Separation