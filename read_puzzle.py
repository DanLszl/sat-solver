from pprint import pprint

puzzle_file = "1000 sudokus"
rules_file = "sudoku-rules"


def read_puzzles(puzzle_file):
    with open("test_sudokus/" + puzzle_file + ".txt", "r") as f:
        for line in f:
            yield line.strip()


def encode_puzzle(puzzle):
    for position, character in enumerate(puzzle):
        row = position // 9 + 1
        column = position % 9 + 1
        if character != ".":
            yield str(row) + str(column) + character + " " + str(0) + "\n"


def read_dimacs(dimacs_file):
    with open(dimacs_file + ".txt", "r") as f:
        for line in f:
            if line[0] != "p" or line[0] != "c":
                yield line


def parse_dimacs(dimacs_generator):
    result = []
    for line in dimacs_generator:
        clause = line.split()[:-1]
        result.append(clause)
    return result


def solve(puzzle_file, rules_file):
    rules = parse_dimacs(read_dimacs(rules_file))
    for puzzle in read_puzzles(puzzle_file):
        parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))
        # solve_puzzle(rules + parsed_puzzle)
        break


solve(puzzle_file, rules_file)
