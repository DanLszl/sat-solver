from davis_putnam import solve_sub_problem, initialise_assignments_from_rules
from read_puzzle import (
    read_dimacs,
    parse_dimacs,
    read_puzzles,
    encode_puzzle
)
from output_sudoku import represent_sudoku
from compress import get_compression_metrics

from copy import deepcopy

from metrics import Metrics
from print_sudoku import print_sudoku
from time import time
import random

from problem import Problem

random.seed(6486)

puzzle_file = "1000 sudokus"
# puzzle_file = "damnhard.sdk"
# puzzle_file = "hardest"
rules_file = "sudoku-rules"

def write_metrics_to_file(puzzle_file, puzzle_id, metrics, solution, heuristic, biased):
    outF = open("solved_sudokus/" + str(puzzle_id) + "_" +
                puzzle_file + "_" + str(heuristic) + "_" + str(biased) + "_solved.txt", "w")
    outF.write("puzzle_id:" + str(puzzle_id) + "\n")
    outF.write("puzzle_file:" + str(puzzle_file) + "\n")
    outF.write("heuristic:" + str(heuristic) + "\n")
    outF.write("biased:" + str(biased) + "\n")
    outF.write("number_of_backtracks:" + str(metrics.number_of_backtracks) + "\n")
    outF.write("number_of_flips:" + str(metrics.number_of_flips) + "\n")
    outF.write("number_of_var_picks:" + str(metrics.number_of_var_picks) + "\n")
    outF.write("simplifications:" + str(metrics.simplifications) + "\n")
    output_sudoku = represent_sudoku(solution.get_true_vars())
    entropy = get_compression_metrics(output_sudoku)
    outF.write("entropy:"+str(entropy) + "\n")
    outF.write(output_sudoku)


def run_experiment():
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = initialise_assignments_from_rules(rules)

    for puzzle_id, puzzle in enumerate(read_puzzles(puzzle_file)):

        parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))

        print(puzzle_id)
        # print("Puzzle:")
        # print(parsed_puzzle)
        # print_sudoku([v[0].name for v in parsed_puzzle])

        problem = Problem(rules + parsed_puzzle)

        heuristics = [None, "MOM", "literalcount", "Jeroslow"]
        biased = [True, False]
        # heuristics = ["Jeroslow"]
        # biased = [True]
        
        for h in heuristics:
            for b in biased:
                start_time = time()
                # print(h, b)
                verbose = False
                metrics = Metrics(verbose = verbose)
                assignments_to_modify = deepcopy(assignments) 
                satisfiable, solution = solve_sub_problem(problem, assignments_to_modify, metrics, heuristic=h, biased_coin=b, verbose=verbose)
                # print()
                # print(metrics)
                # print("Time:", time() - start_time)
                # print()

                if satisfiable:
                    # print_sudoku(solution.get_true_vars())
                    # write_metrics_to_file(puzzle_file, puzzle_id, metrics, solution, h, b)
                    return rules, assignments_to_modify.get_true_vars()
                else:
                    print("The problem is not satisfiable")
        break
if __name__ == "__main__":
    run_experiment()
