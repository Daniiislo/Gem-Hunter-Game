def get_neighbors(r, c, rows, cols):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr != 0 or dc != 0) and 0 <= r + dr < rows and 0 <= c + dc < cols:
                neighbors.append((r + dr, c + dc))
    return neighbors

def one_based_var_id(r, c, cols):
    return r * cols + c + 1 # SAT variables are 1-based

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

def check_result(board):
    rows, cols = len(board), len(board[0])

    for i in range(rows):
        row = []
        for j in range(cols):
            cell = board[i][j]
            if cell != 'T' and cell != 'G':
                num_traps = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if (dr != 0 or dc != 0) and 0 <= i + dr < rows and 0 <= j + dc < cols:
                            neighbor = board[i + dr][j + dc]
                            if neighbor == 'T':
                                num_traps += 1
                if num_traps != int(cell):
                    print(f"Error: Cell ({i}, {j}) has {num_traps} traps, expected {cell}.")
                    return False
                
    print("All cells are valid.")
    return True

def get_board_result(board, assignment):
    rows, cols = len(board), len(board[0])
    result = []

    for i in range(rows):
        row = []
        for j in range(cols):
            cell = board[i][j]
            if cell == '_':
                var = one_based_var_id(i, j, cols)
                row.append("T" if assignment.get(var, False) else "G")
            else:
                row.append(cell)
        result.append(row)
    
    return result