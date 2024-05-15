# Counter

In  this lab,  you'll  implement the  _map_  abstract data type.  This map  uses
strings as keys and integers as values,  and supports  fast lookup and update by
key.  This makes it perfect for a very common programming task: counting things.

This map also  supports iterators,  and iterating over the map  should visit the
keys in _insertion order_.  The first key added to the map will be the first key
visited, the second the second, and so on until reaching the most recently added
key at the very end of the iteration.  This is a convenient feature, and lots of
languages support it:  Ruby's default map type works like this, for example, and
Python provides the `OrderedDict` type.

Unlike maps that are ordered by key, these maps have an average O(1) runtime for
all of their functions.  They achieve this by storing their key-value pairs in a
doubly-linked list, and then using a hash table as an index into that list.  The
linked list  keeps the values in order,  and the hash table lets you jump to any
list node in constant time.

The full implementation can be a bit complicated,  so I recommend using only the
linked list at first,  then adding the hash table later.  See the Implementation
Guide section for more details.


## Your Assignment

- Implement the `Counter` class.  This will eventually use several components:
  - A `List` class that stores key-value pairs in insertion order.
  - An `Iterator` class that iterates over this `List`.
  - An `Index` class that allows fast lookups of `List` nodes.
  - Some `Counter` member functions to tie everything together.
- You may not use any [container classes][containers] from the standard library.
- Make sure your final code doesn't print anything.
- Make sure you don't have any memory leaks.
- Make your code run as fast as you can.


## The Counter

This counter is a map  from `std::string`s  to `int`s.  Any strings that are not
stored in the counter have an implicit count of zero,  and will not show up when
iterating over the counter. Strings that are stored in the counter have explicit
counts, and always show up when iterating, even if their counts are zero.

- The default constructor creates an empty `Counter`.
- The destructor cleans up any allocated memory.
- `begin()` returns an iterator to the first-inserted item in the counter.
- `count()` returns the number of keys stored in the counter.
- `dec(k, d)` decrements a count by a given value (default one).
- `del(k)` removes a key from the counter, setting its count to (implicit) zero.
- `end()` returns an invalid "end" iterator (see below).
- `get(k)` looks up a count by key.  If the key isn't present, it returns zero.
- `inc(k, d)` increments a count by a given value (default one).
- `set(k, v)` sets a count by key.
- `total()` returns the sum of all counts in the counter.

The `inc()`, `dec()`, and `set()` functions will add keys to the counter if they
are not already present.  The `del()` function is the only function that removes
keys; setting a value to zero does not remove the corresponding key.


### Counter Iterators

The `Counter` class contains a nested `Iterator` class, similar to the iterators
from the C++ standard library.  It's basically  a pointer to a linked list node,
and thus a pointer to one of the key-value pairs stored in the counter.

Your iterator must support the following functions and operators.  A constructor
is recommended, but not required.

- The `key()` function gets the key from the key-value pair that the iterator
  is currently referencing.
- The `value()` function gets the value from the key-value pair that the
  iterator is currently referencing.
- The  `++`  operator increments the iterator,  moving it to the  next key-value
  pair in the `Counter`.  If an iterator currently refers to the  last key-value
  pair, incrementing it should make it equal to the "end" iterator.
- The `==` and `!=` operators compare two iterators.

The "end" iterator is a special invalid iterator pointing  "one past the end" of
a counter.  This is used  to indicate that there are  no more key-value pairs to
iterator over.  It exists to allow loops like this:

```cpp
for(auto itr = counter.begin(); itr != counter.end(); ++itr) {
  std::cout << itr.key() << ": " << itr.value() << '\n';
}
```


## Performance

Part of your grade on this lab comes from performance. To make sure your counter
is implemented  efficiently,  the autograder will make sure it can process large
amounts of data in a  reasonable time frame.  This time is measured in  seconds,
not big-O, but with large data sets, the better your big-O runtime is the better
your real-time runtime will be.

There is extra credit available  for the fastest implementations!  The five best
programs will receive  10, 8, 6, 4, and 2  points of extra credit, respectively.
Only submissions made before the due date are eligible for extra credit.


## Implementation Guide

The final `Counter` class has a lot of parts. To help keep your code clean, it's
important to understand  what each part does,  and to keep the parts as separate
as possible.  This is the recommended strategy for for doing that.

1. Start by writing a doubly-linked list that stores `(std::string, int)` pairs.
   Use the `List.h` and `List.cpp` files for this, to keep things organized. The
   list should support  insertion at the tail,  finding the node that contains a
   given string, and removal of any node.

2. Next,  implement a counter in `Counter.h` and `Counter.cpp`.  Use a `List` to
   store key-value pairs. This will be slow, but that's okay: just get the basic
   (non-iterator) counter functions working for now.

   - At this point, you should be able to compile and run locally  (you may need
     to comment out the body of the  `print()` function  in `main.cpp` until you
     implement iterators).

3. Now add iterators.  Implement the `Counter::Iterator`  member functions  (and
   maybe a constructor) in `Iterator.cpp`.  Add the `begin()` and `end()` member
   functions to `Counter`.

   - At this point,  you should be able to pass all of the  correctness tests on
     Gradescope.  Your counter  will be too slow  to pass the performance tests,
     but that's okay for now.

5. Next, use `Index.h` and `Index.cpp` to write an `Index` class. This should be
   a hash table that maps `std::string`s  to linked list node pointers.  You can
   use either probing or chaining, and any hash function you want.

6. Finally, add an `Index` as a member variable in your `Counter` class.  Use it
   to speed things up by jumping directly to the list nodes you care about.

   - At this point, you should be able to attempt the performance tests.  If you
     don't get the performance you want,  try different hash functions, and make
     sure your hash table isn't getting too full.

The  final memory layout  will look  something  like this.  This diagram  uses a
probing  hash table for simplicity,  so each cell in `table` hold a pointer to a
list node.
```
 Counter
+------------------+
|  Index           |        0   1   2   3   4   5   6   7   8
| +--------------+ |      +---+---+---+---+---+---+---+---+---+
| | table      *--------->| * |   | * |   |   |   | * |   |   |
| +--------------+ |      +--\+---+/--+---+---+---+-|-+---+---+
| | count    = 3 | |          \   /                 |
| +--------------+ |           \ /                  |
| | capacity = 9 | |            X                   |
| +--------------+ |           / \                  |
|                  |          /   \                 |
|  List            |         /     \                |
| +--------------+ |        V       V               V
| | head       *------->[one: 1]<->[two: 2]<->[three: 3]<---\
| +--------------+ |                                        |
| | tail       *--------------------------------------------/
| +--------------+ |
|                  |
| count        = 3 |
| total        = 6 |
+------------------+
```


## Hints

- All `int`s are valid counts, including zeros and negative numbers.
- When a key is removed from a counter, it should no longer show up when
  iterating over that counter.  If it gets re-inserted later, it should show
  up at the end of the iteration (not in its previous position).
- When running performance tests, the grader will compile your code with the
  `-O3` option to enable most compile-time optimizations.
- When using the interactive interface in `main.cpp`, note that for commands
  that take a count or value argument, this should come before the key.
- For performance reasons, it's important to use a doubly-linked list and not
  a singly-linked list.  Why?


[containers]: https://cplusplus.com/reference/stl/
