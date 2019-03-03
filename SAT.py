#!/usr/bin/env python

import argparse

from davis_putnam import solve_problem
from read_puzzle import read_dimacs, parse_dimacs


def write_output(assignments, out_file):
    true_vars = assignments.get_true_vars()
    false_vars = assignments.get_false_vars()

    nbvar = len(true_vars) + len(false_vars)  # What to do with don't care variables?
    nbclauses = nbvar
    header = "p cnf {} {}\n".format(nbvar, nbclauses)

    with open(out_file, "w") as f:
        f.write(header)
        for true_var_name in true_vars:
            line = "{} 0\n".format(true_var_name)
            f.write(line)

        for false_var_name in false_vars:
            line = "-{} 0\n".format(false_var_name)
            f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-S",
        "--method",
        type=int,
        choices=list(range(8)),
        help="""Heuristic to run.
            S0: Basic Davis-Putnam algorithm
            S1: DLCS
            S2: MOM
            S3: Jeroslaw-Wang
            S4: Basic DP + biased coin flip
            S5: DLCS + biased coin flip
            S6: MOM + biased coin flip
            S7: Jeroslaw-Wang + biased coin flip
            """,
    )

    parser.add_argument(
        "input_file", type=str, help="Input file containing a SAT problem"
    )

    args = parser.parse_args()

    print(args)
    print(args.input_file)
    print(args.method)

    in_file = args.input_file
    out_file = in_file + ".out"

    heuristics = [None, "MOM", "literalcount", "Jeroslow"]
    biased = [True, False]
    chosen_heuristic = heuristics[args.method % 4]
    chosen_bias = bool(args.method // 4)

    print(chosen_heuristic)
    print(chosen_bias)

    dimacs = read_dimacs(in_file)
    parsed = parse_dimacs(dimacs)
    satisfiable, assignments = solve_problem(
        parsed, chosen_heuristic, chosen_bias, verbose=True
    )

    if satisfiable:
        print("The problem is satisfiable")
        write_output(assignments, out_file)
    else:
        print("The problem is not satisfiable")
        # Writing empty file
        with open(out_file, "w"):
            pass
