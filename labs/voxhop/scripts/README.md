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
