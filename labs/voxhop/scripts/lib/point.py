from collections import namedtuple
import math

PointBase = namedtuple('PointBase', ['x', 'y', 'z'])

class Point(PointBase):
    def __new__(cls, x=0, y=0, z=0):
        return super(Point, cls).__new__(cls, x, y, z)

    # def __init__(self, x=0, y=0, z=0):
    #     super(Point, self).__init__(self, x, y, z)

    def __add__(self, other):
        return Point(
            self.x + other[0],
            self.y + other[1],
            self.z + other[2]
        )

    def __sub__(self, other):
        return Point(
            self.x - other[0],
            self.y - other[1],
            self.z - other[2]
        )

    def __mul__(self, other):
        if getattr(other, '__getitem__', False):
            return Point(
                self.x * other[0],
                self.y * other[1],
                self.z * other[2]
            )
        return Point(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def abs(self):
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def dot(self, other):
        return self.x * other[0] + self.y * other[1] + self.z * other[2]

    def down(self):
        return Point(self.x, self.y, self.z - 1)

    def east(self):
        return Point(self.x + 1, self.y, self.z)

    def length(self):
        return math.sqrt(self.dot(self))

    def length2(self):
        return self.dot(self)

    def max(self, other):
        return Point(
            max(self.x, other[0]),
            max(self.y, other[1]),
            max(self.z, other[2])
        )

    def min(self, other):
        return Point(
            min(self.x, other[0]),
            min(self.y, other[1]),
            min(self.z, other[2])
        )

    def north(self):
        return Point(self.x, self.y - 1, self.z)

    def project(self, other):
        # Vector projection onto other.
        return other * (self.dot(other) / other.dot(other))

    def reject(self, other):
        return self - self.project(other)

    def south(self):
        return Point(self.x, self.y + 1, self.z)

    def up(self):
        return Point(self.x, self.y, self.z + 1)

    def west(self):
        return Point(self.x - 1, self.y, self.z)

    def __str__(self):
        return '(%d, %d, %d)' % self

NORTH = Point( 0, -1,  0)
EAST  = Point(+1,  0,  0)
SOUTH = Point( 0, +1,  0)
WEST  = Point(-1,  0,  0)
UP    = Point( 0,  0, +1)
DOWN  = Point( 0,  0, -1)

CARDINALS = (
    NORTH,
    EAST,
    SOUTH,
    WEST
)

DIRECTIONS = (
    NORTH,
    EAST,
    SOUTH,
    WEST,
    UP,
    DOWN
)
