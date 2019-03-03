import argparse
from copy import deepcopy
from time import time
import random
import pickle

from collections import defaultdict
from multiprocessing.pool import Pool
from pprint import pprint

import itertools
from os import cpu_count
import tqdm

from davis_putnam import solve_sub_problem
from read_puzzle import read_dimacs, parse_dimacs, read_puzzles, encode_puzzle
from output_sudoku import represent_sudoku

from compress import get_compression_metrics
from inverse_problem import find_min_compression
from problem import Problem

from metrics import Metrics


from print_sudoku import print_sudoku


verbose = False

rules_file = "sudoku-rules"
puzzle_files = ["100_easy_sudokus", "damnhard.sdk"]
# puzzle_files = ["2_easy_sudokus"]

heuristics = [None, "MOM", "literalcount", "Jeroslow"]
biased = [True, False]


def tree():
    return defaultdict(tree)


def solve_problem(rules_puzzle, how_many_times=3, min_compressions_attempts=10):
    rules, puzzle = rules_puzzle
    heuristics = [None, "MOM", "literalcount", "Jeroslow"]
    biased = [True, False]

    problem = Problem(puzzle+rules)

    assignments = problem.initialise_assignments_from_rules()

    results = tree()

    for h, b in itertools.product(heuristics, biased):
        for i in range(how_many_times):
            arguments = dict(
                problem=deepcopy(problem),
                assignments=deepcopy(assignments),
                metrics=Metrics(),
                heuristic=h,
                biased_coin=b,
                verbose=True,
            )
            satisfiable, solution = solve_sub_problem(**arguments)
            result = results[(h, b)] 
            if 'metrics' in result:
                result["metrics"].append(arguments["metrics"])
            else:
                result["metrics"] = [arguments["metrics"]]
            
            result["solution"] = solution.get_true_vars()

            if not satisfiable:
                print(
                    "This shouldn't happen with sudokus, the problem appears to be unsat"
                )
                break

    if satisfiable:
        print('compression')
        entropy = get_compression_metrics(
            represent_sudoku(result['solution'])
        )
        results["entropy"] = entropy
        results["min_compression"] = []

        for attempt in tqdm.tqdm(range(min_compressions_attempts)):
            compressed_length, _ = find_min_compression(
                rules, deepcopy(result['solution'])
            )
            results["min_compression"].append(
                compressed_length
            )

    return results


def run_experiments_parallel(puzzles_file, solution_tries, min_compression_attempts):
    rules = parse_dimacs(read_dimacs(rules_file))

    # puzzle_file -> puzzle_id -> (heuristics, biased_coin) -> nb_backtracks -> list
    # 4
    output = tree()

    puzzles = list(read_puzzles(puzzles_file))
    parsed_puzzles = [parse_dimacs(encode_puzzle(puzzle)) for puzzle in puzzles]
    problems = [(rules, puzzle) for puzzle in parsed_puzzles]

    cpus = cpu_count()

    with Pool(cpus) as p:
        results = {}
        for i, result in enumerate(tqdm.tqdm(p.imap(solve_problem, problems), total=len(problems))):
            results[i] = result

    print(results)

    return results


def run_experiments(heuristics, biased, min_compressions_attempts=10):
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = Problem(rules).initialise_assignments_from_rules()
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
                    satisfiable, solution = solve_sub_problem(
                        problem,
                        assignments_to_modify,
                        metrics,
                        heuristic=h,
                        biased_coin=b,
                        verbose=verbose,
                    )
                    if satisfiable:
                        output[puzzle_file][puzzle_id][(h, b)][
                            "number_of_backtracks"
                        ] = metrics.number_of_backtracks
                        output[puzzle_file][puzzle_id][(h, b)][
                            "number_of_flips"
                        ] = metrics.number_of_flips
                        output[puzzle_file][puzzle_id][(h, b)][
                            "number_of_var_picks"
                        ] = metrics.number_of_var_picks
                        output[puzzle_file][puzzle_id][(h, b)][
                            "simplifications"
                        ] = metrics.simplifications

                    else:
                        print("The problem is not satisfiable")

            if satisfiable:
                entropy = get_compression_metrics(
                    represent_sudoku(solution.get_true_vars())
                )
                output[puzzle_file][puzzle_id]["entropy"] = entropy
                output[puzzle_file][puzzle_id]["min_compression"] = []

                for attempt in range(min_compressions_attempts):
                    compressed_length, _ = find_min_compression(
                        rules, assignments_to_modify.get_true_vars()
                    )
                    output[puzzle_file][puzzle_id]["min_compression"].append(
                        compressed_length
                    )

    return output


# if __name__ == "__main__":
#     heuristics = [None, "MOM", "literalcount", "Jeroslow"]
#     biased = [True, False]
#     output = run_experiments(heuristics, biased)
#     pickle.dump(output, open("experiment_results.pickle", "wb"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        default='5_easy_sudokus',
        required=False,
        help="Input file containing sudoku puzzles",
    )

    args = parser.parse_args()
    print(args)

    input_file = args.input_file
    output_file = args.input_file + "-results.p"
    output = run_experiments_parallel(
        input_file, solution_tries=1, min_compression_attempts=10
    )

    with open(output_file, "wb") as f:
        pickle.dump(output, f)
