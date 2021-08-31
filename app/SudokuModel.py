import json
import random
import numpy as np
import copy

import Seeds
from utils import swap_num, get_col, count_appearances, copy_2d_arr


# TODO fix fill method making sure you can only input valid values in range of 0 and 9

# Represents the state of a sudoku game and the operations associated with it
class SudokuModel:

    # initializes sudoku model with given matrix of integers as the board
    # throws an exception if an invalid sudoku board is given
    def __init__(self, board=None, difficulty="easy"):
        if board is None:
            self.board = self.generate_sudoku_board(difficulty)
        else:
            if self.is_valid_board(board):
                self.board = np.array(copy_2d_arr(board))
            else:
                raise TypeError("Invalid board")
        # keeping a copy of the original board for resetting purposes
        self.original = np.array(copy_2d_arr(self.board))

    # solves using backtracking
    # proceed along row filling in empty cells with first possible number according to row cols and square
    # does not mutate passed in board
    # in place solve if no board is passed in
    def solve(self, original_board=None) -> ([[]], bool):

        # inplace solution
        if original_board is None:
            self.reset()
            board = self.board
            empties = self.find_empty_coords()

        # not inplace
        else:
            board = copy_2d_arr(original_board)
            empties = self.find_empty_coords(board)

        # list of empty coords in original board in tuple form of row col pairs
        empty_index = 0
        is_back_tracking = False
        solvable = True

        while empty_index < len(empties):
            if empty_index < 0:
                solvable = False
                break
            row, col = empties[empty_index]
            next_possible = self.__pick(board, (row, col))

            if is_back_tracking:
                if next_possible != 0:
                    board[row][col] = next_possible
                    is_back_tracking = False
                    empty_index += 1
                else:
                    # clearing old attempted value while backtracking
                    board[row][col] = 0
                    empty_index -= 1
            elif next_possible == 0:
                is_back_tracking = True
                empty_index -= 1
            else:
                board[row][col] = next_possible
                empty_index += 1

        if original_board is None:
            return self.get_board(), solvable

        # returning the solution as a list of lists
        return board.toList(), solvable

    # finds the coordinates of the empty cells from the given board's sudoku board
    # returns a list of tuple pairs of row,col pairs
    def find_empty_coords(self, board=None):
        if board is None:
            board = self.original

        acc = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                coords = (row, col)
                if board[row][col] == 0:
                    acc.append(coords)
        return acc

    # picks the next possible value for a specific cell according to the cells val
    # if the value is 0 that means it starts from the beginning of the possibilities
    # if there are no more possible values function returns 0
    # loc represents a pair of row and col coordinates for the cell to be picked
    def __pick(self, board, loc: tuple) -> int:
        row = loc[0]
        col = loc[1]

        initial: int = board[row][col]
        # no more possibilities available
        if initial > 9:
            return 0

        for curr_attempt in range(initial, 10):
            if self.__is_valid_box(board, curr_attempt, loc) and \
                    self.__is_valid_row(board, curr_attempt, loc) and \
                    self.__is_valid_col(board, curr_attempt, loc):
                return curr_attempt
        return 0

    # determines whether attempt at given location results in valid box
    @staticmethod
    def __is_valid_box(board, curr_attempt, loc):
        # find which box that loc is a part of
        # determine whether curr_attempt exists in box

        # lower bounds for row and col for box indices
        box_lower_bounds = list(map(lambda x: x // 3 * 3, loc))

        for row in range(box_lower_bounds[0], box_lower_bounds[0] + 3):
            for col in range(box_lower_bounds[1], box_lower_bounds[1] + 3):
                if curr_attempt == board[row][col] and (row, col) != loc:
                    return False

        return True

    # determines whether attempt at given location results in valid row
    @staticmethod
    def __is_valid_row(board, curr_attempt, loc):
        row = board[loc[0]]
        return not (curr_attempt in row)

    # determines whether attempt at given location results in valid column
    @staticmethod
    def __is_valid_col(board, curr_attempt, loc):
        col = np.array(board)[:, loc[1]]
        return not (curr_attempt in col)

    # fills a given cell with the specified number
    # throws a type error if number isn't between 0 and 9 or tries to fill original value location
    def fill(self, x, y, num):
        if self.original[x][y] == 0 and 0 <= num <= 9:
            self.board[x][y] = num
        else:
            raise TypeError("Invalid number or location.")

    # deletes the number in the given cell
    # unless the number was given in the original board
    def delete(self, x, y):
        self.fill(x, y, 0)

    # resets this board state to the original board state
    def reset(self):
        self.board = copy_2d_arr(self.original)

    # returns a copy of the board
    def get_board(self):
        acc = []
        for row, row_val in enumerate(self.board):
            curr_row = []
            for col, col_val in enumerate(self.board[row]):
                curr_row.append(self.board[row][col])
            acc.append(curr_row)

        return acc

    # gets a particular cell val
    def get_cell(self, loc):
        return self.board[loc[0]][loc[1]]

    # returns a list of the locations of incorrect answers as tuples (row,col)
    def get_incorrect(self, board=None) -> [()]:
        if board is None:
            board = self.board

        acc = []
        for row, row_val in enumerate(board):
            for col, col_val in enumerate(board[row]):
                board_val = board[row][col]
                if board_val == 0:
                    continue
                loc = (row, col)
                valid_box = self.__is_valid_box(board, board_val, loc)
                # making sure value appears only once in row
                valid_row = count_appearances(row_val, board_val) <= 1
                valid_col = count_appearances(get_col(board, col), board_val) <= 1
                is_valid = valid_box and valid_col and valid_row
                if not is_valid:
                    acc.append(loc)

        return acc

    # determines whether board is a valid sudoku board
    def is_valid_board(self, board):
        return len(board) == 9 and len(board[0]) == 9 and len(self.get_incorrect(board)) == 0

    # generates a random solvable sudoku board with given difficulty
    @staticmethod
    def generate_sudoku_board(difficulty):
        # mapping of difficulty level and number of initial empties to start with for sudoku board
        difficulties = {"easy": 11, "medium": 25, "hard": 50}

        # making empty board
        empty_board = [[0] * 9] * 9

        # choose random base board and deep copy's it
        board = copy.deepcopy(Seeds.base_boards[random.randint(0, len(Seeds.base_boards) - 1)])
        SudokuModel.board_shuffler(board)

        possible_indices = []
        for row, row_val in enumerate(board):
            for col, col_val in enumerate(board[row]):
                possible_indices.append((row, col))

        # now need to randomly delete parts of board
        cells_to_empty = random.sample(possible_indices, difficulties[difficulty])
        for row, col in cells_to_empty:
            board[row][col] = 0

        return board

    # creates a permutation of the given board
    # side effect - mutates board
    @staticmethod
    def board_shuffler(board: [[]]):
        boxes = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        board_acc_row = []
        map(lambda box: random.shuffle(box), boxes)
        # no deep copy!
        for x, y, z in boxes:
            board_acc_row.append(board[x])
            board_acc_row.append(board[y])
            board_acc_row.append(board[z])

        # shuffling cols
        board_acc_col = []
        boxes = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        map(lambda box: random.shuffle(box), boxes)
        for x, y, z in boxes:
            board_acc_col.append(get_col(board_acc_row, x))
            board_acc_col.append(get_col(board_acc_row, y))
            board_acc_col.append(get_col(board_acc_row, z))

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numbers)

        for i in range(0, random.randint(0, 8)):
            swap_num(board_acc_col, numbers[i], numbers[i + 1])

        return board_acc_col

    # making this object json serializable
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
