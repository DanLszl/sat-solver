from copy import deepcopy

from read_puzzle import (
    read_dimacs,
    parse_dimacs,
    read_puzzles,
    encode_puzzle,
    rules_file,
    puzzle_file,
)

from variable import Assignments
from simplification import simplify

from print_sudoku import print_sudoku


def initialise_assignments_from_rules(rules):
    assignments = Assignments()
    for clause in rules:
        for variable in clause:
            assignments[variable.name] = None

    return assignments


def solve_sub_problem(problem, assignments, depth=0):
    problem = deepcopy(problem)
    assignments = deepcopy(assignments)
    problem, assignments = simplify(problem, assignments, verbose=4)

    if all_assigned(assignments):
        if satisfied(problem, assignments):
            return True, assignments
        else:
            return False, None
    if not still_satisfiable(problem, assignments):
        return False, None
    else:
        print_sudoku(assignments.get_true_vars())
        # print(depth)
        # print(assignments.get_assigned())

        variable_name = assignments.pick_variable()
        assignments[variable_name] = True

        result = solve_sub_problem(problem, assignments, depth + 1)

        if result[0]:
            return result

        assignments[variable_name] = None
        assignments[variable_name] = False
        result = solve_sub_problem(problem, assignments, depth + 1)

        if result[0]:
            return result
        else:
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


def test_on_puzzle():
    rules = parse_dimacs(read_dimacs(rules_file))
    assignments = initialise_assignments_from_rules(rules)

    for puzzle in read_puzzles(puzzle_file):

        parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))

        print("Puzzle:")
        print(parsed_puzzle)
        print_sudoku([v[0].name for v in parsed_puzzle])

        problem = rules + parsed_puzzle
        # problem, assignments = simplify(problem, assignments)
        satisfiable, solution = solve_sub_problem(problem, assignments)

        if satisfiable:
            print_sudoku(solution.get_true_vars())
        else:
            print("The problem is not satisfiable")

        break


if __name__ == "__main__":
    test_on_puzzle()

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
