import random

class DisjointSet:
    def __init__(self):
        """Creates an isolated disjoint set node."""
        self.parent = None
        self.weight = 1

        # Is there a connection in the 0=north / 1=west direction?
        self.edges = [False, False]

    def find(self):
        """Finds the set representative of a node."""
        if self.parent is None:
            return self
        self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        """Merges two sets; returns True if they weren't already merged."""
        my_rep = self.find()
        yo_rep = other.find()

        if my_rep is yo_rep:
            return False
        elif my_rep.weight < yo_rep.weight:
            yo_rep.weight += my_rep.weight
            my_rep.parent  = yo_rep
        else:
            my_rep.weight += yo_rep.weight
            yo_rep.parent  = my_rep
        return True


class Edge:
    def __init__(self, x, y, d):
        self.x = x  # Source X coordinate
        self.y = y  # Source Y coordinate
        self.d = d  # Direction


def main(width, height):
    vertices = []
    edges    = []

    # Vertices are disjoint set nodes...
    for y in range(height):
        vertices.append([DisjointSet() for x in range(width)])

    # Add northbound edges...
    for y in range(1, height):
        edges.extend(Edge(x, y, 0) for x in range(width))

    # Add westbound edges...
    for x in range(1, width):
        edges.extend(Edge(x, y, 1) for y in range(height))

    # Select edges in random order...
    random.shuffle(edges)

    # Kruskal's Algorithm!
    for edge in edges:
        dx = 1 if edge.d == 1 else 0
        dy = 0 if edge.d == 1 else 1

        src = vertices[edge.y     ][edge.x]
        dst = vertices[edge.y - dy][edge.x - dx]
        if src.union(dst):
            src.edges[edge.d] = True

    # Print the map...
    for y in range(height):
        for x in range(width):
            top = '+   ' if vertices[y][x].edges[0] else '+---'
            print(top, end='')
        print('+')

        for x in range(width):
            mid = '    ' if vertices[y][x].edges[1] else '|   '
            print(mid, end='')
        print('|')

    for x in range(width):
        print('+---', end='')
    print('+')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('width',  type=int, help='width of the maze')
    parser.add_argument('height', type=int, help='height of the maze')

    args = parser.parse_args()
    main(args.width, args.height)
