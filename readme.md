# AI Sudoku Solver Project

## Group Members

- Sharon H.
- Wilson S.
- Eric H.
- Alissa

This project was created for our Introduction to Artificial Intelligence course. It is written in python and implements two algorithms for solving Sudoku puzzles: brute force and constraint satisfaction problem (CSP). The user can choose to load a puzzle from a file or generate a random puzzle. The program will handle puzzles of size 9x9, 12x12(4 rows, 3 columns), 16x16, and 25x25. The user can then choose either algorithm to solve the puzzle. A solution, should one exist, will be displayed along with the time taken to solve the puzzle.

## Running the Program

### Requirements
1. Python. The latest version can be downloaded and installed from the official Python website (https://www.python.org/)

To run the program navigate to the folder in which the project is saved in and run the following command: `python3 main.py` and the Tkinter GUI window will open.


## Algorithm Notes

### Brute Force Algorithm

For the Brute Force Algorithm, we implemented a naive recursive backtracking brute-force algorithm based on the pseudocode in the book "Artificial Intelligence: A Modern Approach." After testing this version of the algorithm, we added a heuristic that reduced the available numbers that the algorithm would iterate through to only valid ones. These valid numbers were determined by checking a square's neighbours and determining which numbers had already been inserted into the board.

### CSP Algorithm

Our CSP (Constraint Satisfaction Problem) algorithm is also based on the pseudocode in the book "Artificial Intelligence: A Modern Approach." It implements MAC (Maintaining Arc Consistency), MRV (Minimum Remaining Values), and LCV (Least Constraining Value) in addition to backtracking. The general flow of the algorithm is to first apply the MRV algorithm to the unassigned squares, then apply the Degree Heuristic where there are more than one square at the end of MRV. Then, the LCV algorithm is applied to the square's domain to determine the optimal order of valid values to iterate through. Finally, the recursive backtracking algorithm is used to repeat this process until a solution is found.

## Notes on This Program

### Resources Used

#### Puzzle Generation

- Alain T. [StackOverflow](https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
- Jeff S. [py-sudoku](https://pypi.org/project/py-sudoku/)

#### GUI/Tkinter

- Gangwar, M. (2022, August 3). [Advanced Tkinter Working with Classes Tutorial](https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes)
- codemy.com (n.d.). [Adding a Full Screen ScrollBar - Python Tkinter GUI Tutorial #96](https://www.youtube.com/watch?v=0WafQCaok6g)
- (n.d.). [Python - GUI Programming (Tkinter)](https://www.tutorialspoint.com/python/python_gui_programming.htm)
- Amos, D. (n.d.). [Python GUI Programming With Tkinter](https://realpython.com/python-gui-tkinter/)

#### Brute Force Algorithm

- "Artificial Intelligence: A Modern Approach" - Norvig, Russell (Textbook and Programming Resources)

#### CSP Algorithm

- "Artificial Intelligence: A Modern Approach" - Norvig, Russell (Textbook and Programming Resources)
- Meerson, Farkash, & Korzac. (2018, August 23). [Sudoku](copy enclosed in zip file).
- Lathrop. (2020). [Chap 6b CSPs Constraint Propagation Structure](https://www.ics.uci.edu/~rickl/courses/cs-171/cs171-lecture-slides/2020_WQ_CS171/chap_6_b_CSPs_Constraint_Propagation_Structure.pdf)

## Figma Prototype

Check out the Figma prototype for our AI Sudoku Solver [here](https://www.figma.com/proto/L8Fjcqn52Kf37M5R27gWwB/Sudoku-Puzzle?node-id=15-233952&scaling=scale-down&page-id=0%3A1&starting-point-node-id=15%3A233952).
