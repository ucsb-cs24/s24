import argparse
import random
import sys

from ..argtype import *
from ..point   import Point
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
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

def generate(args):
    voxmap = VoxMap(args.cols * 4, args.rows * 4, args.tiers * 4)

    for z in range(args.tiers):
        ratmap = VoxMap(args.cols, args.rows, 1)

        for y in range(args.rows):
            for x in range(args.cols):
                point = Point(x, y, 0)
                ratmap[point] = DisjointSet(point)

        centers = set()
        edges   = []

        clusters = random.randrange(args.min_clusters, args.max_clusters + 1)
        clusters = min(clusters, args.cols * args.rows)
        # sys.stderr.write('tier %d: %d clusters\n' % (z, clusters))

        while len(centers) < clusters:
            x     = random.randrange(args.cols)
            y     = random.randrange(args.rows)
            point = Point(x, y, 0)

            if point in centers:
                continue

            centers.add(point)
            edges.append(Edge(point, point.north()))
            edges.append(Edge(point, point.east()))
            edges.append(Edge(point, point.south()))
            edges.append(Edge(point, point.west()))

        while len(edges) > 0:
            i    = random.randrange(len(edges))
            edge = edges[i]
            src  = ratmap.get(edge.src)
            dst  = ratmap.get(edge.dst)

            edges[i] = edges[-1]
            edges.pop()

            if dst is None:
                continue

            if dst.find() != dst:
                if dst.find() == src.find():
                    if random.random() < args.loop:
                        # Same cluster; add a loop.
                        pass
                    else:
                        # Same cluster.
                        continue
                else:
                    # Different clusters.
                    continue
            else:
                # Only add outbound edges for new segments...
                edges.append(Edge(edge.dst, edge.dst.north()))
                edges.append(Edge(edge.dst, edge.dst.east()))
                edges.append(Edge(edge.dst, edge.dst.south()))
                edges.append(Edge(edge.dst, edge.dst.west()))

            # Add an edge!
            src.union(dst)

            x = min(edge.src.x, edge.dst.x)
            y = min(edge.src.y, edge.dst.y)
            w = 6 if edge.src.y == edge.dst.y else 2
            d = 6 if edge.src.x == edge.dst.x else 2

            voxmap.fill(True, 4*x+1, 4*y+1, 4*z, w, d, 1)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('skywalk')
    parser.add_argument('--min-clusters', type=uint(min=1), default=1)
    parser.add_argument('--max-clusters', type=uint(min=1), default=9)
    parser.add_argument('-l', '--loop',   type=prob(),      default=0.05, help='loop probability')

    parser.add_argument('rows',  type=dim(), help='rows')
    parser.add_argument('cols',  type=dim(), help='columns')
    parser.add_argument('tiers', type=dim(), help='tiers')
    return parser
