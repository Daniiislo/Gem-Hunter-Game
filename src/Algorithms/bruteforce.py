import time
from generate_cnf import generate_cnf, read_board, get_vars, var_id
from itertools import product

def is_clause_satisfied(clause, assignment):
    for literal in clause:
        var = abs(literal)
        if var in assignment:
            val = assignment[var]
            if (literal > 0 and val) or (literal < 0 and not val):
                return True
    return False

def is_clause_definitely_unsatisfied(clause, assignment):
    for literal in clause:
        var = abs(literal)
        if var not in assignment:
            return False  # this literal is not assigned yet
        val = assignment[var]
        if (literal > 0 and val) or (literal < 0 and not val):
            return False  # this literal is satisfied
    return True  # all literals are assigned and unsatisfied

def is_formula_satisfied(clauses, assignment):
    return all(is_clause_satisfied(clause, assignment) for clause in clauses)

def get_unassigned_variable(vars, assignment):
    for v in vars:
        if v not in assignment:
            return v
    return None

def bruteforce(clauses, assignment, vars):
    for bits in product([False, True], repeat=len(vars)):
        assignment = dict(zip(vars, bits))
        if is_formula_satisfied(clauses, assignment):
            return assignment
    return None

def get_board_result(board, assignment):
    rows, cols = len(board), len(board[0])
    result = []

    for i in range(rows):
        row = []
        for j in range(cols):
            cell = board[i][j]
            if cell == '_':
                var = var_id(i, j, cols)
                row.append("T" if assignment.get(var, False) else "G")
            else:
                row.append(cell)
        result.append(row)
    
    return result

def solve_by_bruteforce(input_file):
    board = read_board(input_file)
    clauses, num_vars = generate_cnf(board)
    vars = get_vars(board)

    # Start the timer
    start_time = time.time()

    # Solve problem using brute-force
    assignment = bruteforce(clauses, {}, vars)

    bruteforce_time = time.time() - start_time
    if assignment:
        return get_board_result(board, assignment), bruteforce_time
    else:
        return None