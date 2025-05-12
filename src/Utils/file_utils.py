def read_board(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            row = [cell.strip() for cell in line.strip().split(',')]
            board.append(row)
    return board

