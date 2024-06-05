import argparse
import heapq
import math
import random
import sys

from ..argtype import *
from ..point   import Point
from ..voxmap  import VoxMap

class KDNode:
    def __init__(self, point, axis):
        self.point    = point
        self.axis     = axis
        self.children = [None, None]

    def insert(self, point):
        i = 0 if point[self.axis] < self.point[self.axis] else 1
        if self.children[i] is None:
            self.children[i] = KDNode(point, (self.axis + 1) % 3)
        else:
            self.children[i].insert(point)

    def lookup(self, point, array):
        i = 0 if point[self.axis] < self.point[self.axis] else 1
        if self.children[i] is not None:
            self.children[i].lookup(point, array)

        d  = self.point - point
        d2 = -d.dot(d)

        if len(array) < 2:
            heapq.heappush(array, (d2, self.point))
        elif d2 > array[0][0]:
            heapq.heapreplace(array, (d2, self.point))

        d  = self.point[self.axis] - point[self.axis]
        d2 = -(d * d)

        if d2 > array[0][0] and self.children[i^1] is not None:
            self.children[i^1].lookup(point, array)


class KDTree:
    def __init__(self):
        self.root = None

    def insert(self, point):
        if self.root is None:
            self.root = KDNode(point, 0)
        else:
            self.root.insert(point)

    def nearest(self, point):
        array = []
        if self.root is not None:
            self.root.lookup(point, array)
        return array


def dist(point, x, y, z):
    d = point - (x, y, z)
    return d.dot(d)

def generate(args):
    size    = 2 * args.radius + 8
    center  = Point(1, 1, 1) * (size / 2)
    radius2 = args.radius * args.radius

    dz = args.edge_length * math.sqrt(2/3)
    dy = args.edge_length * args.slope * math.sin(math.pi/3)
    dx = args.edge_length * args.slope

    sys.stderr.write('dx = %f\n' % dx)
    sys.stderr.write('dy = %f\n' % dy)
    sys.stderr.write('dz = %f\n' % dz)

    blobs = VoxMap(math.ceil(size/dx), math.ceil(size/dy), math.ceil(size/dz))

    # Create some tetrahedral points...
    points = []
    for t in range(blobs.height):
        for r in range(blobs.depth):
            for c in range(blobs.width):
                oy = (t % 3) / 3 * dy
                ox1 = (t % 3) % 2 * dx/2
                # ox = ((t + r) % 2) / 2 * dx
                ox = ox1 + (r % 2) * dx/2

                x = c*dx+ox
                y = r*dy+oy
                z = t*dz

                point = Point(x, y, z)
                if (point - center).length2() > radius2:
                    continue

                blobs[c, r, t] = point
                points.append(point)

    # Index them for fast lookup...
    tree = KDTree()
    random.shuffle(points)
    for point in points:
        tree.insert(point)

    # Select some linked edges...
    edges = []
    for t in range(blobs.height):
        for r in range(blobs.depth):
            for c in range(blobs.width):
                node = blobs[c, r, t]

                if c > 0:
                    other = blobs[c - 1, r, t]
                    edges.append((node, other))

                if r > 0:
                    d = -1 if y % 2 == 0 else 0
                    if c + d >= 0:
                        other = blobs[c + d, r - 1, t]
                        edges.append((node, other))
                    if c + d + 1 < blobs.width:
                        other = blobs[c + d + 1, r - 1, t]
                        edges.append((node, other))

                if t > 0:
                    d = -1 if t % 3 == 0 else 0
                    if c + d >= 0:
                        other = blobs[c + d, r, t - 1]
                        edges.append((node, other))
                    if c + d + 1 < blobs.width:
                        other = blobs[c + d + 1, r, t - 1]
                        edges.append((node, other))
                    if r + 1 < blobs.depth:
                        other = blobs[c, r + 1, t - 1]
                        edges.append((node, other))

    random.shuffle(edges)
    edges = [edge for edge in edges if edge[1]]
    selected = set(edges[:int(len(edges) * args.edge_chance)])

    # Build the voxel map...
    voxmap = VoxMap(size, size, size)

    for x in range(size):
        for y in range(size):
            for z in range(size):
                p = Point(x, y, z)
                m = p - center
                if m.dot(m) > radius2:
                    continue

                close = tree.nearest(p)

                if close[1][0] > -36:
                    voxmap[x, y, z] = True
                else:
                    src = close[0][1]
                    dst = close[1][1]
                    if (src, dst) in selected or (dst, src) in selected:
                        # d1 = math.sqrt(-close[0][0])
                        # d2 = math.sqrt(-close[1][0])
                        # if d1 + d2 < 25:
                        #     voxmap[x, y, z] = True

                        v1 = dst - src
                        v2 = p   - src
                        v3 = p   - dst

                        l2 = v2.length()
                        l3 = v3.length()
                        l  = min(l2, l3)

                        same = v2.project(v1)

                        dist = (v2 - same).length()
                        if dist < 30 / l:
                            voxmap[x, y, z] = True


    # for x in range(size):
    #     for y in range(size):
    #         for z in range(size):
    #             p = Point(x, y, z)
    #             m = p - center
    #             if m.dot(m) > radius2:
    #                 continue

    #             # sys.stderr.write('(R, T) = %d, %d\n' % (R, T))

    #             # nearest  = None
    #             # distance = 99999999

    #             close = []

    #             T = math.floor(z/dz)
    #             for t in range(T, T + 2):
    #                 oy  = (t % 3) / 3 * dy
    #                 ox1 = (t % 2) / 2 * dx
    #                 R  = math.floor((y - oy) / dy)

    #                 for r in range(R, R + 2):
    #                     ox = ox1 + (r % 3) * dx / 2
    #                     C  = math.floor((x - ox) / dx)
    #                     for c in range(C, C + 2):
    #                         d = dist(p, c*dx+ox, r*dy+oy, t*dz)
    #                         close.append((d, c, r, t))

    #                         # if d < distance:
    #                         #     distance = d
    #                         #     nearest  = (c, r, t)

    #             close.sort()

    #             if close[0][0] < 9:
    #                 voxmap[x, y, z] = True
                # elif math.sqrt(close[0][0] + close[1][0]) < 13:
                #     voxmap[x, y, z] = True

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('goo')
    parser.add_argument('-c', '--edge-chance', type=prob(), help='edge chance', default=0.66)
    parser.add_argument('-l', '--edge-length', type=dim(),  help='edge length', default=20)
    parser.add_argument('-s', '--slope',       type=float,  help='slope multiplier', default=1.2)
    parser.add_argument('radius', type=width())
    return parser
