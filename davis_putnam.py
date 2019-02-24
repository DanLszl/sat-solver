from copy import deepcopy

from variable import Assignments
from simplification import simplify

from print_sudoku import print_sudoku


def initialise_assignments_from_rules(rules):
    assignments = Assignments()
    for clause in rules:
        for variable in clause:
            assignments[variable.name] = None

    return assignments


def solve_sub_problem(problem, assignments, metrics, heuristic, depth=0, biased_coin=False, verbose=0):
    problem = deepcopy(problem)
    assignments = deepcopy(assignments)
    problem, assignments = simplify(problem, assignments, metrics, verbose=verbose)

    if all_assigned(assignments):
        if satisfied(problem, assignments):
            return True, assignments
        else:
            metrics.backtrack()
            return False, None

    if not still_satisfiable(problem, assignments):
        metrics.backtrack()
        return False, None
    else:
        if verbose > 0:
            print_sudoku(assignments.get_true_vars())

        variable_name, first_assignment = assignments.pick_variable(problem, heuristic, biased_coin=biased_coin)

        assignments[variable_name] = first_assignment
        metrics.pick_var()

        result = solve_sub_problem(problem, assignments, metrics, heuristic, depth + 1, biased_coin)

        if result[0]:
            return result

        opposite = not assignments[variable_name]
        assignments[variable_name] = None
        assignments[variable_name] = opposite
        metrics.flip()

        result = solve_sub_problem(problem, assignments, metrics, heuristic, depth + 1, biased_coin)

        if result[0]:
            return result
        else:
            metrics.backtrack()
            return False, None


def all_assigned(assignments):
    for variable, value in assignments.items():
        if value is None:
            return False
    return True


def satisfied(problem, assignments):
    for clause in problem:
        flag = False
        for variable in clause:
            i = assignments[variable.name]
            j = variable.ispositive
            if not (i ^ j):
                flag = True
                break
        if not flag:
            return False
    return True


def evaluable(clause, assignment):
    for variable in clause:
        if assignment[variable.name] is None:
            return False
    return True


def still_satisfiable(problem, assignment):
    for clause in problem:
        flag = False
        if evaluable(clause, assignment):
            for variable in clause:
                if variable.ispositive == assignment[variable.name]:
                    flag = True
                    break
            if not flag:
                return False
    return True


if __name__ == "__main__":
    print("Hello")
    # assignments = {"P": None, "Q": None, "R": None}
    # problem = [[Variable("P"), Variable("-Q")],
    #             [Variable("Q"), Variable("R")],
    #             [Variable("-R"), Variable("-P")]]

    # assignments = Assignments(**{"A": None, "B": None, "C": None, "E": None, "F": None, "I": None})
    # problem = [[Variable("-A"), Variable("B"), Variable("E")],
    #           [Variable("-E"), Variable("A")],
    #           [Variable("-E"), Variable("B")],
    #           [Variable("-C"), Variable("F")],
    #           [Variable("-F"), Variable("C")],
    #           [Variable("I")]]

    # assignments = Assignments(**{"A": None, "B": None, "C": None, "E": None, "F": None, "I": None})
    # problem = [
    #             [Variable("-A"), Variable("B"), Variable("C")],
    #             [Variable('B')],
    #             [Variable('C')]
    #           ]

    # print(simplify(problem, assignments))

    # test_on_puzzle()

    # assignments = Assignments(**{"P": None, "Q": None, "R": None})
    # problem = [[Variable("P"), Variable("-Q")],
    #             [Variable("Q"), Variable("R")],
    #             [Variable("-R"), Variable("-P")]]
    # result = solve_sub_problem(problem, assignments)
    # print(result)

    # clause = [Variable("P"), Variable("-Q"), Variable("-R")]
    # assignments = Assignments(**{'P': False, 'Q': None, 'R': True})
    # print(isunitclause(clause, assignments))
    # print(assignments)
