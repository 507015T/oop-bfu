import pytest
from lab1 import Point2d, Vector2d


class TestPoint2d:
    @pytest.mark.parametrize(
        "x,y", [(0, 0), (100, 200), (Point2d.WIDTH, Point2d.HEIGHT)]
    )
    def test_valid_creation(self, x, y):
        point = Point2d(x, y)
        assert point.x == x
        assert point.y == y

    @pytest.mark.parametrize(
        "x,y",
        [(-1, 100), (Point2d.WIDTH + 1, 100), (100, -1), (100, Point2d.HEIGHT + 1)],
    )
    def test_invalid_creation(self, x, y):
        with pytest.raises(ValueError):
            Point2d(x, y)

    def test_equality(self):
        p1 = Point2d(10, 20)
        p2 = Point2d(10, 20)
        p3 = Point2d(30, 40)
        assert p1 == p2
        assert p1 != p3
        assert p1 != "not a point"

    def test_str_repr(self):
        p = Point2d(5, 15)
        assert str(p) == "Point2d(x=5, y=15)"
        assert repr(p) == "Point2d(x=5, y=15)"


class TestVector2d:
    @pytest.mark.parametrize("x,y", [(0, 0), (1, 2), (-3, -4)])
    def test_creation_xy(self, x, y):
        v = Vector2d(x, y)
        assert v[0] == x
        assert v[1] == y

    def test_creation_from_points(self):
        p1 = Point2d(1, 2)
        p2 = Point2d(4, 6)
        v = Vector2d.from_points(p1, p2)
        assert v == Vector2d(3, 4)

    def test_get_set_item(self):
        v = Vector2d(1, 2)
        assert v[0] == 1
        assert v[1] == 2

        v[0] = 10
        v[1] = 20
        assert v == Vector2d(10, 20)

        with pytest.raises(IndexError):
            _ = v[2]
        with pytest.raises(IndexError):
            v[2] = 100

    def test_iter_len(self):
        v = Vector2d(1, 2)
        assert list(v) == [1, 2]
        assert len(v) == 2

    def test_equality(self):
        v1 = Vector2d(1, 2)
        v2 = Vector2d(1, 2)
        v3 = Vector2d(2, 3)
        assert v1 == v2
        assert v1 != v3
        assert v1 != "not a vector"

    def test_str_repr(self):
        v = Vector2d(5, 6)
        assert str(v) == "Vector2d(x=5, y=6)"
        assert repr(v) == "Vector2d(x=5, y=6)"

    @pytest.mark.parametrize(
        "x,y,expected_length",
        [(3, 4, 5.0), (0, 0, 0.0), (1, 1, pytest.approx(1.41421356237))],
    )
    def test_abs(self, x, y, expected_length):
        v = Vector2d(x, y)
        assert abs(v) == expected_length

    def test_add_sub(self):
        v1 = Vector2d(1, 2)
        v2 = Vector2d(3, 4)
        assert v1 + v2 == Vector2d(4, 6)
        assert v2 - v1 == Vector2d(2, 2)

    @pytest.mark.parametrize(
        "scalar,expected",
        [(2, Vector2d(4, 8)), (0.5, Vector2d(1, 2)), (-1, Vector2d(-2, -4))],
    )
    def test_mul(self, scalar, expected):
        v = Vector2d(2, 4)
        assert v * scalar == expected

    @pytest.mark.parametrize(
        "scalar,expected",
        [(2, Vector2d(1, 2)), (0.5, Vector2d(4, 8)), (-1, Vector2d(-2, -4))],
    )
    def test_div(self, scalar, expected):
        v = Vector2d(2, 4)
        assert v / scalar == expected

    @pytest.mark.parametrize(
        "v1,v2,expected",
        [
            (Vector2d(1, 2), Vector2d(3, 4), 11),
            (Vector2d(0, 0), Vector2d(1, 1), 0),
            (Vector2d(-1, -2), Vector2d(3, 4), -11),
        ],
    )
    def test_dot_product(self, v1, v2, expected):
        assert v1.dot(v2) == expected
        assert Vector2d.dot_product(v1, v2) == expected

    @pytest.mark.parametrize(
        "v1,v2,expected",
        [
            (Vector2d(1, 2), Vector2d(3, 4), -2),
            (Vector2d(0, 0), Vector2d(1, 1), 0),
            (Vector2d(-1, -2), Vector2d(3, 4), 2),
        ],
    )
    def test_cross_product(self, v1, v2, expected):
        assert v1.cross(v2) == expected
        assert Vector2d.cross_product(v1, v2) == expected

    def test_mixed_product(self):
        a = Vector2d(1, 0)
        b = Vector2d(0, 1)
        c = Vector2d(1, 1)
        assert a.mixed(b, c) == 1
