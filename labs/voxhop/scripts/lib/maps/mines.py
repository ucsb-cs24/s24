import argparse
import random
import sys

from ..argtype import *
from ..point   import *
from ..voxmap  import VoxMap

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
            other.parent = self
            return True
        else:
            return False

class Edge:
    def __init__(self, src, dst, ttl):
        self.src = src
        self.dst = dst
        self.ttl = ttl

class Tunnel:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

class Shaft:
    def __init__(self, point, spin, depth):
        self.point = point
        self.spin  = spin
        self.depth = depth


def draw_platform(voxmap, start, shaft):
    norm = CARDINALS[shaft.spin]
    stop = start + [5, 5, 0]

    start -= norm.min([0, 0, 0])
    stop  -= norm.max([0, 0, 0])
    voxmap.fillv(True, start, stop)

    start += [1, 1, 0]
    stop  -= [1, 1, 0]
    voxmap.fillv(False, start, stop)

OFFSETS = (
    Point(0, 0, 0),
    Point(5, 0, 0),
    Point(5, 5, 0),
    Point(0, 5, 0)
)

def draw_stairs(voxmap, start, shaft):
    stair_start = start + OFFSETS[shaft.spin]
    stair_bump  = start + OFFSETS[(shaft.spin + 1) % 4] + [0, 0, 5]
    voxmap.stairs(True, stair_start, (shaft.spin + 1) % 4, 5, fill=False)
    voxmap[stair_bump] = True


def generate(args):
    # Invert the important bits for visual debugging:
    FILL = not args.debug
    HOLE = not FILL

    voxmap = VoxMap(args.cols * 6, args.rows * 6, args.tiers * 5, fill=FILL)
    ratmap = VoxMap(args.cols, args.rows, 1)

    shafts = {}
    while len(shafts) < args.shafts:
        x     = random.randrange(0, args.cols, 2)
        y     = random.randrange(0, args.rows, 2)
        point = Point(x, y)

        if point in shafts:
            continue

        spin  = random.randrange(4)
        depth = random.randrange(args.tiers // 2)
        # depth = 0
        shafts[point] = Shaft(point, spin, depth)

    # sys.stderr.write('shafts: %s\n' % shafts)

    # Clear things out above ground...
    voxmap.fill(False, 0, 0, 5 * (args.tiers - 1), 6 * args.cols, 6* args.rows, 5)

    for z in range(0, args.tiers - 1):
        # Initialize tier map...
        edges   = []
        tunnels = []

        for y in range(args.rows):
            for x in range(args.cols):
                point = Point(x, y, 0)
                ratmap[point] = DisjointSet(point)

        # Set up shafts...
        surface = DisjointSet(None)
        for shaft in shafts.values():
            # All shafts are connected
            surface.union(ratmap[shaft.point])

            if shaft.depth > z:
                continue

            for d in range(4):
                if d != shaft.spin:
                    dst  = shaft.point + CARDINALS[d]
                    edge = Edge(shaft.point, dst, args.branch_ttl)
                    edges.append(edge)

        if z == args.tiers - 2:
            # No tunnels directly beneath the surface...
            edges = []

        # Dig branches...
        while len(edges) > 0:
            i    = random.randrange(len(edges))
            edge = edges[i]
            src  = ratmap.get(edge.src)
            dst  = ratmap.get(edge.dst)

            edges[i] = edges[-1]
            edges.pop()

            if dst is None or not src.union(dst):
                continue

            if edge.ttl > 0:
                if random.random() < args.branch_chance:
                    edges.append(Edge(edge.dst, edge.dst.north(), edge.ttl - 1))
                if random.random() < args.branch_chance:
                    edges.append(Edge(edge.dst, edge.dst.east(),  edge.ttl - 1))
                if random.random() < args.branch_chance:
                    edges.append(Edge(edge.dst, edge.dst.south(), edge.ttl - 1))
                if random.random() < args.branch_chance:
                    edges.append(Edge(edge.dst, edge.dst.west(),  edge.ttl - 1))

            # Dig out an edge!
            src.union(dst)
            x = min(edge.src.x, edge.dst.x)
            y = min(edge.src.y, edge.dst.y)

            if edge.src.y == edge.dst.y:
                voxmap.fill(HOLE, 6*x+1, 6*y+1, 5*z+1, 10, 4, 2)
                voxmap.fill(HOLE, 6*x+2, 6*y+2, 5*z+1,  8, 2, 3)

                tunnel = Tunnel(6*x+1, 6*x+12, 6*y+1, 6*y+5)
                tunnels.append(tunnel)
            else:
                voxmap.fill(HOLE, 6*x+1, 6*y+1, 5*z+1, 4, 10, 2)
                voxmap.fill(HOLE, 6*x+2, 6*y+2, 5*z+1, 2,  8, 3)

                tunnel = Tunnel(6*x+1, 6*x+5, 6*y+1, 6*y+11)
                tunnels.append(tunnel)

        # Add debris...
        for tunnel in tunnels:
            for i in range(args.debris):
                x = random.randrange(tunnel.xmin, tunnel.xmax)
                y = random.randrange(tunnel.ymin, tunnel.ymax)
                w = random.randrange(1, 3)
                d = random.randrange(1, 3)
                h = random.randrange(1, 3)

                voxmap.fill(FILL, x, y, 5*z+1, w, d, h)

        # Dig shafts...
        for shaft in shafts.values():
            if shaft.depth <= z:
                start = shaft.point._replace(z=z) * [6, 6, 5]
                voxmap.fill(False, start.x, start.y, start.z, 6, 6, 5)
                draw_platform(voxmap, start, shaft)
                draw_stairs(voxmap, start, shaft)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('mines')
    parser.add_argument('--debug', action='store_true')

    parser.add_argument('-b', '--branch-chance', type=prob(),      default=0.5)
    parser.add_argument('-t', '--branch-ttl',    type=uint(min=1), default=8)
    parser.add_argument('-s', '--shafts',        type=uint(min=1), default=1)
    parser.add_argument('-d', '--debris',        type=uint(),      default=2)

    parser.add_argument('rows',  type=dim(mod=2), help='rows')
    parser.add_argument('cols',  type=dim(),      help='columns')
    parser.add_argument('tiers', type=dim(min=4), help='tiers')
    return parser
