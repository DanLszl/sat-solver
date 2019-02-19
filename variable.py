from collections import defaultdict


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

    def __repr__(self):
        return "-" + self.name if not self.ispositive else self.name


class Assignments:
    def __init__(self, **kwargs):
        self.assignments = defaultdict(bool)
        for k, v in kwargs.items():
            self.assignments[k] = v

    def __contains__(self, key):
        return key in self.assignments

    def __getitem__(self, key):
        return self.assignments[key]

    def __setitem__(self, key, value):
        if self.assignments[key] is None:
            self.assignments[key] = value
        elif value is None:
            self.assignments[key] = value
        else:
            raise ValueError(
                "Variable {} already assigned".format(self.assignments[key])
            )

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

    def get_unassigned(self):
        unassigned = []
        for k, v in self.assignments.items():
            if v is None:
                unassigned.append(k)
        return unassigned

    def pick_variable(self):
        for k, v in self.assignments.items():
            if v is None:
                return k
        # unassigned = self.get_unassigned()
        # return random.choice(unassigned)
