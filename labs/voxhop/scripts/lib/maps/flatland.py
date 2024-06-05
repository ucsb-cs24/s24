import argparse

from ..voxmap import VoxMap

def generate(args):
    voxmap = VoxMap(args.width, args.depth, args.ground + args.sky)
    voxmap.fill(True, 0, 0, 0, args.width, args.depth, args.ground)
    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('flatland')
    parser.add_argument('-g', '--ground', type=int, default=1, help='ground height')
    parser.add_argument('-s', '--sky',    type=int, default=1, help='sky height')
    parser.add_argument('width',          type=int, help='map width')
    parser.add_argument('depth',          type=int, help='map depth')
    return parser
