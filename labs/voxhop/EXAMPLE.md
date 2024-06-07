# Example Write-Up

_This writeup describes the Python maze generator found in `example.py`._


This program generates mazes of a user-selected width (`W`) and height (`H`).
It uses the following algorithm:

- It first creates a rectangular array of vertices.  Each vertex is represented
  by a disjoint set node augmented with connection information: two booleans
  that indicate whether the vertex is connected to its northern and western
  neighbors.  Information about whether the vertex is connected to its southern
  or eastern neighbors is stored in those neighbors.

  Creating a vertex can be done in `O(1)` time, and the vertices are stored in
  Python `list`s, which are actually implemented as vectors, so building the
  grid takes amortized `O(V)` time, where `V = W * H`.

- It then creates objects representing all possible connections between vertices
  and stores them in a single Python `list`.  Each vertex can have at most four
  connections, and each connection connects two vertices, so there are at most
  `E = 4 / 2 * V = 2V` edges, and this step runs in amortized `O(E)` time.

- It then shuffles the array of edges.  This is presumably implemented with the
  Fisher-Yates shuffle, so it should run in `O(E)` time.

- It then loops over each of the `E` edges in the shuffled array, and for each
  edge:

  - It finds the source and destination vertex in the grid.  These are vector
    index lookups, and run in `O(1)`.

  - It attempts to merge the two vertices' disjoint sets.  Since this disjoint
    set uses both path compression and union by weight, this operation has a
    runtime of the inverse Ackermann function.  This function grows extremely
    slowly, and for all practical purposes it's indistinguishable from `O(1)`.

  - If a union occurs, it updates the vertices to add the connection.  This also
    only takes `O(1)`.

- Finally, it loops over each vertex in the grid as it prints the maze.

In summary, the runtimes of each step are:

- `O(V)` to build the vertex grid.
- `O(E)` to build the edge list.
- `O(E)` to shuffle the edge list.
- `O(E) * O(1) = O(E)` to make connections.
- `O(V)` to print the result.

This gives a total runtime of `O(V + E)`, and since `E` is approximately equal
to `2V`, we can simplify this even further, to `O(V)`.
