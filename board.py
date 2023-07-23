"""
Creates the Squares (csp variables) each which a value and domain to be used in the CSP algorith. Builds these squares
into a board so that locations remain intact from sudoku puzzle.
"""

from gridhelper import GridHelper


class Square:
    def __init__(self, value: int, position: (int, int)):
        """
        Creates a Square object which contains the domain of potential values
        and the value that it was given on the board.
        """
        self._value: int = value  # value of the square
        self._domain: list[int] = []  # possible values for an unassigned square
        self._prev_domain: list[[int]] = []  # values previously used for domain
        self._constraints: list[Square] = []  # list of neighbouring squares
        self._position: (int, int) = position

    def add_to_domain(self, value: int):
        """
        Adds the potential values to the domain.

        :param value: an Int
        """
        if value not in self._domain:
            self._domain.append(value)

    def add_constraint(self, *squares: 'Square'):
        """
        Adds a constraint to a Square's constraint list.

        :param squares: a list of Square objects
        """
        for square in squares:
            if square != self and square not in self._constraints:
                self._constraints.append(square)

    def __str__(self):
        """
        Provides a formatted string representation of a Square.

        :return: a String, representing a Square
        """
        return f"Square({self.position}) " \
               f"\nConstraints:{self.constraints}"

    @property
    def value(self) -> int:
        """
        Retrieves a Square's value.

        :return: an int, representing a Square's value (if zero, square is empty)
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets a Square's value.

        :param value: an int, representing the Square's value (if zero, square is empty)
        """
        self._value = value

    def assign_value(self, value):
        """
        Assigns a value to a Square and updates its domain accordingly. The domain will be reduced to include only the
        value of the Square.

        :param value: an int, other than zero, representing the Square's value
        """
        self._value = value
        # self.domain.remove(value)
        self._prev_domain.append(self._domain)
        self._domain = [value]

    def unassign_value(self):
        """
        Resets a Square's value to zero (empty). The Square's domain is reset to its most recent state prior to the
        assignment of a value.
        """
        self._value = 0
        prev_domain = self._prev_domain.pop()
        self.domain.clear()
        if isinstance(prev_domain, list):
            for value in prev_domain:
                self.add_to_domain(value)
        else:
            self._domain.append(prev_domain)

    @property
    def domain(self) -> list[int]:
        """
        Retrieves the domain of the Square.

        :return: a list, representing the Square's domain
        """
        return self._domain

    @domain.setter
    def domain(self, values: list[int]):
        """
        Sets the domain of the Square.

        :param values: a list, representing the domain of the Square
        """
        self._domain = values

    @property
    def prev_domain(self):
        """
        Retrieves the Squares domain prior to the most recent assignment of a value.

        :return: a list, representing the Square's previous domain
        """
        return self._prev_domain

    @property
    def domain_size(self) -> int:
        """
        Retrieves the size of the Square's domain.

        :return: an int, representing the size of the Square's domain
        """
        return len(self._domain)

    @property
    def position(self) -> (int, int):
        """
        Retrieves the square's position on the sudoku board as an (x,y) coordinate.

        :return: a tuple of two ints, representing the square's location on the sudoku board
        """
        return self._position

    @property
    def row(self) -> int:
        """
        Retreives the row in which the Square exists on the sudoku board.

        :return: an int, representing the Square's y-coordinate on the sudoku board
        """
        return self._position[0]

    @property
    def col(self) -> int:
        """
        Retrieves the column in which the Square exists on the sudoku board.

        :return: an int, representing the Square's x-coordinate on the sudoku board
        """
        return self._position[1]

    @property
    def constraints(self) -> list['Square']:
        """
        Retrieves the Square's constraints.

        :return: A list of Square objects, representing the neighbours of the current Square that act to constrain its
        domain
        """
        return self._constraints

    def constraints_to_str(self) -> str:
        """
        Converts a Square's constraints into a human-readable string.

        :return: a String, representing all of a Square's constraints
        """
        constraints_str = ""
        for constraints in self._constraints:
            constraints_str += str(constraints.position)
        return constraints_str

    def count_unassigned_constraints(self) -> int:
        """
        Determine the number of constraints acting on a Square.

        :return: an int, representing the number of constraints acting on a Square
        """
        count = sum(1 for constraint in self.constraints if constraint.value == 0)
        return count


class Board:

    def __init__(self, sudoku_grid: list):
        """
        Creates a board of Squares, all in the locations they exist in the sudoku_grid.
        """
        self._grid = sudoku_grid
        self._subgrid_count, self._rows_in_subgrid, self._cols_in_subgrid = GridHelper.initialize_grid_counts(
            self._grid)
        self._squares: list[list[Square]] = []
        self._generate_squares()
        self._populate_constraints()
        self._states = [[(Square, int)]]  # stores changes that occurred during MAC for restoration

    def _populate_constraints(self):
        """
        Generate a Square's constraints, each of which is a neighbouring Square on the board.
        """
        for rows in self._squares:
            for square in rows:
                square.add_constraint(*self.get_row_neighbours(square.row))
                square.add_constraint(*self.get_col_neighbours(square.col))
                square.add_constraint(*self.get_subgrid_neighbours(square.row,
                                                                   square.col,
                                                                   self._rows_in_subgrid,
                                                                   self._cols_in_subgrid))

    def get_row_neighbours(self, row: int):
        """
        Returns a list of Squares representing a full row of the sudoku grid.

        :param row: an int, representing the row of Squares to be returned
        :return: a list of Squares
        """
        return self._squares[row]

    def get_subgrid_neighbours(self, row: int, col: int, rows_in_subgrid: int, cols_in_subgrid: int):
        """
        Returns all Squares in a subgrid on the sudoku board.

        :param row: an int, representing the row in which the sub-grid starts on
        :param col: an int, represetning the column in which the sub-grid starts on
        :param rows_in_subgrid: an int, representing the number of rows in the sub-grid
        :param cols_in_subgrid: an int, representing the number of columns in the sub-grid
        :return: a list of Squares, representing an entire subgrid on the sudoku baord
        """
        subgrid_values = []
        o_row, o_col = GridHelper.get_subgrid_origin(row, col, rows_in_subgrid, cols_in_subgrid)
        for r in range(0, rows_in_subgrid):
            for c in range(0, cols_in_subgrid):
                if self._squares[o_row + r][o_col + c] != 0:
                    subgrid_values.append(self._squares[o_row + r][o_col + c])
        return subgrid_values

    def get_col_neighbours(self, col: int):
        """
        Returns a list of Squares representing a full column of the sudoku grid.

        :param col: an int, representing the column of Squares to be returned
        :return: a list of Squares
        """
        return [row[col] for row in self._squares]

    def _generate_squares(self):
        """
        Generates Square objects for each square on the sudoku board.
        """
        for row, rows in enumerate(self._grid):
            row_of_squares = []
            for col, value in enumerate(rows):
                new_square = Square(value, (row, col))
                if value == 0:  # if the square is zero we need to add all the potential values to the square
                    domain = [*range(1, (len(rows) + 1))]
                    for potential_value in domain:
                        new_square.add_to_domain(potential_value)
                else:
                    new_square.add_to_domain(value)  # if the square has a value then the domain is set.
                row_of_squares.append(new_square)
            self._squares.append(row_of_squares)

    @property
    def max_value(self):
        """
        Returns the maximum value permitted in the sudoku board.

        :return: an int, representing the maximum value
        """
        return self._subgrid_count

    @property
    def subgrid_count(self):
        """
        Returns the number of sub-grids on the sudoku board.

        :return: an int, representing the number of sub-grids
        """
        return self._subgrid_count

    @property
    def rows_in_subgrid(self):
        """
        Returns the number of rows in a sub-grid on the sudoku board.

        :return: an int, representing the number of rows in a sub-grid
        """
        return self._rows_in_subgrid

    @property
    def cols_in_subgrid(self):
        """
        Returns the number of columns in a sub-grid on the sudoku board.

        :return: an int, representing the number of columns in a sub-grid
        """
        return self._cols_in_subgrid

    @property
    def grid(self) -> list[list[int]]:
        """
        Returns the sudoku board as a 2D list of ints.

        :return: a 2D list of integers representing the current state of the sudoku board
        """
        return self._grid

    @property
    def squares(self) -> list:
        """
        Return a list of all Square objects.

        :return: a list, representing all Square objects that comprise the sudoku board
        """
        return self._squares

    @squares.setter
    def squares(self, value: list):
        """
        Set the Squares on the sudoku board.

        :param value: a list of Squares
        """
        self._squares = value

    @property
    def states(self) -> [('Square', int)]:
        """
        Returns the state of a square during/after the MAC process.

        :return: a list of Square,int tuples, each representing the state of a Square
        """
        return self._states

    def add_to_states(self, sq_list: [('Square', int)]):
        """
        Add the most recent state of the Square resulting from the MAC process.

        :param sq_list: a list of Square, int tuples, each representing a change to the Square's state
        """
        self._states.append(sq_list)

    def get_square(self, row: int, col: int) -> Square:
        """
        Returns a square object based on its location on the sudoku board.

        :param row: an int, representing the target Square's row
        :param col: an int, representing the target Square's column
        :return: a Square located at the (col, row) coordinate provided
        """
        return self.squares[row][col]

    def update_value(self, square: 'Square', value: int):
        """
        Update a Square's value on the 2D list version of the sudoku board.

        :param square: a Square object, representing the square to be updated
        :param value: an int, representing the Square's new value
        """
        self.grid[square.row][square.col] = value
        square.assign_value(value)

    def undo_value(self, square: 'Square'):
        """
        Revert a Square's value to zero on the 2D list version of the sudoku baord.

        :param square: a Square, representing the square to be reverted
        """
        self.grid[square.row][square.col] = 0
        square.unassign_value()
