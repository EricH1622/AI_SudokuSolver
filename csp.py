import random

from board import Board, Square
from gridhelper import GridHelper


class CSP:
    """
    This class attempts to solve a Sudoku puzzle of N-size using a Constraint Satisfaction Problem algorithm.
    """

    def __init__(self, sudoku_grid: list):
        self._board = Board(sudoku_grid)

    def neighbour_arcs_to_queue(self, queue: list, xi: 'Square', xj: 'Square'):
        """
        This helper function adds arcs to the queue for XI and excludes XJ.
        :param queue: list containing arcs
        :param xi: Square to get constraints from
        :param xj: Prev square to exclude from arcs
        """
        for constraint in xi.constraints:
            if xj != constraint and constraint not in queue:
                queue.append((constraint, xi))

    def initial_arcs_to_queue(self, square: 'Square') -> [('Square', 'Square')]:
        """
        This helper function initializes the queue with the arcs for the chosen square.
        :param square: Square to get constraints from
        :return: list containing tuple of two square pairings
        """
        return [(constraint, square) for constraint in square.constraints]

    def print_all_square_domains(self):
        """
        Helper function to print domains of all squares.
        """
        for row in self._board.squares:
            for square in row:
                print(f"{square.position} - D{square.domain}")

    def count_empty_squares(self) -> int:
        """
        Helper function to count the number of empty squares currently on the board.
        :return: Count of empty squares
        """
        count = 0
        for row in self._board.grid:
            for square in row:
                if square == 0:
                    count += 1
        return count

    def preprocess(self):
        """
        Pre-processes the new board using AC3 in an effort to reduce the search space.
        :return: False if AC3 results in an empty domain (no solution available), else True
        """
        result = self.ac3()
        if result[0]:
            for square in result[1].keys():
                if square.domain_size == 1:
                    self.board.update_value(square, square.domain[0])
            return True
        return False

    def ac3(self, queue: list = []):
        """
        Function applies Arc Consistency Algorithm #3 to the incoming queue.

        Clears the queue and updates the domains to satisfy the constraints. Maintains a dictionary
        of Square: Domain changes, so that changes can be rolled back if needed.
        If an update results in an empty domain, then no solution can be reached in this current branch.
        :param queue: list containing arcs
        :return: Tuple of result and list of domain changes. True, if no empty domains found else False.
        """
        changes = {}
        if not queue:
            for row in self.board.squares:
                for square in row:
                    queue.extend([(constraint, square) for constraint in square.constraints])
        while queue:
            xi, xj = queue.pop()
            if len(xj.domain) == 1 and self.revise(xi, xj):
                if changes.get(xi):
                    changes[xi].append(xj.value)
                else:
                    changes[xi] = [xj.value]
                if xi.domain_size == 0:
                    return False, changes
                self.neighbour_arcs_to_queue(queue, xi, xj)
        return True, changes

    def choose_unassigned_square(self) -> Square:
        """
        Wrapper function that calls on MRV and DH to select an unassigned square.
        :return: unassigned square
        """
        # Apply Minimum Remaining Value
        mrv = self.min_remaining_value()
        if len(mrv) == 1:
            return mrv[0]
        # Apply Degree Heuristics if there's a tie for square with lowest remaining value
        return self.degree_heuristics(mrv)

    def min_remaining_value(self):
        """
        Applies Minimum Remaining Value(MRV) heuristic to select an unassigned square.

        MRV ranks unassigned squares by ascending order of their domain size
        :return: list of squares
        """
        squares_list: list[Square] = []
        # Get list of all squares
        min_domain_size = self.board.max_value
        for row in self.board.squares:
            for square in row:
                if square.value == 0:
                    # Set minimum domain size if new min found
                    min_domain_size = square.domain_size if (square.domain_size < min_domain_size) else min_domain_size
                    squares_list.append(square)
        # Reduce MRV list further by only those with min domain size
        return list(filter(lambda square: square.domain_size == min_domain_size, squares_list))

    def degree_heuristics(self, mrv_result: list) -> Square:
        """
        Applies Degree Heuristics on the results of MRV for tie breaking.

        Degree Heuristics will sort the list by descending order of the number of unassigned constraints.
        If there is a tie between squares, one will be chosen at random.
        :param mrv_result: list of squares
        :return: square with the most unassigned constraints
        """
        sorted_by_constraint_count = sorted(mrv_result, key=lambda square: square.count_unassigned_constraints(),
                                            reverse=True)
        max_count = sorted_by_constraint_count[0].count_unassigned_constraints()
        return random.choice(list(
            filter(lambda square: square.count_unassigned_constraints() == max_count, sorted_by_constraint_count)))

    def order_domain_values(self, square: 'Square'):
        """
        Wrapper function for applying Least Constraining Value heuristics to order values of assignment for a square.
        :param square: Square to sort values for
        :return: list of values sorted by LRV
        """
        value_count = {value: 0 for value in square.domain}
        for constraint in square.constraints:
            for value in value_count.keys():
                if value in constraint.domain:
                    value_count[value] += 1
        lrv = sorted(value_count, key=value_count.get)
        return lrv

    def inference(self, square: 'Square' = None):
        """
        Wrapper function for calling AC3 from the backtracking function.
        :param square: square to apply AC3 on
        :return: results of AC3
        """
        if square is not None and square.domain_size == 1:
            arcs = self.initial_arcs_to_queue(square)
        return self.ac3(queue=arcs)

    def revise(self, xi: 'Square', xj: 'Square'):
        """
        Checks if domain of XI can be reduced based on XJ's domain.
        :param xi: Current square
        :param xj: Constraint square
        :return: True, if any domain changes were made, else False
        """
        revised = False
        if xj.value in xi.domain:
            xi.domain.remove(xj.value)
            revised = True
        return revised

    def restore_prev_domains(self, changes: {'Square': [int]}):
        """
        Helper function to restore domains using a dictionary that was generated during AC3.
        :param changes: dictionary of domains to restore
        """
        for square in changes.keys():
            for value in changes.get(square):
                square.add_to_domain(value)

    def backtrack(self) -> list:
        """
        Main backtracking CSP algorithm that attempts to solve a sudoku puzzle.

        Incorporates MRV and DH for choosing an unassigned square.
        Uses LRV for selecting order of domain values to try out.
        :return: Complete board if solved, else an empty list
        """
        board = self._board
        if GridHelper.is_solved(board.grid):
            return board.grid
        square = self.choose_unassigned_square()
        for value in self.order_domain_values(square):
            self.board.update_value(square, value)
            result = self.inference(square)
            if result[0]:
                solved = self.backtrack()
                if solved:
                    return solved
            self.board.undo_value(square)
            self.restore_prev_domains(result[1])
        return []

    def solve(self):
        """
        Wrapper function for calling the preprocess and backtracking algorithm.
        :return:
        """
        if not self.preprocess():
            return False
        return self.backtrack()

    @property
    def board(self):
        """
        Property getter for board
        :return: board
        """
        return self._board
