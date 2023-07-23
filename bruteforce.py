from gridhelper import GridHelper


class BruteForceSolver:

    def __init__(self, sudoku_grid: list):
        """
        Initialize an object of type BruteForceSolver.
        :param sudoku_grid: a 2D list of integers, each representing a square in the sudoku board to be solved
        """
        self._sudoku_grid = sudoku_grid
        self._subgrid_count, \
            self._rows_in_subgrid, self._cols_in_subgrid = GridHelper.initialize_grid_counts(self._sudoku_grid)

    @property
    def sudoku_grid(self):
        """
        Retrieve the current BruteForceSolver's sudoku board.
        :return: a 2D list of ints, represeting the sudoku board to be solved
        """
        return self._sudoku_grid

    def solve(self) -> list:
        """
        Solves the sudoku puzzle using a brute force algorithm with reduced search size. The algorithm uses a
        backtracking approach and is naive, except the creation of a list of possible, valid numbers to
        iterate and backtrack through.

        :return: solved sudoku grid in a list else and empty list if no solution found
        """
        if GridHelper.is_solved(self._sudoku_grid):
            return self._sudoku_grid
        # Get first encounter of empty square
        row, col = GridHelper.get_min_value_count(self._sudoku_grid,
                                                  self._subgrid_count,
                                                  self._rows_in_subgrid,
                                                  self._cols_in_subgrid)
        # Get available values for empty square
        possible_values = GridHelper.get_all_possible_values(self._sudoku_grid,
                                                             row,
                                                             col,
                                                             self._subgrid_count,
                                                             self._rows_in_subgrid,
                                                             self._cols_in_subgrid)
        if possible_values:
            for value in possible_values:
                self._sudoku_grid[row][col] = value
                self.solve()
                if GridHelper.is_solved(self._sudoku_grid):
                    return self._sudoku_grid
                self._sudoku_grid[row][col] = 0
        return []
