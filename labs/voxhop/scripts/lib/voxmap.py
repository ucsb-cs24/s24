from .errors import *
from .point  import *

class VoxMap:
    def __init__(self, width, depth, height, init=True, fill=None):
        self.width  = width
        self.depth  = depth
        self.height = height

        if init:
            self.data = [fill] * (width * depth * height)

    @staticmethod
    def parse(path):
        with open(path) as stream:
            file = enumerate(stream, 1)
            i, line = next(file)
            line = line.rstrip()

            try:
                dims = [int(x) for x in line.split()]
            except ValueError:
                raise ParseError(i, 'Could not parse integers.')

            if len(dims) != 3:
                raise ParseError(i, 'Expected three integers.')
            if dims[0] <= 0 or dims[0] >= 30000:
                raise ParseError(i, 'Width is out of bounds.')
            if dims[1] <= 0 or dims[1] >= 30000:
                raise ParseError(i, 'Depth is out of bounds.')
            if dims[2] <= 0 or dims[2] >= 30000:
                raise ParseError(i, 'Height is out of bounds.')
            if dims[0] % 4 != 0:
                raise ParseError(i, 'Width is not a multiple of four.')

            voxmap = VoxMap(*dims, False)
            data   = []

            for z in range(voxmap.height):
                i, line = next(file)
                line = line.rstrip()

                if line:
                    raise ParseError(i, 'Expected a blank line.')

                for y in range(voxmap.depth):
                    i, line = next(file)
                    line = line.rstrip()

                    if len(line) != voxmap.width // 4:
                        raise ParseError(i, 'Expected %d hex digits.' % (voxmap.width // 4))
                    for c in line:
                        try:
                            x = int(c, 16)
                        except ValueError:
                            raise ParseError(i, 'Found non-hex digit %s.' % c)
                        data.append((x & 8) != 0)
                        data.append((x & 4) != 0)
                        data.append((x & 2) != 0)
                        data.append((x & 1) != 0)

        voxmap.data = data
        return voxmap

    def __contains__(self, point):
        if point[0] < 0 or point[0] >= self.width:
            return False
        if point[1] < 0 or point[1] >= self.depth:
            return False
        if point[2] < 0 or point[2] >= self.height:
            return False
        return True

    def __getitem__(self, point):
        return self.data[
            point[2] * self.width * self.depth +
            point[1] * self.width +
            point[0]
        ]

    def __setitem__(self, point, value):
        self.data[
            point[2] * self.width * self.depth +
            point[1] * self.width +
            point[0]
        ] = value

    def fill(self, value, x, y, z, w=1, d=1, h=1):
        for i in range(x, x + w):
            for j in range(y, y + d):
                for k in range(z, z + h):
                    self[i, j, k] = value
        # TODO: Optimize this?

    def fillv(self, value, point1, point2):
        start = point1.min(point2)
        dims  = (point1 - point2).abs()
        self.fill(value, start.x, start.y, start.z, dims.x + 1, dims.y + 1, dims.z + 1)

    def get(self, point, default=None):
        if point in self:
            return self[point]
        return default

    def line(self, value, point, direction, length):
        d = DIRECTIONS[direction]
        for i in range(length):
            self[point] = value
            point += d

    def stairs(self, value, point, direction, height, fill=True):
        d = CARDINALS[direction]

        for i in range(height):
            if fill:
                l = height - i
            else:
                l = 2
            self.line(value, point, direction, l)
            point = point.up() + d

    def valid_points(self):
        points = []
        for x in range(self.width):
            for y in range(self.depth):
                b = False
                for z in range(self.height):
                    point = Point(x, y, z)
                    if self[point]:
                        b = True
                    elif b:
                        points.append(point)
                        b = False
        return points

    def validate_path(self, path, src, dst):
        self.validate_point(src)
        self.validate_point(dst)

        point = src
        for c in path:
            if c == 'n':
                next = point.north()
                if next.y < 0:
                    raise InvalidPath('Walked off the north edge.')
            elif c == 'e':
                next = point.east()
                if next.x >= self.width:
                    raise InvalidPath('Walked off the east edge.')
            elif c == 's':
                next = point.south()
                if next.y >= self.depth:
                    raise InvalidPath('Walked off the south edge.')
            elif c == 'w':
                next = point.west()
                if next.x < 0:
                    raise InvalidPath('Walked off the west edge.')
            else:
                raise InvalidPath('Unknown move %s.' % c)

            if self[next]:
                # It's full; maybe jump up?
                if point.z == self.height - 1:
                    raise InvalidPath('Climbed into space.')
                if self[next.up()]:
                    raise InvalidPath('Walked into a wall.')
                if self[point.up()]:
                    raise InvalidPath('Jumped into the ceiling.')
                point = next.up()
            else:
                # It's empty; maybe fall down?
                while next.z > 0:
                    down = next.down()
                    if self[down]:
                        break
                    next = down
                if next.z == 0:
                    raise InvalidPath('Fell into the water.')
                point = next

        if point != dst:
            raise InvalidPath('Does not end at destination.')
        return 'Valid route.'

    def validate_point(self, point):
        if point.x < 0 or point.x >= self.width:
            raise InvalidPoint(point)
        if point.y < 0 or point.y >= self.depth:
            raise InvalidPoint(point)
        if point.z < 1 or point.z >= self.height:
            raise InvalidPoint(point)

        if self[point]:
            raise InvalidPoint(point)
        if not self[point.down()]:
            raise InvalidPoint(point)

    def write(self, stream):
        stream.write('%d %d %d\n' % (self.width, self.depth, self.height))

        for z in range(self.height):
            stream.write('\n')
            for y in range(self.depth):
                for x in range(0, self.width, 4):
                    c = 0
                    if self[x + 0, y, z]: c |= 8
                    if self[x + 1, y, z]: c |= 4
                    if self[x + 2, y, z]: c |= 2
                    if self[x + 3, y, z]: c |= 1
                    stream.write(format(c, 'x'))
                stream.write('\n')
