from typing import Iterator, Self


class Point2d:
    __slots__ = ("_x", "_y")
    WIDTH: int = 1920
    HEIGHT: int = 1080

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = self.check_coordinate(value, self.WIDTH)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = self.check_coordinate(value, self.HEIGHT)

    @staticmethod
    def check_coordinate(value: int, limit: int) -> int:
        if not 0 <= value <= limit:
            raise ValueError(f"Coordinate must be between 0 and {limit}")
        return value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._x == other._x and self._y == other._y

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self._x}, y={self._y})"

    __repr__ = __str__


class Vector2d:
    __slots__ = ("_x", "_y")

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def dot(self, other: Self) -> int:
        return self.dot_product(self, other)

    def cross(self, other: Self) -> int:
        return self.cross_product(self, other)

    def mixed(self, second: Self, third: Self) -> int:
        return self.triple_product(self, second, third)

    @classmethod
    def from_points(cls, start: Point2d, end: Point2d) -> Self:
        return cls(end.x - start.x, end.y - start.y)

    @classmethod
    def dot_product(cls, first: Self, second: Self) -> int:
        return first._x * second._x + first._y * second._y

    @classmethod
    def cross_product(cls, first: Self, second: Self) -> int:
        return first._x * second._y - first._y * second._x

    @classmethod
    def triple_product(cls, a: Self, b: Self, c: Self) -> int:
        return cls.cross_product(a - b, c - a)

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        raise IndexError("Vector index out of range")

    def __setitem__(self, index: int, value: int) -> None:
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise IndexError("Vector index out of range")

    def __iter__(self) -> Iterator[int]:
        yield self._x
        yield self._y

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._x == other._x and self._y == other._y

    def __abs__(self) -> float:
        return (self._x**2 + self._y**2) ** 0.5

    def __add__(self, other: Self) -> Self:
        return self.__class__(self._x + other._x, self._y + other._y)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self._x - other._x, self._y - other._y)

    def __mul__(self, scalar: int | float) -> Self:
        return self.__class__(int(self._x * scalar), int(self._y * scalar))

    def __truediv__(self, scalar: int | float) -> Self:
        return self.__class__(int(self._x / scalar), int(self._y / scalar))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self._x}, y={self._y})"

    __repr__ = __str__


if __name__ == "__main__":
    p1 = Point2d(100, 100)
    p2 = Point2d(200, 300)
    v = Vector2d.from_points(p1, p2)
    print(v, abs(v), v[0], v[1], str(v))
