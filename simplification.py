from read_puzzle import Variable
from collections import defaultdict

from variable import Assignments

from problem import Problem





def isunitclause(clause, assignments):
    count = 0
    last_variable = None
    for variable in clause:
        if assignments[variable.name] is None:
            count += 1
            last_variable = variable

    if count == 1:
        assignments[last_variable.name] = last_variable.ispositive
        print(clause)
        print(last_variable)
        print()
        return True

    else:
        return False


def trueclause(clause, assignments):
    for variable in clause:
        if assignments[variable.name] == variable.ispositive:
            return True
    return False


# Unused functions


def simplify(problem, assignments, metrics, depth=0, verbose=False):
    """
    Modifies the problem and the assignments by
    1. Removing all tautologies
    2. Assigning all pure literals
    3. Assigning unit clauses
    """
    # print("depth:", depth)

    with assignments.printing(verbose):
        # pass

        # if verbose > 0:
        #     print_sudoku(assignments.get_true_vars())

        modifications = 0
        modifications += problem.remove_tautologies()

        modifications += problem.assign_pure_literals(assignments)

        # if verbose > 1:
        #     print_sudoku(assignments.get_true_vars())

        modifications += problem.assign_unit_clauses(assignments)

        # if verbose > 2:
        #     print_sudoku(assignments.get_true_vars())

        if modifications == 0:
            return problem, assignments
        else:
            metrics.simplify(modifications)
            return simplify(problem, assignments, metrics, depth + 1, verbose)


if __name__ == "__main__":

    assignments = Assignments(**{"P": False, "Q": None, "R": None})
    # Solution: P: True, Q: Q: True, R: False
    problem = [
        [Variable("P"), Variable("-Q")],
        [Variable("Q"), Variable("R")],
        [Variable("-R"), Variable("-P")],
    ]
    print(simplify(problem, assignments))
