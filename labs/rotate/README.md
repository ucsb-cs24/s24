# Rotate

In this lab,  you'll implement a _sorted sequence_ abstract data structure using
a _binary search tree_ as the underlying concrete data structure.  In an attempt
to keep the tree balanced,  you'll perform some simple tree rotations after each
`insert()` or `remove()` operation.


## Your Assignment

- Implement a binary search tree in the `.h` and `.cpp` files provided:
  - Declare a binary tree node type called `Node` in `Node.h`.
  - Implement any `Node` member functions (or helper functions) in `Node.cpp`.
  - Implement the `Tree` member functions declared in `Tree.h` in `Tree.cpp`.
- You can't use any [container types][containers] from the standard library.
- Make sure your final code doesn't print anything unexpected.
- Make sure you don't have any memory leaks.


## The Tree

Your tree should store `std::strings` in sorted order, and it should support the
following  public  member functions.  Details of the output format and balancing
process are explained in the following sections.

- The default constructor should create an empty tree.
- The destructor should clean up all memory owned by the tree.
- `clear()` removes all items from the tree.
- `count()` reports the number of items in the tree.
- `contains()` reports whether or not a given item exists in the tree.
- `find()` returns the first index of an item  in the sorted sequence.  If there
  are multiple copies of the item, it returns the smallest index. If the item is
  not present in the tree,  it returns the maximum value that can be stored in a
  `size_t`.
- `insert()` adds an item to the tree as a leaf node.  If that item is already
  present in the tree, you will encounter it on your way down to a leaf node; if
  this happens, insert the new item into the old item's left subtree.
- `lookup()` returns the item at a given index.  If the index is invalid, it
  throws a `std::out_of_range` exception.
- `print()` prints the tree in tree notation, as explained below, followed by a
  newline.
- `remove()` removes the item at a given index.  If the index is invalid, it
  throws a `std::out_of_range` exception.
  - If the item to be removed is on a leaf node, simply remove it.
  - If the item to be removed is on a node with one child, that child takes the
    node's place.
  - If the item is on a node with two children, find the node `n` that contains
    the item at the next greater index.  Swap the values of the two nodes and
    remove node `n`.  Node `n` is guaranteed to have one or zero children.

After performing an  `insert()` or a `remove()`,  your code should rebalance the
tree.  This process is described in the Rebalancing section, below.


## Tree Notation

A user-friendly depiction of a binary tree might look something like this:

```
    d
   / \
  b   e
 / \   \
a   c   f
```

But this is  very hard to print.  Tree notation  is an easier way to print trees
while keeping the output somewhat readable.  For example,  the tree notation for
the tree pictured above would be:

```
((a b c) d (- e f))
```

More formally:
- The tree notation for a leaf node is simply its value.
- The tree notation for a non-existent node is a hyphen (`-`; ASCII value 45).
- The tree notation for a non-leaf node is:
  - A left parenthesis, followed by
  - the tree notation for its left subtree, followed by
  - a space, followed by
  - the node's value, followed by
  - a space, followed by
  - the tree notation for its right subtree, followed by
  - a right parenthesis.
- The tree notation for an empty tree is a hyphen.


## Rebalancing

After an `insert()` or `remove()` operation, your tree should attempt to balance
itself by performing some tree rotations; this lab calls these _promotions_. The
full procedure is as follows:

- Walk back up the tree, starting from the parent of the node that was added or
  removed and ending at the root.
- At each node, consider promoting the child that got (relatively) heavier.
  - After an insert, this is the root of the subtree that was inserted into.
  - After a remove, this is the root of the subtree that was _not_ removed from.
- Only promote nodes when the promotion would improve the _balance_ of the
  resulting subtree, as described below.

Note that a non-existent child cannot be promoted. Additionally, when "removing"
a node with two children,  it is actually some other node `n` that gets removed.
In this case, when walking back up the tree, start at `n`'s parent.

### Promotions

This tree uses a simple rotation scheme called a _promotion_ (sometimes known as
a _single rotation_). When performing a promotion, the root of a subtree selects
one of its children, and promotes  that child to be the new root of the subtree.
For example, promoting `D` in the left tree below results in the right tree, and
promoting `B` in the right tree results in the left tree.

```
...              ...
  \                \
   B      ===>      D
  / \              / \
 a   D    <===    B   e
    / \          / \
   c   e        a   c
```

### Weight and Balance

In an effort to keep itself balanced, the tree only promotes nodes under certain
conditions. Specifically, it defines a metric called _balance_, and only promotes
nodes when this operation would improve the balance of a subtree:

- The _weight_ of a node is the number of nodes in the subtree rooted at that
  node (including the node itself).
- The _imbalance_ of a subtree is the absolute value of the difference between
  the weights of the children of the root of that subtree.
- The _balance_ of a subtree is the negation of its imbalance.  An operation
  that increases balance decreases imbalance, and vice versa.

These are the weights and balances of all subtrees in the left tree above.

| Root | Weight | Imbalance | Balance | Nodes in Subtree        |
|:-----|-------:|----------:|--------:|:------------------------|
| `a`  |      1 |         0 |       0 | `a`                     |
| `B`  |      5 |         2 |      -2 | `a`, `B`, `c`, `D`, `e` |
| `c`  |      1 |         0 |       0 | `c`                     |
| `D`  |      3 |         0 |       0 | `c`, `D`, `e`           |
| `e`  |      1 |         0 |       0 | `e`                     |


### An Example

This is the simplest example of an insert that would result in a promotion.

```
(1) a       (2) a       (3) b
     \           \         / \
      b           c       a   c
       \         /
        c       b
```

Suppose you have  just attached  node `c`,  as part of an  `insert()` operation,
generating  tree `(1)`.  You would then look at the  nodes you passed through to
reach `c`, considering promotions.

- First,  you would look at node `b`.  Since you just inserted into  `b`'s right
  subtree, you would consider promoting `b`'s right child, `c`.  This would make
  tree `(2)`. But the balance of the `bc` subtree wouldn't improve, so you would
  not perform this promotion.
- Then  you would look at  node `a`.  Since you  just inserted into  `a`'s right
  subtree, you would consider promoting `a`'s right child, `b`.  This would make
  tree `(3)`,  and this _would_ improve the balance of the `abc` subtree, so you
  would perform this promotion.
- You have now passed the root of the tree,  and there are no more promotions to
  consider.  The final result of the insert operation is tree `(3)`.


## Hints

- Recursion works very, very nicely with trees.
- You can pass most of the tests without implementing rotations or `remove()`; I
  suggest you ignore these at first.  Once your other functions are working, add
  rotations and make sure you pass all the `insert()` tests. Save `remove()` for
  last.
- You may need to perform multiple promotions after a single insert or remove.
- The index  of an item  in the sorted sequence  is the same as  its index in an
  in-order traversal of the tree.  As a corollary, the index of the root item is
  the weight of its left subtree.
- You  may want to store  subtree weights  on each node.  This will make indexed
  operations faster, but you'll have to keep these weights up to date.
- The autograder  will use your `insert()`, `print()` , and `count()`  functions
  to build and inspect your tree,  so those will need to work before you can get
  useful output from Gradescope.
- If you store your child pointers as an array,  you can write one function that
  can promote either child.  Use `1 - i` or `i ^ 1` to toggle your indices.
- The `this` argument to a C++ member function is never supposed to be null, and
  the compiler will complain if you check this.  So it may be easier to make any
  recursive helper functions global functions or static (class) functions.
- The rotation scheme  described here doesn't guarantee that  the tree will have
  `O(log n)` performance.  Can you find an access pattern that's `O(n)`?


[containers]: https://cplusplus.com/reference/stl/
