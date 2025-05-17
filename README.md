# Gem Hunter: Logic Puzzle Solver

![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-red.svg)
![PySAT](https://img.shields.io/badge/PySAT-0.1.8-purple.svg)

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Solving Algorithms](#solving-algorithms)
  - [Backtracking](#backtracking)
  - [Bruteforce](#bruteforce)
  - [PySAT](#pysat)
- [Performance Comparison](#performance-comparison)
- [License](#license)
- [Author](#author)

## Project Overview

This project was created as part of an AI course (CSC14003) in University of Science, Vietnam National University, Ho Chi Minh City (HCMUS), focusing on using Conjunctive Normal Form (CNF) and applying brute-force, backtracking algorithms, the PySAT library to find hidden gems while avoiding traps.

## Project Structure

```
Gem Hunter/
│
├── src/                         # Source code
│   ├── Algorithms/              # Solving algorithms
│   │   ├── backtracking.py      # Backtracking implementation
│   │   ├── bruteforce.py        # Bruteforce implementation
│   │   ├── generate_CNF.py      # CNF generator for SAT
│   │   └── pysat_lib.py         # PySAT interface
│   │
│   ├── Game/                    # Game logic and UI components
│   │   ├── event_management.py  # Event handling
│   │   ├── screen_management.py # Screen rendering
│   │   ├── state_management.py  # Game state tracking
│   │   └── ui_components.py     # UI elements
│   │
│   ├── Utils/                   # Utility functions
│   │   ├── algorithm_utils.py   # Algorithm helpers
│   │   └── file_utils.py        # File I/O operations
│   │
│   ├── config.py                # Configuration settings
│   └── runner.py                # Main game runner
│
├── Input/                       # Input puzzle files
│   ├── input_1.txt              # 5×5 puzzle
│   ├── input_2.txt              # 11×11 puzzle
│   └── input_3.txt              # 20×20 puzzle
│
├── Output/                      # Solution output files
│   ├── 5x5/                     # 5×5 solutions
│   ├── 11x11/                   # 11×11 solutions
│   └── 20x20/                   # 20×20 solutions
│
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

## Features

- **Interactive GUI**: Built with Pygame featuring animations and visual feedback
- **Multiple Solving Algorithms**:
  - **Backtracking**: Recursive approach with constraint propagation
  - **Bruteforce**: Systematic trial of all possible combinations
  - **PySAT**: Conversion to SAT problem and solving with a SAT solver
- **Multiple Puzzle Sizes**: Support for 5×5, 11×11, and 20×20 grids
- **Real-time Solving Visualization**:
  - Loading animation during solving
  - Timeout warnings and cancellation options
  - Execution time tracking
- **Result Storage**: Automatic saving of solutions to output files

## Installation

### 1. Clone or download the repository

Download and extract the project files to your local machine.

### 2. Install dependencies

Open a terminal/command prompt and navigate to the project directory:

- `cd path/to/project`
- `pip install -r requirements.txt`

## Usage

1. Run the main application:

   `python main.py`

2. Navigate through the game interface:

   - Start from the main menu
   - Select grid size (5×5, 11×11, or 20×20)
   - Choose a solving algorithm (Backtracking, Bruteforce, or PySAT)
   - Press "Solve" to start the solving process
   - View results when the puzzle is solved

3. Understand the solving process:
   - Green: Represents gems (G)
   - Red: Represents traps (T)
   - Blue: Represents numerical constraints
   - Cells with numbers indicate how many traps must be adjacent

## Solving Algorithms

### Backtracking

An efficient recursive approach that assigns values one cell at a time, backtracking when constraints are violated. Performs well with constraint propagation, making it suitable for most puzzle sizes.

### Bruteforce

A systematic approach that tries all possible combinations. Simple but computationally expensive for larger puzzles, often hitting timeout limits for grids larger than 5×5.

### PySAT

Converts the puzzle into a SAT (Boolean Satisfiability) problem in Conjunctive Normal Form (CNF) and uses the Glucose SAT solver to find a solution. Highly efficient for complex puzzles.

## Performance Comparison

Algorithm performance varies significantly by puzzle size:

| Algorithm    | 5×5      | 11×11    | 20×20    |
| ------------ | -------- | -------- | -------- |
| Backtracking | 0.00088s | 0.00509s | 0.07420s |
| Bruteforce   | 0.49694s | Timeout  | Timeout  |
| PySAT        | 0.00079s | 0.00051s | 0.00130s |

## License

This project is part of an academic exercise. All rights reserved.

## Author

Developed as part of the AI course in University of Science, Vietnam National University, Ho Chi Minh City (HCMUS)
