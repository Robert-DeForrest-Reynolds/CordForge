class Vector2:
    x:int
    y:int

    def __init__(_, x: int = 0, y: int = 0):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Vector2 only supports integers.")
        _.x = x
        _.y = y


    def __add__(_, other: "Vector2") -> "Vector2":
        return Vector2(_.x + other.x, _.y + other.y)


    def __sub__(_, other: "Vector2") -> "Vector2":
        return Vector2(_.x - other.x, _.y - other.y)


    def __mul__(_, value: int) -> "Vector2":
        if not isinstance(value, int):
            raise TypeError("Multiplication only supports integers.")
        return Vector2(_.x * value, _.y * value)


    def __floordiv__(_, value: int) -> "Vector2":
        if value == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        if not isinstance(value, int):
            raise TypeError("Division only supports integers.")
        return Vector2(_.x // value, _.y // value)


    def __eq__(_, other: object) -> bool:
        if not isinstance(other, Vector2):
            return False
        return _.x == other.x and _.y == other.y


    def __iter__(_) -> iter:
        return iter((_.x, _.y))


    def __repr__(_) -> str:
        return f"Vector2({_.x}, {_.y})"


    def copy(_) -> "Vector2":
        return Vector2(_.x, _.y)
