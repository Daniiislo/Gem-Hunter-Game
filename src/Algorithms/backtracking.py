import time
from src.Algorithms.generate_CNF import generate_cnf, get_var_ids
from src.Utils.file_utils import read_board
from src.Utils.algorithm_utils import get_board_result, is_clause_definitely_unsatisfied, is_formula_satisfied, get_unassigned_variable


def backtrack(clauses, assignment, var_ids, cancel_flag=None):
    # Check if solving has been cancelled
    if cancel_flag and cancel_flag():
        return None
        
    if len(assignment) == len(var_ids):
        if is_formula_satisfied(clauses, assignment):
            return assignment
        return None
    
    unasgn_var_id = get_unassigned_variable(var_ids, assignment)

    for value in [False, True]:
        # Check if solving has been cancelled before each iteration
        if cancel_flag and cancel_flag():
            return None
            
        assignment[unasgn_var_id] = value

        for clause in clauses:
            if is_clause_definitely_unsatisfied(clause, assignment):
                break
        else:
            result = backtrack(clauses, assignment, var_ids, cancel_flag)
            if result:
                return result
        del assignment[unasgn_var_id]

    return None

def backtracking_solver(input_file, cancel_check=None):
    board = read_board(input_file)
    clauses = generate_cnf(board)

    var_ids = get_var_ids(board)

    # Start the timer
    start_time = time.time()

    assignment = backtrack(clauses, {}, var_ids, cancel_check)

    backtracking_time = time.time() - start_time

    if assignment:
        return get_board_result(board, assignment), backtracking_time
    else:
        return None, backtracking_time




