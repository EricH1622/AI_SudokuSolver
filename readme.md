## AI Sudoku Solver Project - Group 3
### Group Members: <br>
Sharon H. <br>
Wilson S. <br>
Eric H. <br>
Alissa 

Figma Prototype: <br>
https://www.figma.com/proto/L8Fjcqn52Kf37M5R27gWwB/Sudoku-Puzzle?node-id=15-233952&scaling=scale-down&page-id=0%3A1&starting-point-node-id=15%3A233952

### Algorithm Notes
#### Brute Force Algorithm
For the Brute Force Algorithm, we implemented a naive recursive backtracking bruteforce algorithm based on the pseudocode 
in Artificial Intelligence: A Modern Approach. After testing this version of the algorithm, we added in a heuristic
that reduced the available numbers that the algorithm would iterate through to only valid numbers. These valid numbers
were determined by checking a square's neighbours and determining which numbers had already been inserted into the board.

#### CSP Algorithm
Our CSP algorithm is based on the pseudocode in Artificial Intelligence: A Modern Approach. It implements MAC, MRV, 
and LCV in addition to Backtracking. The general flow of the algorithm is to first apply the MRV algorithm to the
unassigned squares, then apply the Degree Heuristic where there are more than one Squares at the end of MRV. Then,
the LCV algorithm is applied to the Square's domain to determine the optimal order of valid values to iterate through.
Finally, the recursive backtracking algorithm is used to repeat this process until a solution is found.

### Notes on this program:
<b>Resources Used:</b><br>
Puzzle Generation:<br>
1. Alain T. https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
2. Jeff S. https://pypi.org/project/py-sudoku/

GUI/Tkinter:<br>
1. Gangwar, M. (2022, August 3). Advanced Tkinter Working with Classes Tutorial. Digital Ocean. https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
2. codemy.com (n.d.). Adding a Full Screen ScrollBar - Python Tkinter GUI Tutorial #96. Youtube. https://www.youtube.com/watch?v=0WafQCaok6g
3. (n.d.). Python - GUI Programming (Tkinter). TutorialsPoint. https://www.tutorialspoint.com/python/python_gui_programming.htm
4. Amos, D. (n.d.). Python GUI Programming With Tkinter. Real Python. https://realpython.com/python-gui-tkinter/

Brute Force Algorithm:<br>
1. "Artificial Intelligence: A Modern Approach" - Norvig, Russell (Textbook and Programming Resources)

CSP Algorithm:<br>
1. "Artificial Intelligence: A Modern Approach" - Norvig, Russell (Textbook and Programming Resources)
2. Meerson, Farkash, & Korzac. (2018, August 23). Sudoku. The Hebrew University of Jerusalem. Retrieved March 2023, from copy enclosed in zip file.
3. Lathrop . (2020). Chap 6b CSPs Constraint Propagation Structure. Retrieved March 2023, from https://www.ics.uci.edu/~rickl/courses/cs-171/cs171-lecture-slides/2020_WQ_CS171/chap_6_b_CSPs_Constraint_Propagation_Structure.pdf
