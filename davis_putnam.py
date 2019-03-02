from copy import deepcopy

from variable import Assignments
from simplification import simplify


# def initialise_assignments_from_rules(rules):
#     assignments = Assignments()
#     for clause in rules:
#         for variable in clause:
#             assignments[variable.name] = None

#     return assignments


def solve_sub_problem(problem, assignments, metrics, heuristic, biased_coin=False, verbose=False):
    with problem.checkpoint():
        with assignments.checkpoint():
            problem, assignments = simplify(problem, assignments, metrics, verbose=verbose)

            if assignments.is_all_assigned():
                if problem.satisfied(assignments):
                    assignments.set_solved()
                    return True, assignments
                else:
                    metrics.backtrack()
                    return False, None

            if not problem.still_satisfiable(assignments):
                metrics.backtrack()
                return False, None
            else:
                with assignments.printing(verbose):

                    variable_name, first_assignment = assignments.pick_variable(problem, heuristic, biased_coin=biased_coin)

                    assignments[variable_name] = first_assignment
                    metrics.pick_var()

                    result = solve_sub_problem(problem, assignments, metrics, heuristic, biased_coin, verbose=verbose)

                    if result[0]:
                        return result

                    opposite = not assignments[variable_name]
                    assignments[variable_name] = None
                    assignments[variable_name] = opposite
                    metrics.flip()

                    result = solve_sub_problem(problem, assignments, metrics, heuristic, biased_coin, verbose=verbose)

                    if result[0]:
                        return result
                    else:
                        metrics.backtrack()
                        return False, None


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
