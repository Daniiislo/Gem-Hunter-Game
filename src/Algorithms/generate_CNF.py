from itertools import combinations
from src.Utils.algorithm_utils import one_based_var_id, get_neighbors

def encode_exactly_k(var_ids, k):
    clauses = []

    # At least k: choose k from n - k + 1 variables
    for combo in combinations(var_ids, len(var_ids) - k + 1):
        clauses.append(list(combo))

    # At most k: choose k + 1 from n variables
    for combo in combinations(var_ids, k + 1):
        clauses.append([-v for v in combo])

    return clauses

def generate_cnf(board):
    rows, cols = len(board), len(board[0])
    clauses = []

    for r in range(rows):
        for c in range(cols):
            if board[r][c].isdigit():
                k = int(board[r][c])

                neighbors = get_neighbors(r, c, rows, cols)

                var_ids = [
                    one_based_var_id(nr, nc, cols) for (nr, nc) in neighbors if board[nr][nc] == '_'
                ]

                if var_ids:
                    clauses += encode_exactly_k(var_ids, k)
    return clauses

def get_var_ids(board):
    rows, cols = len(board), len(board[0])
    var_ids = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '_':
                var_ids.append(one_based_var_id(r, c, cols))
    return var_ids

def print_cnf_readable(clauses):
    for clause in clauses:
        pretty_clause = ' ∨ '.join([
            f"¬x{abs(l)}" if l < 0 else f"x{l}"
            for l in clause
        ])
        print(f"({pretty_clause})")


