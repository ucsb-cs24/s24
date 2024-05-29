# VoxHop

You live on an island made of cubes, like a Minecraft world. Each cube is called
a "voxel" (short for volumetric pixel), and can be either full or empty.  A full
voxel is full of stone, and you can walk on top of it. An empty voxel is full of
air, and you can walk through it.

Finding your way around the island can be confusing, so you want to write a path
finding program to help you navigate. Your program will read a map of the island
when it starts up, and then it'll find routes between places on the island.

Some islands are big, so it's important that the program runs efficiently!


## Your Assignment

- Implement the program described below.
- You **may** use container classes from the standard library.
- Make sure you don't print anything that isn't explicitly allowed.
- Make sure you don't have any memory leaks.
- Make your program run as fast as possible.

**Note:** This is a challenge lab, and the rules are a little different.

- You may work with a partner if you choose to.  If you do, make _one_ final
  submission to Gradescope, and put both partners' names on it.
- To get full credit, your program needs to work correctly _and_ be reasonably
  efficient (performance tests coming soon).
- Extra credit is available for the fastest submissions.  The five fastest will
  receive 50 / 40 / 30 / 20 / 10 points of extra credit. If you work in a group,
  both group members will get the full bonus.


## The Program

Your program  should take one  command line argument:  this is the path to a map
file, which will be in the format described below. Your program should read this
file as it starts up, and then wait for user input.

User input  will come as a series of points in 3D space.  Each point consists of
three non-negative integers: `X`, `Y`, and `Z`.  These integers are separated by
whitespace; points are also separated by whitespace.

Your program should read two points at a time. The first point is the coordinate
of a "source" voxel,  and the second is the coordinate of a "destination" voxel.
It should then make sure that both voxels are valid places for someone to stand.
In order to be valid:

- The voxel must be empty.
- The voxel must have a full voxel directly below it.
- The voxel must be within the map bounds.

If either voxel is invalid, your program should print `Invalid point: (X, Y, Z)`
(where `X`, `Y`, and `Z`  are the coordinates  of the voxel)  and move on to the
next pair of voxels.

If both voxels are valid,  your program should attempt to find a route  from the
source voxel  to the destination voxel.  If you can find a route,  print it as a
single line in the format described below.  If you can't find a route, print `No
route from (X, Y, Z) to (X, Y, Z).`

Keep processing pairs of points until you reach the end of the input. You should
print exactly one line of output for every pair of points in the input.


## Other Stuff

| Coordinate | Dimension | Axis (0-N)  |
|------------|-----------|-------------|
| X          | Width     | West-East   |
| Y          | Depth     | North-South |
| Z          | Height    | Down-Up     |


## Routes and Moves

A route is a series of moves.  Each move is a single step in one of the four
cardinal directions: north, east, south, or west.  You can't move diagonally.

You also  can't specify a move in the Z direction.  Instead, you move up or down
automatically based on the terrain.  When you move into an empty voxel, you fall
until you hit a filled voxel  that you can stand on (you might not fall at all).
Alternatively,  if the voxel directly  above you  is empty,  you can jump up one
tier while moving.

For example, if your position is marked with `@`, and you want to move right:

```
  @-->X            @---\
+---+---+---+    +---+ |                  +---+            +---+        +---+
|   |   |   |    |   | |            /-->X |   |            |   |        |   |
+---+---+---+    +---+ V            | +---+---+            +---+        +---+---+
|   |   |   |    |   | X            @ |   |   |          @ |   |          @ |   |
+---+---+---+    +---+---+---+    +---+---+---+    +---+---+---+    +---+---+---+
|   |   |   |    |   |   |   |    |   |   |   |    |   |   |   |    |   |   |   |
+---+---+---+    +---+---+---+    +---+---+---+    +---+---+---+    +---+---+---+
  Flat Move        Fall Down         Jump Up         Can't Move       Can't Move
```

Any move that takes you into a wall or outside the bounds of the map is invalid.

When printing a route,  use the characters  `n`, `e`, `s`, and `w`  to represent
moves to the north, east, south, and west, respectively.  For example, to show a
route from point (2, 1, 1) to point (1, 4, 1), you could print `wsss`.


## Map File Format

The maps your program will read  are stored as ASCII text.  Each map file starts
with a line  containing three positive integers  separated by whitespace.  These
are, in order: the width of the map, the depth of the map, and the height of the
map. The width is the east-west axis, and the depth is the north-south axis. All
coordinates will be  between 1 and 30000 (inclusive),  and the width will always
be a multiple of four.

The rest of the file contains a series of "tiers."  Each tier represents a slice
of the map containing all the voxels at a specific height. The first tier is for
height zero, the next tier is for height one, and so on.

A tier consists of an empty line  (for readability) followed by several lines of
hexadecimal characters.  The top line within a tier  represents the northernmost
voxels in that tier; the bottom line represents the southernmost. Within a line,
each character represents  four voxels.  The first character represents the four
westernmost voxels;  the last character represents the four easternmost.  Within
a character, the highest binary digit (8s) represents the westernmost voxel, and
the lowest binary digit (1s) represents the easternmost.  If the binary digit is
a one, that voxel is filled; otherwise, it is empty.


## Compilation

The autograder will compile  your `main.cpp` file  and all other `.cpp` files in
the `voxhop` folder  whose names start with  capital letters.  Some helper files
are provided to get you started, but there's no requirement that you use them.

When compiling your program for the performance tests, the autograder will add
the `-O3` flag.


## Hints

<!-- - First make it work.  Then make it fast. -->
- For now, just make it work!  Performance tests are coming soon.
- Your program  will never be given an invalid map file.  It can still be useful
  to add error checks to your parser, though - it'll help catch parsing bugs.
- You don't need to find  the shortest route,  but finding short routes can help
  your program run faster.
<!-- - The performance tests make many queries per map,  -->

