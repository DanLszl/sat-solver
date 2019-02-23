from davis_putnam import solve_sub_problem, initialise_assignments_from_rules
from read_puzzle import (
    read_dimacs,
    parse_dimacs,
    read_puzzles,
    encode_puzzle
)

from metrics import Metrics
from print_sudoku import print_sudoku

puzzle_file = "1000 sudokus"
rules_file = "sudoku-rules"


def test_on_puzzle():
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = initialise_assignments_from_rules(rules)

    for puzzle in read_puzzles(puzzle_file):

        parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))

        print("Puzzle:")
        print(parsed_puzzle)
        print_sudoku([v[0].name for v in parsed_puzzle])

        problem = rules + parsed_puzzle

        metrics1 = Metrics()
        satisfiable, solution = solve_sub_problem(problem, assignments, metrics1)
        
        metrics = Metrics()
        satisfiable, solution = solve_sub_problem(problem, assignments, metrics, heuristic="MOM")
        
        print(metrics1)
        print(metrics)
        
        # metrics = Metrics()        
        # satisfiable, solution = solve_sub_problem(
        #     problem, assignments, metrics, heuristic="Jeroslow"
        # )
        # print(metrics)

        if satisfiable:
            print_sudoku(solution.get_true_vars())
        else:
            print("The problem is not satisfiable")

        break

if __name__ == "__main__":
    test_on_puzzle()