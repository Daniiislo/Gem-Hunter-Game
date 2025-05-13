import pygame
import time
import threading

from src.Utils.file_utils import read_board, write_result
from src.Algorithms.backtracking import backtracking_solver
from src.Algorithms.bruteforce import bruteforce_solver
from src.Algorithms.pysat_lib import solve_by_pysat
from src.config import INPUT_FILE, ALGORITHMS, OUTPUT_FILE, TIMEOUT_SECONDS

class EventHandler:
    def __init__(self, game_state, screen_manager):
        self.game_state = game_state
        self.screen_manager = screen_manager
        self.original_cursor = pygame.mouse.get_cursor()

    def handle_all_events(self, events):
        # Update elapsed time if solving
        if self.game_state.is_solving:
            current_time = time.time()
            self.game_state.elapsed_time = current_time - self.game_state.solution_start_time
            
            # Check for timeout
            if self.game_state.elapsed_time > TIMEOUT_SECONDS and not self.game_state.timeout_reached:
                self.game_state.timeout_reached = True
                self.game_state.cancel_solving = True
                
        mouse_pos = pygame.mouse.get_pos()
        self.screen_manager.update(mouse_pos, 1/60)  # Pass dt for animations
        
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state.running = False
                # Make sure to stop any running threads
                self.game_state.cancel_solving = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left mouse button clicked
                    self._handle_click(mouse_pos)
                    
    def _handle_click(self, mouse_pos):# Left click
        if self.game_state.current_screen == self.game_state.MAIN_MENU:
            # Go to level select screen
            if self.screen_manager.start_button.is_clicked(mouse_pos, True):
                self.game_state.current_screen = self.game_state.LEVEL_SELECT
                
        elif self.game_state.current_screen == self.game_state.LEVEL_SELECT:
            if self.screen_manager.back_button.is_clicked(mouse_pos, True):
                # Back to main menu
                self.game_state.current_screen = self.game_state.MAIN_MENU
            
            # Check if any grid option is clicked
            for i, grid_option in enumerate(self.screen_manager.grid_options):
                if grid_option.is_clicked(mouse_pos, True):
                    self.game_state.selected_size = grid_option.text

                    # Go to algorithm select screen
                    self.game_state.current_screen = self.game_state.ALGORITHM_SELECT
                    break
                    
        elif self.game_state.current_screen == self.game_state.ALGORITHM_SELECT:
            if self.screen_manager.back_button.is_clicked(mouse_pos, True):
                # Back to level select screen
                self.game_state.current_screen = self.game_state.LEVEL_SELECT
            
            # Check if any algorithm button is clicked
            for i, button in enumerate(self.screen_manager.algorithm_buttons):
                if button.is_clicked(mouse_pos, True):
                    self.game_state.selected_algorithm = ALGORITHMS[i]
                    self._load_puzzle()

                    # Go to puzzle screen
                    self.game_state.current_screen = self.game_state.PUZZLE_SCREEN
                    break
                    
        elif self.game_state.current_screen == self.game_state.PUZZLE_SCREEN:
            # Back to algorithm select screen
            if self.screen_manager.back_button.is_clicked(mouse_pos, True):
                self.game_state.timeout_reached = False
                self.game_state.cancel_solving = False
                self.game_state.is_solving = False
                
                self.game_state.current_screen = self.game_state.ALGORITHM_SELECT
            
            # Handle solve or cancel button clicks
            if not self.game_state.is_solving and self.screen_manager.solve_button.is_clicked(mouse_pos, True):
                # Start solving
                self._start_solving_process()
            elif self.game_state.is_solving and self.screen_manager.cancel_button.is_clicked(mouse_pos, True):
                # Cancel solving
                self._cancel_solving()
                
        elif self.game_state.current_screen == self.game_state.RESULT_SCREEN:
            # Back to puzzle screen
            if self.screen_manager.back_button.is_clicked(mouse_pos, True):
                self.game_state.current_screen = self.game_state.PUZZLE_SCREEN
    
    def _start_solving_process(self):
        # Set up solving state
        self.game_state.is_solving = True
        self.game_state.solution_start_time = time.time()
        self.game_state.elapsed_time = 0
        self.game_state.timeout_reached = False
        self.game_state.cancel_solving = False
        
        # Change cursor to waiting cursor
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        
        # Start a new thread for solving
        self.game_state.solver_thread = threading.Thread(target=self._solve_puzzle_threaded)
        self.game_state.solver_thread.daemon = True
        self.game_state.solver_thread.start()
    
    def _cancel_solving(self):
        if self.game_state.is_solving:
            # Reset cursor
            pygame.mouse.set_cursor(self.original_cursor)

            self.game_state.cancel_solving = True
            self.game_state.timeout_reached = False
            self.game_state.is_solving = False
            self.game_state.solver_thread = None
            self.game_state.elapsed_time = 0
            self.game_state.solution_start_time = 0
            
    
    def _solve_puzzle_threaded(self):
        try:
            input_file = INPUT_FILE[self.game_state.selected_size]
            
            if not input_file:
                self._finish_solving(None, 0)
                return
            
            # Define cancel check function
            def is_cancelled():
                return self.game_state.cancel_solving
            
            # Start solving based on selected algorithm
            start_time = time.time()
            result = None
            solve_time = 0
            
            output_file = OUTPUT_FILE[self.game_state.selected_size][self.game_state.selected_algorithm]
            try:
                if self.game_state.selected_algorithm == ALGORITHMS[0]:
                    result, solve_time = backtracking_solver(input_file, is_cancelled)
                elif self.game_state.selected_algorithm == ALGORITHMS[1]:
                    result, solve_time = bruteforce_solver(input_file, is_cancelled)
                elif self.game_state.selected_algorithm == ALGORITHMS[2]:
                    result, solve_time = solve_by_pysat(input_file, is_cancelled)
            except Exception as e:
                print(f"Error solving puzzle: {e}")
            
            if  self.game_state.timeout_reached:
                # Solving was cancelled
                write_result(self.game_state.selected_algorithm, self.game_state.selected_size, None, 0, output_file, True)
                self._finish_solving(None, time.time() - start_time)
                return
            if self.game_state.cancel_solving:
                self._finish_solving(None, time.time() - start_time)
                return
                
            # Write results if solution was found
            if result:
                write_result(self.game_state.selected_algorithm, self.game_state.selected_size, result, solve_time, output_file)
            
            self._finish_solving(result, solve_time)
            
        except Exception as e:
            print(f"Error in solving thread: {e}")
            self._finish_solving(None, 0)
    
    def _finish_solving(self, result, solve_time):
        if self.game_state.is_solving:
            self.game_state.is_solving = False

            # Reset cursor regardless of result
            pygame.mouse.set_cursor(self.original_cursor)
            
            if self.game_state.cancel_solving or self.game_state.timeout_reached:
                self.game_state.solution = None
                self.game_state.solution_time = 0

            else:
                # Normal completion
                self.game_state.solution = result
                self.game_state.solution_time = solve_time
                
                # Only go to result screen if solution was found
                if result is not None:
                    self.game_state.current_screen = self.game_state.RESULT_SCREEN

    def _load_puzzle(self):
        # Load puzzle based on the selected size
        input_file = INPUT_FILE[self.game_state.selected_size]
        if input_file:
            try:
                self.game_state.current_board = read_board(input_file)
            except Exception as e:
                print(f"Error loading puzzle: {e}")
                self.game_state.current_board = None

