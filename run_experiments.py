from davis_putnam import solve_sub_problem, initialise_assignments_from_rules
from read_puzzle import (
    read_dimacs,
    parse_dimacs,
    read_puzzles,
    encode_puzzle
)
from output_sudoku import represent_sudoku
from compress import get_compression_metrics
from inverse_problem import find_min_compression
from problem import Problem

from copy import deepcopy

from metrics import Metrics
from print_sudoku import print_sudoku
from time import time
import random
import pickle
from pprint import pprint


verbose = False

rules_file = "sudoku-rules"
puzzle_files = ["100_easy_sudokus", "damnhard.sdk"]
# puzzle_files = ["2_easy_sudokus"]

heuristics = [None, "MOM", "literalcount", "Jeroslow"]
biased = [True, False]


def run_experiments(heuristics, biased, min_compressions_attempts = 10):
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = initialise_assignments_from_rules(rules)
    output = dict()

    for puzzle_file in puzzle_files:
        output[puzzle_file] = dict()

        for puzzle_id, puzzle in enumerate(read_puzzles(puzzle_file)):
            parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))
            problem = Problem(rules + parsed_puzzle)
            output[puzzle_file][puzzle_id] = dict()
            
            for h in heuristics:
                for b in biased:
                    print(puzzle_file, puzzle_id, h, b)

                    metrics = Metrics()
                    output[puzzle_file][puzzle_id][(h, b)] = dict()

                    assignments_to_modify = deepcopy(assignments) 
                    satisfiable, solution = solve_sub_problem(problem, assignments_to_modify, metrics, heuristic=h, biased_coin=b, verbose=verbose)
                    if satisfiable:
                        output[puzzle_file][puzzle_id][(h, b)]["number_of_backtracks"] = metrics.number_of_backtracks
                        output[puzzle_file][puzzle_id][(h, b)]["number_of_flips"] = metrics.number_of_flips
                        output[puzzle_file][puzzle_id][(h, b)]["number_of_var_picks"] = metrics.number_of_var_picks
                        output[puzzle_file][puzzle_id][(h, b)]["simplifications"] = metrics.simplifications
        
                    else:
                        print("The problem is not satisfiable")

            if satisfiable:
                entropy = get_compression_metrics(represent_sudoku(solution.get_true_vars()))
                output[puzzle_file][puzzle_id]["entropy"] = entropy
                output[puzzle_file][puzzle_id]["min_compression"] = []

                for attempt in range(min_compressions_attempts):
                    compressed_length, _ = find_min_compression(rules, assignments_to_modify.get_true_vars())
                    output[puzzle_file][puzzle_id]["min_compression"].append(compressed_length)
                    
    return output
            
        
if __name__ == "__main__":
    heuristics = [None, "MOM", "literalcount", "Jeroslow"]
    biased = [True, False]
    output = run_experiments(heuristics, biased)
    pickle.dump(output, open("experiment_results.pickle", "wb"))

