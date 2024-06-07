# Profiling with GProf

> Premature optimization is the root of all evil.

Thus spake Donald Knuth, and he's right, as usual.  Programmers spend a lot of
time worrying about code that _feels_ slow, but doesn't actually contribute much
to the runtime of the program.  If you really want to improve your program's
runtime, you need to figure out what it spends most of its time doing, and
then focus on that.

There's a tool called `gprof` that can help you do this.  The process has three
main phases.  First, you compile your program with `g++` and enable profiling.
Then you run the profiled program.  Finally, you use `gprof` to display the
output.

`gprof` works on Linux, and should work on WSL without issues.  Non-WSL Windows
users and Mac users can find it pre-installed on CSIL.


## How to Use GProf

1. **Find a Test Case**

   Before you can test your program, you need some data to test it on. Find some
   data that takes your program a reasonable amount of time to process: at least
   a few seconds, but less than a minute.  Ten or fifteen seconds is perfect.

   If your test case requires input from the command line, save this input into
   a text file (in this example it's called `input.txt`).  This lets you send
   data directly to your program, so you don't measure the time it spends
   waiting for the user.


2. **Compile your Program**

   Compile as usual, but add the `-pg` and `-g` flags.  The `-pg` flag enables
   the profiler, and the `-g` flag adds debug symbols, which will improve the
   output.

   ```sh
   g++ -o path/to/program ... -g -pg whatever.cpp ...
   ```

   The program that gets created will automatically write profiling information
   as it runs, so it'll run slower than usual.


3. **Run your Program**

   Run the program that you just created.  Use the shell's `<` operator to send
   your `input.txt` file to the program's standard input.

   ```sh
   path/to/program arg1 arg2 < input.txt
   ```

   As it runs, it will create a file named `gmon.out` in your current directory.
   This file contains runtime statistics for your program.


4. **Run `gprof`**

   To see the results, run `gprof` and pass the path the the program that you
   profiled as the first command line argument.  If you want to use a profile
   other than the `gmon.out` file in the current directory, you can pass that
   as the second argument.

   ```sh
   gprof path/to/program
   ```

   This command will produce a _lot_ of output. There are two main sections: the
   Flat Profile and the Call Graph. Each section starts with a header explaining
   how to read it, but you can also find a more detailed explanation here:

   <https://ftp.gnu.org/old-gnu/Manuals/gprof-2.9.1/html_mono/gprof.html#SEC10>


5. **Optimize!**

   Now that you know what's taking up the most time, you're ready to optimize.
   Go for it!  Work on the slowest functions first.  See how much you can speed
   them up - or try to call them fewer times.


I've never  needed to do much more than this,  but `gprof` is a powerful program
with a lot more options.  If you're curious what else it can do, see the manual:

<https://ftp.gnu.org/old-gnu/Manuals/gprof-2.9.1/html_chapter/gprof_toc.html>
