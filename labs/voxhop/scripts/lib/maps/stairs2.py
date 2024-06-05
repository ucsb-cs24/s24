import argparse

from ..voxmap import VoxMap

def generate(args):
    h      = args.size // 2
    voxmap = VoxMap(args.size, args.size, h + 1)

    for i in range(h):
        voxmap.fill(True, 0, 0,     i, h, h - i, 1)
        voxmap.fill(True, h, h + i, i, h, h - i, 1)

        voxmap.fill(True, 0,     h, i, h - i, h, 1)
        voxmap.fill(True, h + i, 0, i, h - i, h, 1)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('stairs2')
    parser.add_argument('size', type=int, help='map width and depth')
    return parser
