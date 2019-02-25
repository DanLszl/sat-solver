from collections import defaultdict
from contextlib import contextmanager

from variable import Variable


def evaluable(clause, assignment):
    for variable in clause:
        if assignment[variable.name] is None:
            return False
    return True


def istautology(clause):
    variables = {}
    for variable in clause:
        if variable.name in variables:
            if variable.ispositive != variables[variable.name]:
                return True
        else:
            variables[variable.name] = variable.ispositive
    return False


class Problem:
    def __init__(self, problem):
        self.problem = problem

    def satisfied(self, assignments):
        problem = self.problem
        for clause in problem:
            flag = False
            for variable in clause:
                assignment = assignments[variable.name]
                if variable.evaluate(assignment) is True:
                    flag = True
                    break
            if not flag:
                return False
        return True

    def still_satisfiable(self, assignment):
        problem = self.problem
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

    def remove_tautologies(self):
        problem = self.problem
        new_problem = [clause for clause in problem if not istautology(clause)]
        diff = len(problem) - len(new_problem)
        problem[:] = new_problem
        return diff

    def variables(self):
        problem = self.problem
        for clause in problem:
            for variable in clause:
                yield variable

    def get_pure_literals(self, assignments):
        variables = defaultdict(set)

        for variable in self.variables():
            if variable.name not in assignments:
                variables[variable.name].add(variable.ispositive)

        return [
            Variable(name, ispositive.pop())
            for name, ispositive in variables.items()
            if len(ispositive) == 1
        ]

    def assign_pure_literals(self, assignments):
        pure_literals = self.get_pure_literals(assignments)

        modifications = len(pure_literals)
        for variable in pure_literals:
            assignments[variable.name] = variable.ispositive
        return modifications

    def assign_unit_clauses(self, assignments):
        problem = self.problem
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

    def variables_with_clause_length(self):
        problem = self.problem
        for clause in problem:
            for variable in clause:
                yield variable, len(clause)



