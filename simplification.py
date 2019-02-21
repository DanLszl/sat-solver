from read_puzzle import Variable
from collections import defaultdict

from variable import Assignments, variables_of_problem
from print_sudoku import print_sudoku


def istautology(clause):
    variables = {}
    for variable in clause:
        if variable.name in variables:
            if variable.ispositive != variables[variable.name]:
                return True
        else:
            variables[variable.name] = variable.ispositive
    return False


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


def remove_tautologies(problem):
    new_problem = [clause for clause in problem if not istautology(clause)]
    diff = len(problem) - len(new_problem)
    problem[:] = new_problem
    return diff


def get_pure_literals(problem, assignments):
    variables = defaultdict(set)

    for variable in variables_of_problem(problem):
        if variable.name not in assignments:
            variables[variable.name].add(variable.ispositive)

    return [
        Variable(name, ispositive.pop())
        for name, ispositive in variables.items()
        if len(ispositive) == 1
    ]


def assign_unit_clauses(problem, assignments):
    new_problem = []
    for clause in problem:
        count = 0
        for variable in clause:
            if assignments[variable.name] == variable.ispositive:
                # This clause is True
                count = 0
                break
            elif assignments[variable.name] is None:
                last_variable = variable
                count += 1

        if count == 0:
            pass
        if count == 1:
            # Unit variable, assign, and do not append
            assignments[last_variable.name] = last_variable.ispositive
        else:
            new_problem.append(clause)

    diff = len(problem) - len(new_problem)
    problem[:] = new_problem
    return diff


def simplify(problem, assignments, depth=0, verbose=0):
    """
    Modifies the problem and the assignments by
    1. Removing all tautologies
    2. Assigning all pure literals
    3. Assigning unit clauses
    """
    # print("depth:", depth)

    if verbose > 0:
        print_sudoku(assignments.get_true_vars())

    modifications = 0
    modifications += remove_tautologies(problem)

    pure_literals = get_pure_literals(problem, assignments)

    modifications += len(pure_literals)
    for variable in pure_literals:
        assignments[variable.name] = variable.ispositive

    if verbose > 1:
        print_sudoku(assignments.get_true_vars())

    modifications += assign_unit_clauses(problem, assignments)

    if verbose > 2:
        print_sudoku(assignments.get_true_vars())

    if modifications == 0:
        return problem, assignments
    else:
        return simplify(problem, assignments, depth + 1)


if __name__ == "__main__":

    assignments = Assignments(**{"P": False, "Q": None, "R": None})
    # Solution: P: True, Q: Q: True, R: False
    problem = [
        [Variable("P"), Variable("-Q")],
        [Variable("Q"), Variable("R")],
        [Variable("-R"), Variable("-P")],
    ]
    print(simplify(problem, assignments))
