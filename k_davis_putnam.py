from collections import defaultdict
from collections import deque
from read_puzzle import *
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
	if len(clause) == 1:
		return True


def trueclause(clause, assignments):
	for variable in clause:
		if assignments[variable.name] == variable.ispositive:
			return True
	return False


def simplify(problem, assignments):
	simples_idx = []
	literals = defaultdict(lambda: {True: 0, False: 0, "literal_clauses": []})

	for clause_idx, clause in enumerate(problem):
		for variable in clause:
			literals[variable.name][variable.ispositive] += 1
			literals[variable.name]["literal_clauses"].append(clause_idx)

		if istautology(clause):
			simples_idx.append(clause_idx)

		if isunitclause(clause):
			simples_idx.append(clause_idx)
			assignments[clause[0].name] = clause[0].ispositive

		if trueclause(clause, assignments):
			simples_idx.append(clause_idx)

	for literal, count in literals.items():
		if count[False] == 0 and assignments[literal] == None:
			assignments[literal] = True
			simples_idx += count["literal_clauses"]
		if count[True] == 0 and assignments[literal] == None:
			assignments[literal] = False
			simples_idx += count["literal_clauses"]

	simples_idx = list(dict.fromkeys(simples_idx)) # remove duplicates
	if len(simples_idx) > 0:
		for i in sorted(simples_idx, reverse=True): 
			del problem[i]
		return simplify(problem, assignments)
	else:
		return problem, assignments
			

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


def test_on_puzzle():
	rules = parse_dimacs(read_dimacs(rules_file))
	assignments = initialise_assignments_from_rules(rules)

	for puzzle in read_puzzles(puzzle_file):
		parsed_puzzle = parse_dimacs(encode_puzzle(puzzle))
		problem = rules + parsed_puzzle
		problem, assignments = simplify(problem, assignments)
		break

		
if __name__ == '__main__':
	assignments = {"P": None, "Q": None, "R": None}
	problem = [[Variable("P"), Variable("-Q")],
	            [Variable("Q"), Variable("R")],
	            [Variable("-R"), Variable("-P")]]

	# assignments = {"A": None, "B": None, "C": None, "E": None, "F": None, "I": True}
	# problem = [[Variable("-A"), Variable("B"), Variable("E")],
	# 			[Variable("-E"), Variable("A")],
	# 			[Variable("-E"), Variable("B")],
	# 			[Variable("-C"), Variable("F")],
	# 			[Variable("-F"), Variable("C")],
	# 			[Variable("I")]]
	# print(split(problem, assignments))
	test_on_puzzle()
	
	