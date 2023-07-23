from random import sample

"""
This file contains the code to generate a valid Sudoku puzzle of size N x N. 

Only creates puzzle with square subsquares.
"""


def generate_puzzle():
    """
    Generate a Sudoku puzzle of size N x N
    base is the size of the sub-grid, side is the size of the entire board
    :return: a list of strings, each string is a row of the puzzle
    """
    base = 3
    side = base * base

    def pattern(r, c):
        """
        Calculate the value at position (r, c) on a Sudoku board of size N x N using a pattern that ensures
        a baseline valid solution.

        Parameters:
            r (int): the row index, where 0 <= r < N.
            c (int): the column index, where 0 <= c < N.

        Returns:
            int: the value at position (r, c) on the Sudoku board.

        The pattern is based on the size of the board, N, and the position of the row and column within their
        sub-grids. Specifically, the formula is:

            (N * (r % S) + r // S + c) % N

        where S is the square root of N, and represents the size of each sub-grid. The formula calculates the
        index of the cell within its sub-grid, by taking into account the position of the row within its sub-grid
        (r % S), which sub-grid the row belongs to (r // S), and the column index (c). The result is then taken
        modulo N to ensure that the value is within the range of valid indices.

        This pattern ensures that the board has a baseline valid solution, which can be further randomized and
        modified to create a puzzle.
        """
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        """
        Randomize the sequence s in-place. The algorithm is based on the Fisher-Yates shuffle.
        :param s: the sequence to be shuffled
        :return: the shuffled sequence
        """
        return sample(s, len(s)) # uses sampling without replacement to shuffle the sequence

    rBase = range(base) # a number from 0 to N
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)] # shuffled list row indices
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)] # shuffled list col indices
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # replace 'empties' number of squares with 0
    squares = side * side
    #make 75% of the squares empty
    empties = int(squares * 0.75)
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    print("Board size:", side * side)
    for line in board: print(line)

    # Formatting the board
    puzzle_array = []

    for line in board:
        row_array = []
        for _ in line:
            string_value = str(_)
            row_array.append(string_value)
        puzzle_array.append(row_array)

    print("\nList of arrays: ")
    print(board)

if __name__ == '__main__':
    generate_puzzle()
