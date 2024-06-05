import argparse
import random
import sys

from ..argtype import *
from ..point   import *
from ..voxmap  import VoxMap

class Room:
    def __init__(self, point):
        self.point   =  point
        self.floor   =  None
        self.ledge   =  None
        self.catwalk =  None
        self.stairs  =  None
        self.walls   = [None] * 4
        self.bridges = [None] * 2


STAIR_OFFSETS = (
    Point(1, 1, 0),
    Point(8, 1, 0),
    Point(8, 8, 0),
    Point(1, 8, 0)
)

def draw_stairs(voxmap, origin, d):
    start = origin + STAIR_OFFSETS[d]
    voxmap.line(False, start + (0, 0, 7), (d + 1) % 4, 7)
    voxmap.stairs(True, start, (d + 1) % 4, 8, fill=False)

DOOR_OFFSETS = (
    Point(4, 0, 0),
    Point(9, 4, 0),
    Point(4, 9, 0),
    Point(0, 4, 0)
)

def draw_door(voxmap, origin, d):
    start = origin + DOOR_OFFSETS[d]
    end   = start  + CARDINALS[(d + 1) % 4].abs()
    voxmap.fillv(False, start + (0, 0, 1), end + (0, 0, 3))

WINDOW_OFFSETS = (
    Point(0, 0, 3),
    Point(9, 0, 3),
    Point(0, 9, 3),
    Point(0, 0, 3)
)

def draw_window(voxmap, origin, d):
    start  = origin + WINDOW_OFFSETS[d]
    normal = CARDINALS[(d + 1) % 4].abs()

    window = start + normal
    voxmap.fillv(False, window, window + normal + (0, 0, 2))

    window += normal * 3
    voxmap.fillv(False, window, window + normal + (0, 0, 2))

    window += normal * 3
    voxmap.fillv(False, window, window + normal + (0, 0, 2))


def generate(args):
    maxdist = min(args.cols - 1, args.rows - 1) // 2
    maxtier = args.tiers + maxdist * args.constant_growth + args.random_growth

    # sys.stderr.write('maxdist = %d\n' % maxdist)
    # sys.stderr.write('maxtier = %d\n' % maxtier)

    rooms   = VoxMap(args.cols, args.rows, maxtier + 1)

    # Populate with rooms...
    for x in range(args.cols):
        for y in range(args.rows):
            xdist = min(x, args.cols - x - 1)
            ydist = min(y, args.rows - y - 1)
            dist  = min(xdist, ydist)

            lift  = dist * args.constant_growth
            lift += random.randrange(args.random_growth + 1)

            # sys.stderr.write('xdist = %d\n' % xdist)
            # sys.stderr.write('ydist = %d\n' % ydist)
            # sys.stderr.write('lift  = %d\n' % lift)
            h = args.tiers + lift

            for z in range(h):
                room = Room(Point(x, y, z))
                room.floor = random.random() < args.floor_chance
                room.ledge = random.random() < args.ledge_chance
                # sys.stderr.write('point = %d, %d, %d\n' % (x, y, z))
                rooms[x, y, z] = room

    args.tiers = maxtier

    # Add stairs...
    for x in range(args.cols):
        for y in range(args.rows):
            for z in range(args.tiers):
                room = rooms[x, y, z]
                if room is None:
                    # Reached the top.
                    break

                if room.floor is False and room.stairs is None:
                    # Can't start in midair.
                    room.stairs = False
                    continue

                if room.stairs is not None:
                    # Already set up from below.
                    continue

                if random.random() < args.stair_chance:
                    room.stairs = random.randrange(4)
                    room.walls[room.stairs] = 'stairs'

                    while True:
                        upper = rooms.get(room.point.up())
                        if upper:
                            # TODO: Allow windows here!
                            upper.walls[room.stairs] = 'window'

                        if upper and not upper.floor:
                            upper.stairs = (room.stairs + 1) % 4
                            upper.walls[upper.stairs] = 'stairs'
                            room = upper
                        else:
                            break
                else:
                    room.stairs = False

    # Add bridges...
    for x in range(args.cols):
        for y in range(args.rows):
            for z in range(args.tiers):
                room = rooms[x, y, z]
                if room is None:
                    break

                # North Bridge
                if y > 0 and random.random() < args.bridge_chance:
                    other = rooms[x, y - 1, z]
                    rokay = room.ledge or room.walls[0] is None
                    ookay = other and (other.ledge or other.walls[2] is None)

                    if rokay and ookay:
                        if random.random() < args.thin_bridge_chance:
                            room.bridges[0] = 'thin'
                        else:
                            room.bridges[0] = 'thick'

                        if room.walls[0] is None and random.random() < args.bridge_door_chance:
                            room.walls[0] = 'door'
                            room.catwalk  = True
                        if other.walls[2] is None and random.random() < args.bridge_door_chance:
                            other.walls[2] = 'door'
                            other.catwalk  = True

                # West Bridge
                if x > 0 and random.random() < args.bridge_chance:
                    other = rooms[x - 1, y, z]
                    rokay = room.ledge or room.walls[3] is None
                    ookay = other and (other.ledge or other.walls[1] is None)

                    if rokay and ookay:
                        if random.random() < args.thin_bridge_chance:
                            room.bridges[1] = 'thin'
                        else:
                            room.bridges[1] = 'thick'

                        if room.walls[3] is None and random.random() < args.bridge_door_chance:
                            room.walls[3] = 'door'
                            room.catwalk  = True
                        if other.walls[1] is None and random.random() < args.bridge_door_chance:
                            other.walls[1] = 'door'
                            other.catwalk  = True

    # Build the map...
    CELL = 20 # Cell Size
    D    =  9 # Width and Depth
    H    =  7 # Height

    voxmap = VoxMap(args.cols * CELL, args.rows * CELL, (args.tiers + 1) * H)

    # Add basic framing...
    for c in range(args.cols):
        for r in range(args.rows):
            for t in range(args.tiers + 1):
                room   = rooms[c, r, t]
                origin = Point(CELL*c + 3, CELL*r + 3, H*t)

                if not room:
                    # Reached the top - add a roof:
                    voxmap.fillv(True, origin, origin + (D, D, 0))
                    # And parapets!
                    voxmap.fillv(True, origin, origin + (0, D, 1))
                    voxmap.fillv(True, origin, origin + (D, 0, 1))
                    voxmap.fillv(True, origin + (D, 0, 0), origin + (D, D, 1))
                    voxmap.fillv(True, origin + (0, D, 0), origin + (D, D, 1))
                    break

                # Add Walls...
                voxmap.fillv(True, origin, origin + (0, D, H))
                voxmap.fillv(True, origin, origin + (D, 0, H))
                voxmap.fillv(True, origin + (D, 0, 0), origin + (D, D, H))
                voxmap.fillv(True, origin + (0, D, 0), origin + (D, D, H))

                # Add floors and ledges...
                if room.ledge:
                    voxmap.fillv(True, origin - (1, 1, 0), origin + (D+1, D+1, 0))
                else:
                    voxmap.fillv(True, origin, origin + (D, D, 0))

                if not room.floor:
                    if room.catwalk:
                        voxmap.fillv(False, origin + (2, 2, 0), origin + (D-2, D-2, 0))
                    else:
                        voxmap.fillv(False, origin + (1, 1, 0), origin + (D-1, D-1, 0))

    # Add stairs and bridges...
    for c in range(args.cols):
        for r in range(args.rows):
            for t in range(args.tiers):
                room   = rooms[c, r, t]
                origin = Point(CELL*c + 3, CELL*r + 3, H*t)
                if not room: break

                if room.stairs is not False:
                    draw_stairs(voxmap, origin, room.stairs)

                if room.bridges[0]: # North Bridge
                    bridge_start = origin + (3, -10, 0)
                    bridge_end   = origin + (6,   0, 0)
                    if room.bridges[0] == 'thin':
                        bridge_start += (1, 0, 0)
                        bridge_end   -= (1, 0, 0)
                    voxmap.fillv(True, bridge_start, bridge_end)

                if room.bridges[1]: # West Bridge
                    bridge_start = origin + (  0, 3, 0)
                    bridge_end   = origin + (-10, 6, 0)
                    if room.bridges[1] == 'thin':
                        bridge_start += (0, 1, 0)
                        bridge_end   -= (0, 1, 0)
                    voxmap.fillv(True, bridge_start, bridge_end)

    # Add doors and windows...
    for c in range(args.cols):
        for r in range(args.rows):
            for t in range(args.tiers):
                room   = rooms[c, r, t]
                origin = Point(CELL*c + 3, CELL*r + 3, H*t)
                if not room: break

                for d in range(4):
                    if room.walls[d] == 'door':
                        draw_door(voxmap, origin, d)
                    elif room.walls[d] == 'window':
                        draw_window(voxmap, origin, d)
                    elif room.walls[d] is None:
                        draw_window(voxmap, origin, d)

    return voxmap

def subparser(subparsers):
    parser = subparsers.add_parser('towers')
    parser.add_argument('-c', '--constant-growth', type=uint(), default=0)
    parser.add_argument('-r', '--random-growth',   type=uint(), default=0)

    parser.add_argument('--bridge-chance',      type=prob(), default=0.70)
    parser.add_argument('--thin-bridge-chance', type=prob(), default=0.30)
    parser.add_argument('--bridge-door-chance', type=prob(), default=0.90)
    parser.add_argument('--ledge-chance',       type=prob(), default=0.30)
    parser.add_argument('--stair-chance',       type=prob(), default=0.80)
    parser.add_argument('--floor-chance',       type=prob(), default=0.80)

    parser.add_argument('rows',  type=int, help='rows')
    parser.add_argument('cols',  type=int, help='columns')
    parser.add_argument('tiers', type=int, help='tiers')
    return parser
