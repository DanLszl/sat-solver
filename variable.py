from collections import defaultdict, Counter
import numbers
import random

from contextlib import contextmanager
from print_sudoku import print_sudoku


class Variable:
    def __init__(self, variable, ispositive=None):
        if ispositive is not None:
            self.name = variable
            self.ispositive = ispositive
        else:
            if variable[0] == "-":
                self.ispositive = False
                self.name = variable[1:]
            else:
                self.ispositive = True
                self.name = variable

    def evaluate(self, assignment):
        return not assignment ^ self.ispositive

    def __repr__(self):
        return "-" + self.name if not self.ispositive else self.name


class MOMCounter(Counter):
    def __add__(self, other):
        return MOMCounter({k: self[k] + other[k] for k in self.keys() | other.keys()})

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return MOMCounter({k: count * other for k, count in self.items()})
        else:
            return MOMCounter(
                {k: self[k] * other[k] for k in self.keys() | other.keys()}
            )
    
    def get_most_common(self):
        most_common = super().most_common()
        for idx, ((i_name, i_value), (j_name, j_value)) in enumerate(zip(most_common[:-1], most_common[1:])):
            if i_value != j_value:
                return random.choice(most_common[:idx+1])[0]
        return random.choice(most_common)


class Assignments:
    def __init__(self, **kwargs):
        self.assignments = defaultdict(lambda: None)
        self.modification_stack = [[]]
        self.verbose = False
        self.solved = False
        for k, v in kwargs.items():
            self.assignments[k] = v

    def create_checkpoint(self):
        self.modification_stack.append([])

    def restore_checkpoint(self):
        for modification in self.modification_stack[-1]:
            self.assignments[modification] = None
        del self.modification_stack[-1]

    @contextmanager
    def printing(self, verbose):
        old_verbose = self.verbose
        self.verbose = verbose
        try:
            yield
        finally:
            self.verbose = old_verbose

    @contextmanager
    def checkpoint(self):
        try:
            self.create_checkpoint()
            yield
        finally:
            if not self.solved:
                self.restore_checkpoint()

    def set_solved(self):
        self.solved = True

    def is_solved(self):
        return self.solved

    def __contains__(self, key):
        return key in self.assignments

    def __getitem__(self, key):
        return self.assignments[key]

    def __setitem__(self, key, value):
        if self.solved:
            raise ValueError("The current assignment appeared to be a solution, so cannot be modified")
        
        if self.assignments[key] is None:
            self.assignments[key] = value
            self.modification_stack[-1].append(key)
            if self.verbose and value is True:
                print_sudoku(self.get_true_vars())
        elif value is None:
            self.assignments[key] = value
            # if self.verbose:
            #     print_sudoku(self.get_true_vars())
        else:
            raise ValueError("Variable {} already assigned".format(key))

    def items(self):
        return self.assignments.items()

    def __repr__(self):
        return repr(self.assignments)

    def get_true_vars(self):
        true_vars = []
        for variable, assignment in self.assignments.items():
            if assignment:
                true_vars.append(variable)
        return true_vars

    def get_false_vars(self):
        true_vars = []
        for variable, assignment in self.assignments.items():
            if assignment is False:
                true_vars.append(variable)
        return true_vars

    def get_assigned(self):
        return self.get_true_vars() + self.get_false_vars()

    def get_solution(self):
        true_vars = [Variable(var_name, True) for var_name in self.get_true_vars()]
        false_vars = [Variable(var_name, False) for var_name in self.get_false_vars()]
        return true_vars + false_vars

    def get_unassigned(self):
        unassigned = []
        for k, v in self.assignments.items():
            if v is None:
                unassigned.append(k)
        return unassigned

    def is_all_assigned(self):
        for k, v in self.assignments.items():
            if v is None:
                return False
        return True

    def is_assigned(self, var_name):
        return self.assignments[var_name] is not None

    def pick_deterministic(self):
        for k, v in self.assignments.items():
            if v is None:
                return k

    def pick_random(self):
        unassigned = self.get_unassigned()
        return random.choice(unassigned)

    def pick_value(self, biased_coin):
        if not biased_coin:
            weights = [0.5, 0.5]
        else:
            weights = [1-81/729, 81/729]
        
        return random.choices([True, False], weights=weights, k=1)[0]

    def pick_variable(self, problem, heuristic=None, biased_coin=False):
        if heuristic is None:
            return self.pick_random(), self.pick_value(biased_coin)
        elif heuristic == "MOM":
            return self.pick_variable_MOM(problem), self.pick_value(biased_coin)
        elif heuristic == "Jeroslow":
            return self.pick_variable_Jeroslow(problem), self.pick_value(biased_coin)
        elif heuristic == "literalcount":
            pos_counter, neg_counter = self.count_pos_neg(problem)
            variable_name = self.pick_variable_literal_count(problem, pos_counter, neg_counter)
            value = self.pick_value_literalcount(self, pos_counter[variable_name], neg_counter[variable_name], biased_coin)
            return variable_name, value

    def pick_value_literalcount(self, variable_name, p_count, n_count, biased_coin):
        sum_count = p_count + n_count
        if not biased_coin:
            return p_count >= n_count
        else:
            weights = [p_count/sum_count, n_count/sum_count]
            return random.choices([True, False], weights=weights, k=1)[0]

    def pick_variable_literal_count(self, problem, pos_counter, neg_counter):
        sum_counter = pos_counter + neg_counter
        variable_name = sum_counter.get_most_common()[0]
        return variable_name

    def count_pos_neg(self, problem):
        pos_counter = MOMCounter(
            v.name
            for v in problem.variables()
            if v.ispositive and not self.is_assigned(v.name)
        )
        neg_counter = MOMCounter(
            v.name
            for v in problem.variables()
            if not v.ispositive and not self.is_assigned(v.name)
        )
        return pos_counter, neg_counter

    def pick_variable_MOM(self, problem, k=2):
        pos_counter, neg_counter = self.count_pos_neg(problem)

        S = (pos_counter + neg_counter) * 2 ** k + pos_counter * neg_counter

        return S.get_most_common()[0]

    def pick_variable_Jeroslow(self, problem):
        jeroslow_values = defaultdict(float)

        for var, clause_len in problem.variables_with_clause_length():
            if not self.is_assigned(var.name):
                jeroslow_values[var.name] += 2 ** (-clause_len)

        maxes = all_max(jeroslow_values, key=jeroslow_values.get)
        return random.choice(maxes)


def all_max(iterable, key=lambda x: x):
    max_value = float('-inf')
    maxes = []
    for i in iterable:
        if key(i) > max_value:
            max_value = key(i)
            maxes = [i]
        elif key(i) == max_value:
            maxes.append(i)
    return maxes


if __name__ == "__main__":
    a = [1, 2, 3, 3]
    d = [2, 3, 3, 4]
    a_c = MOMCounter(a)
    d_c = MOMCounter(d)
    print(a_c * 2)
    print(a_c * d_c)
