from davis_putnam import solve_sub_problem, initialise_assignments_from_rules
from read_puzzle import (
    read_dimacs,
    parse_dimacs,
    read_puzzles,
    encode_puzzle
)

from copy import deepcopy

from metrics import Metrics
from print_sudoku import print_sudoku
from time import time
import random

from problem import Problem


# puzzle_file = "1000 sudokus"
puzzle_file = "damnhard.sdk"
# puzzle_file = "hard_with_25"
rules_file = "sudoku-rules"


def test_on_puzzle():
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = initialise_assignments_from_rules(rules)

    for puzzle in read_puzzles(puzzle_file):

        parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))

        print("Puzzle:")
        print(parsed_puzzle)
        print_sudoku([v[0].name for v in parsed_puzzle])

        problem = Problem(rules + parsed_puzzle)

        heuristics = [None, "MOM", "literalcount", "Jeroslow"]
        biased = [True, False]
        # heuristics = ["Jeroslow"]
        # biased = [True]
        
        # heuristics = ["MOM"]
        # biased = [True]
        random.seed(285834)
        for h in heuristics:
            for b in biased:
                start_time = time()
                print(h, b)
                verbose = False
                metrics = Metrics(verbose=not verbose)
                assignments_to_modify = deepcopy(assignments) 
                satisfiable, solution = solve_sub_problem(problem, assignments_to_modify, metrics, heuristic=h, biased_coin=b, verbose=verbose)
                print(metrics)
                print("Time:", time() - start_time)
                print()

                if satisfiable:
                    print_sudoku(solution.get_true_vars())
                else:
                    print("The problem is not satisfiable")
        break


if __name__ == "__main__":
    test_on_puzzle()