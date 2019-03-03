from collections import defaultdict

def represent_sudoku(true_vars):
    s = defaultdict(lambda: defaultdict(lambda: " "))
    row = []
    for var in true_vars:
        var_int = int(var)
        row_col = var_int // 10
        row = row_col // 10
        col = row_col % 10

        value = var_int % 10
        s[row - 1][col - 1] = str(value)

    output = (("{} "*8 + "{}\n")*9).format(*[s[i][j] for i in range(9) for j in range(9)])
        
    return output