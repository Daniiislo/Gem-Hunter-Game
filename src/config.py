SCREEN_WIDTH = 576
SCREEN_HEIGHT = 672
FPS = 60

BACKGROUND_COLOR = (0, 0, 0)

CELL_COLORS = {
            "empty": (191, 191, 191),   
            "number": (0, 153, 255),  
            "trap": (204, 0, 0),   
            "gem": (102, 255, 102)     
}

INPUT_FILE = {
            "5x5": "Testcases/input_1.txt",
            "11x11": "Testcases/input_2.txt",
            "20x20": "Testcases/input_3.txt"
}

ALGORITHMS = ["Backtracking", "Bruteforce", "PySAT"]

OUTPUT_FILE = {
            "5x5": {
                "Backtracking": "Output/5x5/output_1_backtracking.txt",
                "Bruteforce": "Output/5x5/output_1_bruteforce.txt",
                "PySAT": "Output/5x5/output_1_pysat.txt"
            },
            "11x11": {
                "Backtracking": "Output/11x11/output_2_backtracking.txt",
                "Bruteforce": "Output/11x11/output_2_bruteforce.txt",
                "PySAT": "Output/11x11/output_2_pysat.txt"
            },
            "20x20": {
                "Backtracking": "Output/20x20/output_3_backtracking.txt",
                "Bruteforce": "Output/20x20/output_3_bruteforce.txt",
                "PySAT": "Output/20x20/output_3_pysat.txt"
            }
}

# Timeout settings
TIMEOUT_SECONDS = 10  # Thời gian tối đa cho giải thuật (10 giây)