from collections import defaultdict
from read_puzzle import parse_dimacs, read_dimacs, rules_file, Variable
from copy import deepcopy
from pprint import pprint


def initialise_assignments_from_rules(rules):
    assignments = defaultdict(bool)
    for clause in rules:
        for variable in clause:
            assignments[variable.name] = None

    return assignments


def istautology(clause):
    variables = {}
    for variable in clause:
        if variable.name in variables:
            if variable.ispositive != variables[variable.name]:
                return True
        else:
            variables[variable.name] = variable.ispositive
    return False


def isunitclause(clause):
    return len(clause) == 1


def simplify(problem, assignments):
    simplified_problem = []
    literals = defaultdict(lambda: {True: 0, False: 0})
    for clause in problem:
        for variable in clause:
            literals[variable.name][variable.ispositive] += 1

        if istautology(clause):
            # TODO: Remove entire clause
            pass
        elif isunitclause(clause):
            variable = clause[0]
            # TODO what if this was already set? Can that happen
            assignments[variable.name] = variable.ispositive

    pos_pure_literals = [l for l, count in literals.items() if count[False] == 0]
    neg_pure_literals = [l for l, count in literals.items() if count[True] == 0]

    return simplified_problem


def satisfied(problem, assignments):
    for clause in problem:
        flag = False
        for variable in clause:
            i = assignments[variable.name]
            j = variable.ispositive
            if (not (i ^ j)):
                flag = True
                break
        if not flag:
            return False
    return True


def inconsistent(problem, assignment):
    for clause in problem:
        # Check for empty clause
        if not clause:
            return True
    return False


if __name__ == '__main__':
    
    #rules = parse_dimacs(read_dimacs(rules_file))
    #variables = get_variables_from_rules(rules)

    assignments = {"P": False, "Q": False, "R": True}
    problem = [[Variable("P"), Variable("-Q")],
                [Variable("Q"), Variable("R")],
                [Variable("-R"), Variable("-P")]]

    print(satisfied(problem, assignments))
    




    









