from variable import Variable, Assignments


def simplify(problem, assignments, metrics, verbose=False):
    """
    Modifies the problem and the assignments by
    1. Removing all tautologies
    2. Assigning all pure literals
    3. Assigning unit clauses
    """

    with assignments.printing(verbose):
        modifications = 0
        modifications += problem.remove_tautologies()
        modifications += problem.assign_pure_literals(assignments)
        modifications += problem.assign_unit_clauses(assignments)

        if modifications == 0:
            return problem, assignments
        else:
            metrics.simplify(modifications)
            return simplify(problem, assignments, metrics, verbose)


if __name__ == "__main__":

    assignments = Assignments(**{"P": False, "Q": None, "R": None})
    # Solution: P: True, Q: Q: True, R: False
    problem = [
        [Variable("P"), Variable("-Q")],
        [Variable("Q"), Variable("R")],
        [Variable("-R"), Variable("-P")],
    ]
    print(simplify(problem, assignments))
