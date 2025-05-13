import time
from src.Algorithms.generate_CNF import generate_cnf, get_var_ids
from src.Utils.file_utils import read_board
from src.Utils.algorithm_utils import get_board_result, is_clause_definitely_unsatisfied, is_formula_satisfied, get_unassigned_variable
from itertools import product

def bruteforce(clauses, assignment, var_ids, cancel_flag=None):
    for bits in product([False, True], repeat=len(var_ids)):
        # Check if solving has been cancelled
        if cancel_flag and cancel_flag():
            return None
            
        assignment = dict(zip(var_ids, bits))
        if is_formula_satisfied(clauses, assignment):
            return assignment
    return None

def bruteforce_solver(input_file, cancel_check=None):
    board = read_board(input_file)
    clauses = generate_cnf(board)
    var_ids = get_var_ids(board)

    # Start the timer
    start_time = time.time()

    assignment = bruteforce(clauses, {}, var_ids, cancel_check)

    bruteforce_time = time.time() - start_time

    if assignment:
        return get_board_result(board, assignment), bruteforce_time
    else:
        return None, bruteforce_time