from src.Algorithms.backtracking import backtracking_solver
from src.Utils.algorithm_utils import check_result

input_file = './Input/input_1.txt'

def main():

    board_result, backtracking_time = backtracking_solver(input_file)


if __name__ == "__main__":
    main()
