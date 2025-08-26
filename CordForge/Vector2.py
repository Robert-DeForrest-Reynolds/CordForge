class Vector2:
    def __init__(_, X: int = 0, Y: int = 0):
        if not isinstance(X, int) or not isinstance(Y, int):
            raise TypeError("Vector2 only supports integers.")
        _.X = X
        _.Y = Y

    def __add__(_, Other: "Vector2") -> "Vector2":
        return Vector2(_.X + Other.X, _.Y + Other.Y)

    def __sub__(_, Other: "Vector2") -> "Vector2":
        return Vector2(_.X - Other.X, _.Y - Other.Y)

    def __mul__(_, Value: int) -> "Vector2":
        if not isinstance(Value, int):
            raise TypeError("Multiplication only supports integers.")
        return Vector2(_.X * Value, _.Y * Value)

    def __floordiv__(_, Value: int) -> "Vector2":
        if Value == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        if not isinstance(Value, int):
            raise TypeError("Division only supports integers.")
        return Vector2(_.X // Value, _.Y // Value)

    def __eq__(_, Other: object) -> bool:
        if not isinstance(Other, Vector2):
            return False
        return _.X == Other.X and _.Y == Other.Y

    def __iter__(_) -> iter:
        return iter((_.X, _.Y))

    def __repr__(_) -> str:
        return f"Vector2({_.X}, {_.Y})"

    def Copy(_) -> "Vector2":
        return Vector2(_.X, _.Y)
