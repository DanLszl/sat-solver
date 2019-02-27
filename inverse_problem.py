from simplification import simplify
from problem import Problem
from variable import Variable
from variable import Assignments
from metrics import Metrics
# from run_experiments import run_experiment
from print_sudoku import print_sudoku
import random
from davis_putnam import solve_sub_problem


def pick_randomly_until_solvable(rules, true_variables, assignments, picked_variables, metrics):
    picked_idx = random.randrange(0, len(true_variables))
    picked_name = true_variables[picked_idx]
    del true_variables[picked_idx]

    # print(picked_name)
    new_clause = [Variable(picked_name, True)]
    
    picked_variables.append(new_clause)
    problem = Problem(rules + picked_variables)

    simplify(problem, assignments, metrics, verbose=False)

    if assignments.is_all_assigned() and problem.satisfied(assignments):
        return
    else:
        return pick_randomly_until_solvable(rules, true_variables, assignments, picked_variables, metrics)


def find_min_compression(rules, true_var_names):
    metrics = Metrics()
    # print_sudoku(true_var_names)
    # assignments = Assignments(**{var_name: None for var_name in true_var_names})   # No assignments in the beginning
    assignments = Assignments()
    picked_variables = []
    pick_randomly_until_solvable(rules, true_var_names, assignments, picked_variables, metrics)
    compressed_length = len(picked_variables)
    
    return compressed_length, picked_variables


    

if __name__ == "__main__":
    import time
    random.seed(time.time())
    rules, true_var_names = run_experiment()

    compressed_length, picked_variables = find_min_compression(rules, true_var_names)

    compressed = [[556], [532], [981], [416], [972], [927], [451], [226], [171], [642], [959], [392], [447], [824], [145], [494], [158], [379], [295], [793], [868], [284], [686], [473], [718], [129], [253], [625], [774], [482], [678], [943], [261], [313]]
    new_problem = Problem(rules + [[Variable(str(i), True)] for j in compressed for i in j])
    ass = Assignments()
    metrics = Metrics()
    solve_sub_problem(new_problem, ass, metrics, heuristic=None, biased_coin=False, verbose=True)
    
    print(metrics)
    print_sudoku(true_var_names)
    print(true_var_names)


    print('compressed_length:', compressed_length)
    print('picked_variables:', picked_variables)
    print('new problem')
    print_sudoku([k.name for i in picked_variables for k in i])