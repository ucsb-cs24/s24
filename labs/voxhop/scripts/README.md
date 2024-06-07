# Scripts

These are the scripts used to generate (most of) the maps on Gradescope. You can
use them to create  some large test files for testing locally.  To create a map,
use the `generate.py` script, and redirect its output to a file:

```sh
path/to/generate.py maptype [options] > path/to/new-map-file.vox
```

There are  a bunch of different `maptype`s.  Run `generate.py maptype --help` to
see what options each type needs.


Once you have a map, you can use the `testcase.py` script to generate test cases
for it.  For example, to generate one thousand queries:

```sh
path/to/testcase.py -n 1000 path/to/new-map-file.vox > path/to/tests.tsv
```

Some map types don't have many routes upward; some have none.  When generating
test cases for these maps, add the `-f prob` flag.  This is a probability that
test points with a lower source point than destination point will be swapped -
this reduces the number of tests with no valid route.  For example, to swap
seventy-five percent of the cases that would have needed an upward path:

```sh
path/to/testcase.py -f 0.75 ...
```


## The Test Cases

These are the commands I used to generate the performance test cases.  You won't
get the exact same maps,  because there are random numbers involved,  but you'll
get maps  of the same style and scale,  which will be helpful  for running large
tests locally.

### Great Wall

```sh
path/to/generate.py greatwall --amplitude 30  300 325
```

### Skywalk

```sh
path/to/generate.py skywalk --min-clusters 10 --max-clusters 20  24 32 24
```

This map only has downward routes.  When generating test cases, add `-f 0.90` to
flip 90%  of the upward routes, ensuring that the majority of the resulting test
cases have valid solutions.

### World of Goo

Note: this is  _very_  slow for large maps.  Don't forget to use `>` to redirect
your output to a file!

```sh
path/to/generate.py goo 100
```

This map also has  mostly downward routes;  the performance tests were generated
with `-f 0.66` to increase the number of valid routes.

The Goo Ball map is a smaller version, which generates comparatively quickly:

```sh
path/to/generate.py goo 32
```


### Mines of Solomon

```sh
path/to/generate.py mines --shafts 10  24 24 32
```

This map is hard to visualize,  'cause it's mostly underground.  You can use the
"clip" feature of the map viewer to see individual strata, but this isn't always
convenient, so I added a debug mode: add the `--debug` flag while generating the
map to invert  filled and empty voxels.  The result isn't a valid test case, but
it's a lot easier to visualize.

### Kowloon

```sh
path/to/generate.py towers --constant-growth 2 --random-growth 3  10 11 9
```

The  Tower Block map is a smaller version of this map.  The command for that one
is something like:

```sh
path/to/generate.py towers --constant-growth 2 --random-growth 2  3 4 4
```
