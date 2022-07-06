import copy
import unittest

import numpy as np

import Seeds
from SudokuModel import SudokuModel

# tests and examples for sudoku model class
from utils import make_2d_list, copy_2d_arr, string_to_grid


class TestSudokuModel(unittest.TestCase):

    def setUp(self) -> None:
        self.board1 = [[3, 9, 1, 5, 6, 2, 8, 4, 7],
                       [8, 7, 6, 9, 4, 3, 1, 2, 5],
                       [5, 4, 2, 1, 8, 7, 3, 9, 6],
                       [6, 0, 0, 2, 0, 9, 0, 7, 8],
                       [9, 0, 0, 0, 0, 4, 6, 0, 1],
                       [4, 0, 3, 7, 0, 0, 0, 0, 0],
                       [1, 3, 4, 0, 0, 0, 7, 0, 2],
                       [2, 0, 0, 0, 0, 1, 0, 6, 0],
                       [7, 6, 0, 4, 0, 0, 0, 0, 0]]

        self.board1_solved = Seeds.board1

        self.board1_backtrack1 = [[3, 0, 1, 5, 0, 2, 8, 4, 7],
                                  [8, 7, 0, 9, 4, 3, 1, 2, 5],
                                  [5, 4, 2, 1, 8, 7, 3, 9, 6],
                                  [6, 1, 5, 2, 3, 9, 4, 7, 8],
                                  [9, 2, 7, 8, 5, 4, 6, 3, 1],
                                  [4, 8, 3, 7, 1, 6, 2, 5, 9],
                                  [1, 3, 4, 6, 9, 5, 7, 8, 2],
                                  [2, 5, 8, 3, 7, 1, 9, 6, 4],
                                  [7, 0, 9, 4, 2, 8, 5, 1, 3]]

        self.board2 = [[0, 0, 4, 0, 0, 0, 0, 6, 7],
                       [3, 0, 0, 4, 7, 0, 0, 0, 5],
                       [1, 5, 0, 8, 2, 0, 0, 0, 3],
                       [0, 0, 6, 0, 0, 0, 0, 3, 1],
                       [8, 0, 2, 1, 0, 5, 6, 0, 4],
                       [4, 1, 0, 0, 0, 0, 9, 0, 0],
                       [7, 0, 0, 0, 8, 0, 0, 4, 6],
                       [6, 0, 0, 0, 1, 2, 0, 0, 0],
                       [9, 3, 0, 0, 0, 0, 7, 1, 0]]

        self.board2_solved = Seeds.board2

        self.model1 = SudokuModel(self.board1)
        self.model1_solved = SudokuModel(self.board1_solved)

        self.impossible_board = copy.deepcopy(self.board2)
        self.impossible_board[0][0] = 8

    # testing find empties method
    def test_find_empties(self):
        self.assertEqual(31, len(self.model1.find_empty_coords()))
        # checking edge cases for correct coords
        self.assertEqual((3, 1), self.model1.find_empty_coords()[0])
        self.assertEqual((8, 8), self.model1.find_empty_coords()[30])

        self.assertEqual([], self.model1_solved.find_empty_coords())

    # testing solve on solved board
    def test_solve_for_solved_board(self):
        copy = SudokuModel(np.copy(self.board1_solved))
        self.model1_solved.solve()

        # nothing should've changed
        self.assertEqual(copy.get_board(), self.model1_solved.get_board())

    # testing solve on single cell empty
    def test_solve_first_cell_empty(self):
        new_board = np.copy(self.board1_solved)
        new_board[0][0] = 0
        first_empty_model = SudokuModel(new_board)

        self.assertNotEqual(first_empty_model.get_board(), self.model1_solved.get_board(), "boards are equal")

        first_empty_model.solve()

        self.assertEqual(first_empty_model.get_board(), self.model1_solved.get_board())

    # testing solve on multiple empties but no backtracking
    def test_solve_no_backtracking(self):
        new_board = np.copy(self.board1_solved)

        # setting up for no backtracking solve
        new_board[0][2] = 0
        new_board[0][8] = 0
        new_board[5][2] = 0
        new_board[5][3] = 0

        test_model = SudokuModel(new_board)
        test_model.solve()

        self.assertEqual(test_model.get_board(), self.board1_solved)

    # testing solve for 1 backtracking step
    def test_single_backtrack(self):
        test_model = SudokuModel(self.board1_backtrack1)
        solved_board, solvable = test_model.solve()

        self.assertEqual(solved_board, self.board1_solved)

    # testing regular board solving cases
    def test_solve_normal(self):
        self.assertEqual(self.model1.solve()[0], self.board1_solved)

        test_model = SudokuModel(self.board2)
        self.assertEqual(test_model.solve()[0], self.board2_solved)

    # testing generates a random board for easy difficulty
    def test_generate_board_easy(self):
        board = self.model1.generate_sudoku_board("easy")

        self.assertEqual(len(board), 9)

    # testing that generate bord makes solvable boards
    def test_solvable_generate_board(self):
        board = SudokuModel.generate_sudoku_board("medium")
        test_model = SudokuModel(board)

        self.assertTrue(test_model.solve()[1])

    # testing string to grid method
    def test_string_to_grid(self):
        board = string_to_grid(str(self.board1))
        self.assertEqual(self.board1, board)
        # testing on 1d dimensional grid string
        self.assertEqual(make_2d_list(Seeds.board4_list), string_to_grid(str(Seeds.board4_list)))

    def test_copy(self):
        print(copy_2d_arr(Seeds.board2))
        self.assertEqual(copy_2d_arr(Seeds.board2), Seeds.board2)
