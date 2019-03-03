
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
