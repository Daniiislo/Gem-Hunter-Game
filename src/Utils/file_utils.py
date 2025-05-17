def read_board(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            row = [cell.strip() for cell in line.strip().split(',')]
            board.append(row)
    return board

def write_result(algorithm, grid_size, board, solving_time, filename, timeout=False):
    with open (filename, 'w') as f:
        f.write(f"Algorithm: {algorithm}\n")
        f.write(f"Grid Size: {grid_size}\n")
        f.write(f"Solving Time: {solving_time:.5f} seconds\n")
        f.write("Result Board:\n")
        if not timeout:
            for row in board:
                f.write(','.join(row) + '\n')
        else:
            f.write("Timeout reached, no solution found.\n")