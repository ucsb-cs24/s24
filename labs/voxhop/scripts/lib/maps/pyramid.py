import argparse

from ..voxmap import VoxMap

def generate(args):
    if args.height is None:
        args.height = min(args.width // 2, args.depth // 2)

    c = 1
    w = args.width - 2
    d = args.depth - 2

    voxmap = VoxMap(args.width, args.depth, args.height)
    for i in range(min(args.width, args.depth, args.height)):
        voxmap.fill(True, c, c, i, w, d, 1)
        w -= 2
        d -= 2
        c += 1

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('pyramid')
    parser.add_argument('width',  type=int, help='map width')
    parser.add_argument('depth',  type=int, help='map depth')
    parser.add_argument('height', type=int, help='map height', nargs='?')
    return parser
