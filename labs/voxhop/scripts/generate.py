#! /usr/bin/env python3

import argparse
import random
import sys

from lib.maps import flatland, goo, greatwall, labrat, mines, pyramid, skywalk, stairs, stairs2, towers

def main():
    parser     = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser.add_argument('-s', '--seed', type=int, help='random seed')

    flatland.subparser(subparsers)
    greatwall.subparser(subparsers)
    goo.subparser(subparsers)
    labrat.subparser(subparsers)
    mines.subparser(subparsers)
    pyramid.subparser(subparsers)
    skywalk.subparser(subparsers)
    stairs.subparser(subparsers)
    stairs2.subparser(subparsers)
    towers.subparser(subparsers)

    args = parser.parse_args()
    # print(args)

    if args.seed is None:
        args.seed = random.randrange(2**32)
    sys.stderr.write('Random seed is %d.\n' % args.seed)
    random.seed(args.seed)

    if args.command == 'flatland':
        voxmap = flatland.generate(args)
    elif args.command == 'goo':
        voxmap = goo.generate(args)
    elif args.command == 'greatwall':
        voxmap = greatwall.generate(args)
    elif args.command == 'labrat':
        voxmap = labrat.generate(args)
    elif args.command == 'mines':
        voxmap = mines.generate(args)
    elif args.command == 'pyramid':
        voxmap = pyramid.generate(args)
    elif args.command == 'skywalk':
        voxmap = skywalk.generate(args)
    elif args.command == 'stairs':
        voxmap = stairs.generate(args)
    elif args.command == 'stairs2':
        voxmap = stairs2.generate(args)
    elif args.command == 'towers':
        voxmap = towers.generate(args)
    else:
        raise Unreachable()

    voxmap.write(sys.stdout)

if __name__ == '__main__':
    main()
