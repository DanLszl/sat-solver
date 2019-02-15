from collections import defaultdict
from read_puzzle import parse_dimacs, read_dimacs, rules_file
from copy import deepcopy


def get_variables_from_rules(rules):
    variables = defaultdict(bool)
    for clause in rules:
        for variable in clause:
            variables[variable.name] = None

    return variables


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
    new_problem = []
    literals = defaultdict(lambda: {True: 0, False: 0})
    for clause in problem:
        for variable in clause:
            literals[variable.name][variable.ispositive] += 1

        if istautology(clause):
            pass
        elif isunitclause(clause):
            variable = clause[0]
            # TODO what if this was already set? Can that happen
            assignments[variable.name] = variable.ispositive

    pos_pure_literals = [l for l, count in literals.items() if count[False] == 0]
    neg_pure_literals = [l for l, count in literals.items() if count[True] == 0]





    return problem

    return problem


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
        else:
            return False

rules = parse_dimacs(read_dimacs(rules_file))
# print(rules[:100])
variables = get_variables_from_rules(rules)
print(variables)
print(len(variables))
