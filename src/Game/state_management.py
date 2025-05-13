from src.config import *
import threading

class GameState:
    MAIN_MENU = "main_menu"
    LEVEL_SELECT = "level_select"
    ALGORITHM_SELECT = "algorithm_select"
    PUZZLE_SCREEN = "puzzle_screen"
    RESULT_SCREEN = "result_screen"
    
    def __init__(self):
        self.__running = True
        self.__fps = FPS
        self.__current_time = 0
        
        self.__current_screen = self.MAIN_MENU  
        self.__selected_size = None  # "5x5", "11x11" or "20x20"
        self.__selected_algorithm = None  # "Backtracking", "Bruteforce" or "PySAT"
        
        self.__solution = None
        self.__solution_time = None
        
        self.__current_board = None
    
        self.__is_solving = False
        self.__solver_thread = None
        self.__solution_start_time = 0
        self.__elapsed_time = 0
        self.__timeout_reached = False
        self.__cancel_solving = False
        
    # getter/setter
    @property
    def is_solving(self):
        return self.__is_solving
    @is_solving.setter
    def is_solving(self, value):
        self.__is_solving = value
        
    @property
    def solver_thread(self):
        return self.__solver_thread
    @solver_thread.setter
    def solver_thread(self, value):
        self.__solver_thread = value
        
    @property
    def solution_start_time(self):
        return self.__solution_start_time
    @solution_start_time.setter
    def solution_start_time(self, value):
        self.__solution_start_time = value
        
    @property
    def elapsed_time(self):
        return self.__elapsed_time
    @elapsed_time.setter
    def elapsed_time(self, value):
        self.__elapsed_time = value
        
    @property
    def timeout_reached(self):
        return self.__timeout_reached
    @timeout_reached.setter
    def timeout_reached(self, value):
        self.__timeout_reached = value
        
    @property
    def cancel_solving(self):
        return self.__cancel_solving
    @cancel_solving.setter
    def cancel_solving(self, value):
        self.__cancel_solving = value
        
    @property
    def running(self):
        return self.__running
    @running.setter
    def running(self, value):
        self.__running = value

    @property
    def fps(self):
        return self.__fps
    @fps.setter
    def fps(self, value):
        self.__fps = value
        
    @property
    def current_time(self):
        return self.__current_time
    @current_time.setter
    def current_time(self, value):
        self.__current_time = value
        
    @property
    def current_screen(self):
        return self.__current_screen
    @current_screen.setter
    def current_screen(self, value):
        self.__current_screen = value
        
    @property
    def selected_size(self):
        return self.__selected_size
    @selected_size.setter
    def selected_size(self, value):
        self.__selected_size = value
        
    @property
    def selected_algorithm(self):
        return self.__selected_algorithm
    @selected_algorithm.setter
    def selected_algorithm(self, value):
        self.__selected_algorithm = value
        
    @property
    def solution(self):
        return self.__solution
    @solution.setter
    def solution(self, value):
        self.__solution = value
        
    @property
    def solution_time(self):
        return self.__solution_time
    @solution_time.setter
    def solution_time(self, value):
        self.__solution_time = value
        
    @property
    def current_board(self):
        return self.__current_board
    @current_board.setter
    def current_board(self, value):
        self.__current_board = value
