from src.Algorithms.bt import solve_by_backtracking
from bruteforce import solve_by_bruteforce
from pysat_lib import solve_by_pysat

def read_board(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            row = [cell.strip() for cell in line.strip().split(',')]
            board.append(row)
    return board

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

def print_result(board_result, backtracking_time):
    if not board_result:
        print("No solution found.")
        return
    
    for row in board_result:
        print(', '.join(row))
    print(f"Time: {backtracking_time:.6f} seconds")

input_file = './testcases/input_1.txt'

board_result, backtracking_time = solve_by_backtracking(input_file)

print("Check result returned by Backtracking:")
check_result(board_result)
print_result(board_result, backtracking_time)

print()
board_result, backtracking_time = solve_by_bruteforce(input_file)

print("Check result returned by Brute-force:")
check_result(board_result)
print_result(board_result, backtracking_time)

print()
board_result, backtracking_time = solve_by_pysat(input_file)

print("Check result returned by Pysat library:")
check_result(board_result)
print_result(board_result, backtracking_time)