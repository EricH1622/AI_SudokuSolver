import math


class GridHelper:
    """
    Gathers initial information about the puzzle and the board to use for running the solution.
    """

    @staticmethod
    def initialize_grid_counts(grid: list) -> (int, int, int):
        """
        Calculates the number of subgrids, number of rows per subgrid, numer of col per subgrid and returns
        as a tuple.
        :return: subgrid_count, rows_in_subgrid, cols_in_subgrid as a tuple
        """
        subgrid_count = len(grid)
        temp = math.sqrt(subgrid_count)
        if temp % 1 == 0:  # if 9x9, 16x16, 25x25, 100x100, this will be 0
            cols_in_subgrid = int(temp)  # 3 subgrids per row of a 9x9, 4 subgrids per row of a 16x16, and so on
            rows_in_subgrid = int(temp)
        else:
            cols_in_subgrid = 4  # case of 12x12 sudoku board, with 4 col x 3 row subgrids
            rows_in_subgrid = 3
        return subgrid_count, rows_in_subgrid, cols_in_subgrid

    @staticmethod
    def is_solved(grid: list) -> bool:
        """
        Checks board for empty squares.
        :return:true if no empty squares are found, else false
        """
        for row in grid:
            if 0 in row:
                return False
        return True

    @staticmethod
    def grab_empty_square(grid: list) -> (int, int):
        """
        Returns the first empty square found.
        :return: row, col as tuple
        """
        for row, row_values in enumerate(grid):
            try:
                return row, row_values.index(0)
            except ValueError:  # occurs when no value found
                pass

    @staticmethod
    def get_subgrid_origin(row: int, col: int, rows_in_subgrid: int, cols_in_subgrid: int) -> (int, int):
        """
        Returns the top-left row,col of the subgrid

        :param row: square's row
        :param col: square's col
        :param rows_in_subgrid: an int
        :param cols_in_subgrid: an int
        :return: row and col of top-left subgrid as a tuple
        """
        # example want subgrid 2
        o_row = rows_in_subgrid * int(row / rows_in_subgrid)
        o_col = col - (col % cols_in_subgrid)
        return o_row, o_col

    @staticmethod
    def get_row_values(grid: list, row: int) -> [int]:
        """
        Fetches all values in the specified row

        :param grid: a list
        :param row: row to fetch values from
        :return: list of values currently in row
        """
        return grid[row]

    @staticmethod
    def get_col_values(grid: list, col: int) -> [int]:
        """
        Fetches all values in the specified col

        :param grid: a list
        :param col: col to fetch values from
        :return: list of values currently in col
        """
        return [row[col] for row in grid]

    @staticmethod
    def get_subgrid_values(grid: list, row: int, col: int, rows_in_subgrid: int, cols_in_subgrid: int) -> [int]:
        """
        Fetches all values in the subgrid for the specified row and col

        :param grid: a list
        :param row: square's row
        :param col: square's col
        :param rows_in_subgrid: an int
        :param cols_in_subgrid: an int
        :return: list of values currently in the subgrid
        """
        subgrid_values = []
        o_row, o_col = GridHelper.get_subgrid_origin(row, col, rows_in_subgrid, cols_in_subgrid)
        for r in range(0, rows_in_subgrid):
            for c in range(0, cols_in_subgrid):
                if grid[o_row + r][o_col + c] != 0:
                    subgrid_values.append(grid[o_row + r][o_col + c])
        return subgrid_values

    @staticmethod
    def get_all_possible_values(grid: list, row: int, col: int, subgrid_count: int, rows_in_subgrid: int,
                                cols_in_subgrid: int):
        """
        Fetches all the currently used values in the row, col, and subgrid

        :param grid: a list
        :param row: square's row
        :param col: square's col
        :param subgrid_count: an int
        :param rows_in_subgrid: an int
        :param cols_in_subgrid: an int
        :return: list of values currently in the row, col, and subgrid
        """
        used_values = set()
        used_values.update(GridHelper.get_row_values(grid, row))
        used_values.update(GridHelper.get_col_values(grid, col))
        used_values.update(GridHelper.get_subgrid_values(grid, row, col, rows_in_subgrid, cols_in_subgrid))
        available_values = [n for n in range(1, subgrid_count + 1) if n not in used_values]
        return available_values

    @staticmethod
    def print_puzzle(grid: list):
        """
        Helper function to print the puzzle as a grid.
        """
        for row in grid:
            print(row)

    @staticmethod
    def get_min_value_count(grid: list, subgrid_count: int, rows_in_subgrid: int, cols_in_subgrid: int) -> (int, int):
        """
        Gets the square with the smallest domain.

        :param grid: a list
        :param subgrid_count: an int
        :param rows_in_subgrid: an int
        :param cols_in_subgrid: an int
        :return: a tuple of ints
        """
        min_count = subgrid_count
        empty = ()
        for row, row_values in enumerate(grid):
            for col, square_value in enumerate(row_values):
                if grid[row][col] == 0:
                    num_options = len(GridHelper.get_all_possible_values(grid, row, col, subgrid_count, rows_in_subgrid,
                                                                         cols_in_subgrid))
                    if num_options == 1:
                        return row, col
                    if num_options < min_count:
                        min_count = num_options
                        empty = (row, col)
        return empty
