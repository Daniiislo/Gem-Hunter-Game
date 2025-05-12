from pysat.solvers import Glucose3
from pysat.formula import CNF
import time

from generate_cnf import generate_cnf, read_board

def solve_by_pysat(input_file):
    board = read_board(input_file)
    clauses, num_vars = generate_cnf(board)
    
    solver = Glucose3()

    # Create a CNF formula
    cnf = CNF()
    cnf.extend(clauses)

    # Add the clauses to the solver
    solver.append_formula(cnf)

    # Start the timer
    start_time = time.time()

    # Solve the SAT problem
    if solver.solve():
        assignment = solver.get_model()
        pysat_time = time.time() - start_time

        board_result = [['_' for _ in range(len(board[0]))] for _ in range(len(board))]
        for i in range(len(board[0])):
            for j in range(len(board)):
                if board[i][j] != '_':
                    board_result[i][j] = board[i][j]
                    continue
                var = (i * len(board[0])) + j + 1
                if var in assignment:
                    board_result[i][j] = 'T'
                elif -var in assignment:
                    board_result[i][j] = 'G'

        return board_result, pysat_time
    else:
        return None
