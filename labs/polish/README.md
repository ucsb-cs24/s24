# Polish

In this lab, you'll implement a simple calculator and equation converter.  It'll
parse expressions written in [reverse Polish notation][rpn].  Then, depending on
a command line argument, it will do one of the following:

- Print the expression in [Polish notation][pn].
- Print the expression in reverse Polish notation.
- Evaluate the expression and print the result.

Your calculator should operate on `double`s and support the following operators.

- `+` adds two numbers (`3 4 +` is `7`).
- `-` subtracts one number from another (`2 6 -` is `-4`).
- `*` multiplies two numbers (`2 7 *` is `14`).
- `/` divides one number by another (`7 -4 /` is `-1.75`).
- `%` returns the remainder after dividing one number by another (`0.7 0.3 %` is `0.1`).
- `~` negates a single number (`8 ~` is `-8`).

Your calculator should read one line of input at a time, print some output, then
move on to the next line.  It should exit  when it reaches the end of the input.
Use `Ctrl+D`  to simulate this on Mac and Linux, or `Ctrl+Z` followed by `Enter`
on Windows.


## Definitions

All the following examples are representations of this equation, written here in
standard (infix) notation.  It evaluates to 67.5.

```
(12 + 3) * ((5 + 4) / 2)
```

### Polish Notation

In Polish notation, also known as prefix notation, the operator comes before its
arguments.

```
* + 12 3 / + 5 4 2
```

### Reverse Polish Notation

In reverse Polish notation, also known as postfix notation, the operator comes
after its arguments.

```
12 3 + 5 4 + 2 / *
```

### Abstract Syntax Tree

An abstract syntax tree  is a tree representing the steps of a computation.  For
an expression, each leaf node represents a number, and the other nodes represent
operations on those numbers.  Every operation uses the values of its children as
input, so the root of the tree is the last operation to happen.

```
       (*)
      /   \
    (+)   (/)
   /  |   |  \
 12   3  (+)  2
        /   \
       5     4
```


## Your Assignment

- Implement the calculator components described below.
- You can't use any container types from the standard library.
- Make sure your code doesn't print anything unexpected.
- Make sure you don't have any memory leaks.


### The Abstract Syntax Tree

The `AST` class defined in `AST.h` is the base class for all AST nodes. It lists
the functions that every AST node must implement.  However, it doesn't implement
these functions itself -- this makes it an "abstract" class,  which can never be
instantiated directly.

In order to create an AST, you'll need to be able to create AST nodes. So you'll
need to create some non-abstract subclasses of `AST`. You'll want a number class
and some operator classes: declare these in `Nodes.h` and implement their member
functions in `Nodes.cpp`.


### The Stack

Parsing reverse Polish notation  requires a stack  that stores  pointers  to AST
nodes.  Declare this class in  `Stack.h`  and implement its  member functions in
`Stack.cpp`.


### Parsing

The `AST::parse()` function in `AST.cpp`  creates an AST from its reverse Polish
notation representation. It takes a string as an argument and iterates over each
(whitespace-separated) token in the string.  If the token is a number, it pushes
it onto the stack.  If the token is an operator, the function pops its arguments
off of the stack and pushes the new operator onto the stack. When it reaches the
end of the string, there should be  exactly one AST node  on the stack:  this is
the root of the final AST.

Implement this function using your stack class and your AST subclasses.

A token is either one of the operators listed above or a number. A number is one
or mode decimal digits.  It may optionally include a leading sign  (`+` or `-`),
and/or a trailing fractional part (`.` followed by one or more decimal digits).

You may run into some invalid inputs while parsing.  When you do, throw a
`std::runtime_error` with the appropriate error message:

- If there is nothing on the stack at the end of parsing, say `No input.`
- If there are multiple nodes on the stack at the end of parsing, say `Too many operands.`
- If there aren't enough operands for an operator, say `Not enough operands.`
- If you encounter an invalid token, say `Invalid token: XXX`, where `XXX` is
  the invalid token.


### Output

Your AST node subclasses need to support the following output functions.

- `AST::prefix()` returns a string representation of the subtree rooted at the node.
  This string is in Polish notation, with tokens separated by single spaces.
- `AST::postfix()` returns a string representation of the subtree rooted at the node.
  This string is in reverse Polish notation, with tokens separated by single spaces.
- `AST::value()` returns the value of the subtree rooted at the node.

In the `value()` function,  you may encounter cases  where you attempt to divide
(or take the remainder after dividing) by zero.  If this happens, throw a
`std::runtime_error` with the message `Division by zero.`


## Hints

- A `std::istringstream` may be helpful for parsing strings into tokens.
- Be careful while parsing numbers:
  - Some parsing methods will parse `+` and `-` as the number zero.
  - The tokens `tuba` and `2ba` are both invalid, but many parsing methods will
    parse the latter as the number two, ignoring the rest of the string.
- The `double` type doesn't support the `%` operator,  but the `fmod()` function
  from the `cmath` header will compute what you need.
- Beware of memory leaks! If you encounter an invalid token, make sure you clean
  up any nodes you've already constructed. These may be on the stack (making the
  stack destructor clean up any remaining nodes will take care of this), or they
  may be in local variables in your `parse()` function.
- <https://xkcd.com/645/>


[pn]:  https://en.wikipedia.org/wiki/Polish_notation
[rpn]: https://en.wikipedia.org/wiki/Reverse_Polish_notation
