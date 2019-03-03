from collections import defaultdict
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


previous = None


def print_sudoku(true_vars):
    global previous
    if previous is not None:
        color_this = set(true_vars) - set(previous)
    else:
        color_this = []
    previous = true_vars

    s = defaultdict(lambda: defaultdict(lambda: " "))
    row = []
    for var in true_vars:
        var_int = int(var)
        row_col = var_int // 10
        row = row_col // 10
        col = row_col % 10

        value = var_int % 10
        if var in color_this:
            s[row - 1][col - 1] = Fore.RED + str(value) + Style.RESET_ALL
        else:
            s[row - 1][col - 1] = str(value)
    # yapf: disable

    board = \
    (
    "╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╠───┼───┼───╬───┼───┼───╬───┼───┼───╣\n"
    "║ {} | {} | {} ║ {} | {} | {} ║ {} | {} | {} ║\n"
    "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝".format(*[s[i][j] for i in range(9) for j in range(9)])
    )
    # yapf: enable
    print(board)
