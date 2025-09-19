class Color(tuple):
    r:int
    g:int
    b:int
    __slots__ = []
    def __new__(Class,r,g,b,a=255):
        return super().__new__(Class,[r,g,b,a])

    @property
    def r(_): return _[0]
    @property
    def g(_): return _[1]
    @property
    def b(_): return _[2]
    @property
    def a(_):return _[3]

    def __repr__(_):
        return f"Color({_.r},{_.g},{_.b},{_.a})"


WHITE = Color(255,255,255,255)
BLACK = Color(0,0,0,255)
GRAY = Color(30,30,30,255)
DEBUG_COLOR = Color(255,0,255,255)
TRANSPRENCY = Color(0,0,0,0)