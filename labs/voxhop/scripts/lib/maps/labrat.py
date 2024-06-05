import argparse
import random

from ..point  import Point
from ..voxmap import VoxMap

class DisjointSet:
    def __init__(self, point):
        self.parent = None
        self.point  = point

    def find(self):
        if self.parent is None:
            return self
        self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        sp = self.find()
        op = other.find()

        if sp is not op:
            sp.parent = op
            return True
        else:
            return False

class Edge:
    def __init__(self, src, dst):
        self.src  = src
        self.dst  = dst

def generate(args):
    ratmap = VoxMap(args.cols,     args.rows,     1)
    voxmap = VoxMap(args.cols * 4, args.rows * 4, 2)
    edges  = []

    for y in range(args.rows):
        for x in range(args.cols):
            point = Point(x, y, 0)
            ratmap[point] = DisjointSet(point)
            if y > 0:
                edges.append(Edge(Point(x, y-1), Point(x, y)))
            if x > 0:
                edges.append(Edge(Point(x-1, y), Point(x, y)))

    voxmap.fill(True, 0, 0, 0, 4*args.cols, 4*args.rows, 2)
    for y in range(args.rows):
        for x in range(args.cols):
            voxmap.fill(False, x*4+1, y*4+1, 1, 2, 2, 1)

    random.shuffle(edges)
    for edge in edges:
        src = ratmap[edge.src]
        dst = ratmap[edge.dst]
        if src.union(dst) or random.random() < args.loop:
            if edge.src.x == edge.dst.x:
                voxmap.fill(False, 4*src.point.x+1, 4*src.point.y+3, 1, 2, 2, 1)
            else:
                voxmap.fill(False, 4*src.point.x+3, 4*src.point.y+1, 1, 2, 2, 1)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('labrat')
    parser.add_argument('-l', '--loop', type=float, default=0.05, help='loop probability')
    parser.add_argument('rows', type=int, help='rows')
    parser.add_argument('cols', type=int, help='columns')
    return parser
