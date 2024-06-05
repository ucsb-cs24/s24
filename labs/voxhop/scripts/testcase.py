#! /usr/bin/env python3

import argparse
import random
import sys

from lib.argtype import prob
from lib.voxmap  import VoxMap

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flip',   type=prob(), default=0.0, help='chance to flip low-to-high queries')
    parser.add_argument('-n', '--number', type=int,    default=10,  help='number of queries to generate')
    parser.add_argument('-s', '--seed',   type=int,    help='random seed')
    parser.add_argument('mapfile', help='path to a map file')
    args = parser.parse_args()

    if args.seed is None:
        args.seed = random.randrange(2**32)
    sys.stderr.write('Random seed is %d.\n' % args.seed)
    random.seed(args.seed)

    voxmap = VoxMap.parse(args.mapfile)
    points = voxmap.valid_points()

    for i in range(args.number):
        src, dst = random.sample(points, 2)
        if src.z < dst.z and random.random() < args.flip:
            src, dst = dst, src

        print('%d\t%d\t%d\t\t%d\t%d\t%d' % (
            src.x, src.y, src.z,
            dst.x, dst.y, dst.z
        ))


if __name__ == '__main__':
    main()
