import argparse
import math
import random
import sys

from ..argtype import *
from ..voxmap  import VoxMap

def function(s):
    # The 1.2 instead of 2 is a hack for more interesting terrain.
    a1 = (s + s * (random.random() - 0.5)) / 3
    f1 = (s + s *  random.random()) * (1.2 * math.pi)
    d1 = f1 * random.random()

    a2 = (s + s * (random.random() - 0.5)) / 3
    f2 = (s + s *  random.random()) * (1.2 * math.pi)
    d2 = f2 * random.random()

    a3 = (s + s * (random.random() - 0.5)) / 3
    f3 = (s + s *  random.random()) * (1.2 * math.pi)
    d3 = f3 * random.random()

    def compute(x, y):
        result  = a1 * math.sin((x + d1) / f1)
        result += a2 * math.sin((y + d2) / f2)
        result += a3 * math.sin((x + y + d3) / f3)
        return result

    compute.amplitude = a1 + a2 + a3
    return compute


def generate(args):
    if args.amplitude is None:
        args.amplitude = min(args.width, args.depth) // 2

    # Create functions...
    functions = []
    # scale = max(args.width, args.depth)
    scale = args.amplitude / 2
    while scale > 1:
        f = function(scale)
        functions.append(f)
        scale /= 2

    # Calculate constants...
    zrange = sum(f.amplitude for f in functions)
    lift   = args.lift * zrange

    height = 2 * args.amplitude + args.wall_height + 3

    # # height = round(zrange + lift) + args.wall_height + 3
    # sys.stderr.write('scale  = %f\n' % scale)
    # sys.stderr.write('zrange = %f\n' % zrange)
    # sys.stderr.write('lift   = %f\n' % lift)
    # sys.stderr.write('height = %f\n' % height)


    # height = max(args.width, args.depth)
    # lift   = 10 - sum(f(args.width / 2, args.depth / 2) for f in functions)


    voxmap = VoxMap(args.width, args.depth, height)

    east_side = (args.width + args.wall_width) // 2
    west_side = (args.width - args.wall_width) // 2

    # Fill in the map...
    for y in range(args.depth):
        minh = 9999999
        maxh = 0
        for x in range(args.width):
            h = sum(f(x, y) for f in functions)
            h = round(max(0, h + lift))

            # Build a wall...
            if west_side <= x <= east_side:
                minh = min(minh, h)
                maxh = max(maxh, h)

            voxmap.fill(True, x, y, 0, 1, 1, h)

        for x in range(west_side, east_side + 1):
            h = maxh + args.wall_height
            if x == west_side or x == east_side:
                h += 1 # Rampart
                if (y + 1) % 4 < 2:
                    h += 1 # Crenelle

            voxmap.fill(True, x, y, minh, 1, 1, h - minh)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('greatwall')
    parser.add_argument('-a', '--amplitude', type=uint())
    # parser.add_argument('-l', '--lift',        type=prob(), default=0.5)
    parser.add_argument('-l', '--lift',        type=prob(), default=0.5)
    parser.add_argument('-H', '--wall-height', type=dim(),  default=10)
    parser.add_argument('-W', '--wall-width',  type=dim(),  default=10)

    parser.add_argument('width', type=width(), help='map width')
    parser.add_argument('depth', type=dim(),   help='map depth')
    return parser
