import argparse

from ..voxmap import VoxMap

def generate(args):
    voxmap = VoxMap(args.width, args.depth, args.depth)
    for i in range(args.depth):
        voxmap.fill(True, 0, i, i, args.width, args.depth - i, 1)
    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('stairs')
    parser.add_argument('width', type=int, help='map width')
    parser.add_argument('depth', type=int, help='map depth')
    return parser
