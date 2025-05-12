import time
from src.Algorithms.generate_CNF import generate_cnf, get_var_ids
from src.Utils.file_utils import read_board
from src.Utils.algorithm_utils import get_board_result

def is_clause_satisfied(clause, assignment):
    for literal in clause:
        abs_id = abs(literal)
        if abs_id in assignment:
            value = assignment[abs_id]
            if (literal > 0 and value) or (literal < 0 and not value):
                return True # this literal is satisfied
    return False

def is_clause_definitely_unsatisfied(clause, assignment):
    for literal in clause:
        abs_id = abs(literal)
        if abs_id not in assignment:
            return False # this literal is not assigned yet
        
        value = assignment[abs_id]
        if (literal > 0 and value) or (literal < 0 and not value):
            return False # this literal is satisfied
        
    return True # all literals are assigned and unsatisfied

def is_formula_satisfied(clauses, assignment):
    for clause in clauses:
        if not is_clause_satisfied(clause, assignment):
            return False
    return True

def get_unassigned_variable(var_ids, assignment):
    for v in var_ids:
        if v not in assignment:
            return v
    return None

def backtrack(clauses, assignment, var_ids):
    if len(assignment) == len(var_ids):
        if is_formula_satisfied(clauses, assignment):
            return assignment
        return None
    
    unasgn_var_id = get_unassigned_variable(var_ids, assignment)

    for value in [False, True]:
        assignment[unasgn_var_id] = value

        for clause in clauses:
            if is_clause_definitely_unsatisfied(clause, assignment):
                break
        else:
            result = backtrack(clauses, assignment, var_ids)
            if result:
                return result
        del assignment[unasgn_var_id]

    return None

def backtracking_solver(input_file):
    board = read_board(input_file)
    clauses = generate_cnf(board)

    var_ids = get_var_ids(board)

    #Start the timer
    start_time = time.time()

    assignment = backtrack(clauses, {}, var_ids)

    backtracking_time = time.time() - start_time

    if assignment:
        return get_board_result(board, assignment), backtracking_time
    else:
        return None
    



