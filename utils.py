# converts a list of sudoku board value into a 9 by 9 list grid
def make_2d_list(vals) -> [[]]:
    board = []
    curr_row = []
    for i, val in enumerate(vals):
        curr_row.append(val)
        if len(curr_row) == 9:
            board.append(curr_row)
            curr_row = []
    return board


# gets the col from a 2d arr
def get_col(arr, col):
    acc = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            if j == col:
                acc.append(arr[i][j])

    return acc


# counts the number of appearances of a specific value in an iterable
def count_appearances(iterable, val):
    count = 0
    for value in iterable:
        if value == val:
            count += 1
    return count


# exchanges the two numbers in a grid entirely, in place
def swap_num(board: list, num1, num2):
    for row, val in enumerate(board):
        for col, col_val in enumerate(board[row]):
            if col_val == num1:
                board[row][col] = num2
            elif col_val == num2:
                board[row][col] = num1


# returns a deep copy of the provided 2d array of integers
def copy_2d_arr(arr):
    acc = []
    curr_row = []
    for row in arr:
        for val in row:
            curr_row.append(val)
        acc.append(curr_row)
        curr_row = []
    return acc

    # converts a string into a list and returns the grid


def string_to_grid(s: str):
    s = s.strip()
    s = s.strip("[]")
    s = s.replace(",", "")
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.replace(" ", "")
    if s.isnumeric() and len(s) == 81:
        acc = []
        for digit in s:
            acc.append(int(digit))
        return make_2d_list(acc)
    else:
        return []
