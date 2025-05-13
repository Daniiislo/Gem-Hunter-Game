from pysat.solvers import Glucose3
from pysat.formula import CNF
import time
import threading

from src.Algorithms.generate_CNF import generate_cnf
from src.Utils.file_utils import read_board
from src.Utils.algorithm_utils import one_based_var_id, get_board_result

def solve_by_pysat(input_file, cancel_check=None):
    board = read_board(input_file)
    clauses = generate_cnf(board)
    
    solver = Glucose3()

    # Create a CNF formula
    cnf = CNF()
    cnf.extend(clauses)

    # Add the clauses to the solver
    solver.append_formula(cnf)

    # Start the timer
    start_time = time.time()
    
    # Flag to track if solving was cancelled
    cancelled = False
    
    # Solve with timeout monitoring in a separate thread if cancel_check is provided
    if cancel_check:
        # Use a thread-safe way to stop the solver
        stop_solving = threading.Event()
        
        def monitor_cancellation():
            while not stop_solving.is_set():
                if cancel_check():
                    solver.interrupt()  # Interrupt the solver
                    stop_solving.set()
                    return
                time.sleep(0.1)  # Check every 100ms
                
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_cancellation)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    # Solve the SAT problem
    try:
        if solver.solve():
            assignment = solver.get_model()
            pysat_time = time.time() - start_time
            
            if cancel_check and cancel_check():
                return None, pysat_time  # Solving was cancelled
            
            # Process and return results
            result = get_board_result(board, {abs(v): v > 0 for v in assignment})
            return result, pysat_time
        else:
            pysat_time = time.time() - start_time
            return None, pysat_time
    finally:
        # Clean up if we used the monitoring thread
        if cancel_check:
            stop_solving.set()
