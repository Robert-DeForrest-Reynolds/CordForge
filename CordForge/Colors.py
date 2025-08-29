class Color(tuple):
    __slots__ = []
    def __new__(Class,R,G,B,A=255):
        return super().__new__(Class,[R,G,B,A])

    @property
    def R(_): return _[0]
    @property
    def G(_): return _[1]
    @property
    def B(_): return _[2]
    @property
    def A(_):return _[3]

    def __repr__(_):
        return f"Color({_.R},{_.G},{_.B},{_.A})"


WHITE = Color(255,255,255,255)
BLACK = Color(0,0,0,255)
GRAY = Color(30,30,30,255)
DEBUG_COLOR = Color(255,0,255,255)
TRANSPRENCY = Color(0,0,0,0)