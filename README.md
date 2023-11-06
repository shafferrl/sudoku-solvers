# sudoku-solvers
Sudoku-solving program in various stages of evolution from command line interface to object-oriented web app module.

## Project(s) Overview ##

The first program in this repository ("sudoku_solver_v1") was the first non-trivial project I undertook after learning Python, after having played sudoku for many years and feeling like the process of solving a sudoku puzzle by hand was programmatic in a way.  This repo actually comprises multiple projects, however, that built upon the original project over the course of months of learning both Python and web development.

A little effort has gone into cleaning up the code's formatting, but it still bears the marks of having been written by someone who had been learning Python for roughly a month when the first version was fully functional and was just beginning to scratch at the surface of appropriate situations for object-oriented programming with Python.

It should be noted that none of the project's iterations thus far determine whether or not a set of inputs provide a unique solution.  Any set of inputs above a certain lower bound will return the first solution encountered by the solver, provided that set has at least one solution.

## Project(s) Evolution ##

"sudoku_solver_v1":  This is essentially the first iteration or stage of evolution for this project.  This version of the program was designed to work in the Python shell and retrieve input from the user as comma-separated row/column values for the coordinates at which each of the nine numbers are intially entered into the puzzle.  Due to the tedium of having to enter numbers in this manner when debugging, there are also several puzzles that have been hard-coded into the program, and the user input section is bypassed entirely.

"sudoku_hacker_v1":  The original puzzle was modified to work as a GUI desktop app using Python's tkinter library.  The user clicks on puzzle cells to increment the value to the appropriate initial input and clicks a "solve puzzle" button to attempt to solve the puzzle.  Cell values obey sudoku rules when clicked, meaning a conflict in a row, column, or 3x3 box will be incremented past until an acceptable value is reached, and each cell cycles back to blank after 9 is reached.

"sudoku_hacker_v2":  This is an update of the "v1" GUI desktop application, which improved some quirks in the user interface, used list comprehensions (then newly discovered) where appropriate to reduce lines of code, added an icon, and made some of the code more maintainable.  It should be noted that even with updates, the "about" popup window was sized statically in pixel units on Windows 10 and does not display properly on Linux and possibly Mac (has not been tested).  This has not been corrected since tkinter and desktop apps more generally have since been abandoned in favor of web apps.

"sudoku_hacker_raw_algorithm":  Well after having written the previous two/three iteratons of this project, the desire arose to incorporate the sudoku solver into a web page.  The original code was subsequently modified for a more object-oriented approach in addition to being able to return feedback to the client in the event of a failure to solve the given inputs.  The web-based interface can be accessed at https://ryanludwigshaffer.com/projects/sudoku-solver/
