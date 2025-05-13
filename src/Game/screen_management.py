import pygame
import math
from src.config import BACKGROUND_COLOR, CELL_COLORS, TIMEOUT_SECONDS

from src.Game.ui_components import Button, GridOption, LoadingSpinner
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.Utils.file_utils import read_board

class ScreenManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.background_color = BACKGROUND_COLOR
        
        # Font options
        self.title_font = pygame.font.SysFont('Arial', 60, bold=True)
        self.normal_font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 20)
        
        # Initialize start button
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT // 2 + 100, 
            200, 50, 
            "Start Game",
        )
        
        # Initialize grid options
        grid_size = 150
        spacing = 40
        start_x = SCREEN_WIDTH // 2 - (grid_size * 3 + spacing * 2) // 2
        
        self.grid_options = [
            GridOption(start_x, SCREEN_HEIGHT // 2 - 50, grid_size, 5, "5x5"),
            GridOption(start_x + grid_size + spacing, SCREEN_HEIGHT // 2 - 50, grid_size, 11, "11x11"),
            GridOption(start_x + (grid_size + spacing) * 2, SCREEN_HEIGHT // 2 - 50, grid_size, 20, "20x20")
        ]
        
        # Initialize algorithm buttons
        self.algorithm_buttons = [
            Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50, "Backtracking"),
            Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 50, "Bruteforce"),
            Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 90, 300, 50, "PySAT")
        ]
        
        # Initialize solve and cancel buttons
        self.solve_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Solve")
        self.cancel_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Cancel")
        
        # Initialize back button
        self.back_button = Button(10, SCREEN_HEIGHT - 50, 90, 40, "Back")
        
        # Colors for cells
        self.cell_colors = CELL_COLORS
        
        # Initialize loading spinner
        self.loading_spinner = LoadingSpinner(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        
    def draw(self, screen):
        if self.game_state.current_screen == self.game_state.MAIN_MENU:
            self._draw_main_menu(screen)
        elif self.game_state.current_screen == self.game_state.LEVEL_SELECT:
            self._draw_level_select(screen)
        elif self.game_state.current_screen == self.game_state.ALGORITHM_SELECT:
            self._draw_algorithm_select(screen)
        elif self.game_state.current_screen == self.game_state.PUZZLE_SCREEN:
            self._draw_puzzle_screen(screen)
        elif self.game_state.current_screen == self.game_state.RESULT_SCREEN:
            self._draw_result_screen(screen)
    
    def _draw_main_menu(self, screen):
        screen.fill(self.background_color)
        
        # Draw fancy title with special effects
        self._draw_fancy_title(screen, "GEM HUNTER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        
        # Draw start button
        self.start_button.draw(screen)
        
    def _draw_fancy_title(self, screen, text, x, y):
        """
        Draw a title with special effects like shadows and glowing effects
        
        Parameters:
            screen: pygame display surface
            text: text to display
            x, y: center position of the title
        """
        # Shadow effect
        shadow_offset = 4
        glow_colors = [(220, 120, 30), (240, 180, 20), (255, 215, 0)]  # Gold to orange
        
        # Pulsing effect based on time
        pulse = (math.sin(self.game_state.current_time / 500) + 1) / 2  # 0.0 to 1.0
        
        # Size pulsing effect
        base_font_size = 64
        pulse_font_size = base_font_size + int(10 * pulse)  # Font size varies between 64-74
        pulsing_font = pygame.font.SysFont('Arial', pulse_font_size)
        
        # Sparkling gem positions around the title
        gem_positions = [
            (x - 220, y - 30),
            (x + 220, y - 30),
            (x - 180, y + 40),
            (x + 180, y + 40)
        ]
        
        # Draw diamond lights
        for pos in gem_positions:
            size = 15 + int(5 * pulse)
            color_intensity = 150 + int(105 * pulse)
            pygame.draw.polygon(screen, (color_intensity, color_intensity, 255), [
                (pos[0], pos[1] - size),
                (pos[0] + size, pos[1]),
                (pos[0], pos[1] + size),
                (pos[0] - size, pos[1])
            ])
        
        # Draw shadow layers
        for i in range(3):
            offset = shadow_offset * (i + 1)
            shadow = pulsing_font.render(text, True, (30, 30, 40))
            shadow_rect = shadow.get_rect(center=(x + offset, y + offset))
            screen.blit(shadow, shadow_rect)
            
        # Draw glow layers
        for i, color in enumerate(glow_colors):
            glow = pulsing_font.render(text, True, color)
            glow_rect = glow.get_rect(center=(x - i, y - i))
            screen.blit(glow, glow_rect)
            
        # Draw main title
        title_color = (255, 255, 255)
        title = pulsing_font.render(text, True, title_color)
        title_rect = title.get_rect(center=(x, y))
        screen.blit(title, title_rect)
        
    def _draw_level_select(self, screen):
        screen.fill(self.background_color)
        
        # Header
        title = self.title_font.render("Choose Grid Size", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
        screen.blit(title, title_rect)
        
        # Draw grid options
        for grid_option in self.grid_options:
            grid_option.draw(screen)
            
        # Draw back button
        self.back_button.draw(screen)
        
    def _draw_algorithm_select(self, screen):
        screen.fill(self.background_color)
        
        # Header
        title = self.title_font.render("Choose Algorithm", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))
        screen.blit(title, title_rect)
        
        # Show selected size
        size_text = self.normal_font.render(f"Size: {self.game_state.selected_size}", True, (255, 255, 255))
        size_rect = size_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(size_text, size_rect)
        
        # Draw algorithm buttons
        for button in self.algorithm_buttons:
            button.draw(screen)
            
        # Draw back button
        self.back_button.draw(screen)
        
    def _draw_puzzle_screen(self, screen):
        screen.fill(self.background_color)
        
        # Header
        title = self.title_font.render("Puzzle", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title, title_rect)
        
        # Display selected size and algorithm
        size_text = self.small_font.render(f"Grid size: {self.game_state.selected_size}", True, (255, 255, 255))
        screen.blit(size_text, (5, 20))
        
        algo_text = self.small_font.render(f"Algorithm: {self.game_state.selected_algorithm}", True, (255, 255, 255))
        screen.blit(algo_text, (5, 50))
        
        # Special case for timeout
        if self.game_state.timeout_reached:
            # Display TIMEOUT message in center of screen
            timeout_font = pygame.font.SysFont('Arial', 72, bold=True)
            timeout_text = timeout_font.render("TIMEOUT", True, (255, 0, 0))
            timeout_rect = timeout_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(timeout_text, timeout_rect)
            
            # Display additional message
            message_text = self.normal_font.render("Algorithm took too long to solve", True, (255, 150, 150))
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(message_text, message_rect)
            
            self.back_button.draw(screen)
            return  # Exit early to avoid drawing the rest
            
        # Regular case - display board if available and not solving
        if self.game_state.current_board and not self.game_state.is_solving:
            self._draw_board(screen, self.game_state.current_board, False)
        
        # Show loading spinner and elapsed time if solving
        if self.game_state.is_solving:
            # Draw loading spinner
            self.loading_spinner.draw(screen)
            
            # Draw elapsed time
            elapsed = self.game_state.elapsed_time
            time_text = self.normal_font.render(f"Time: {elapsed:.1f}s", True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 160))
            screen.blit(time_text, time_rect)
            
            # Show timeout warning if approaching timeout
            if elapsed >= TIMEOUT_SECONDS * 0.8 and not self.game_state.timeout_reached:
                warning_text = self.small_font.render(f"Approaching timeout ({TIMEOUT_SECONDS}s)...", True, (255, 255, 0))
                warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 190))
                screen.blit(warning_text, warning_rect)
            
            # Draw cancel button instead of solve button
            self.cancel_button.draw(screen)
        else:
            # Draw solve button
            self.solve_button.draw(screen)
        
        # Draw back button
        self.back_button.draw(screen)
        
    def _draw_result_screen(self, screen):
        screen.fill(self.background_color)
        
        # Header
        title = self.title_font.render("Result", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title, title_rect)
        
        # Display selected size and algorithm
        size_text = self.small_font.render(f"Grid size: {self.game_state.selected_size}", True, (255, 255, 255))
        screen.blit(size_text, (5, 20))
        
        algo_text = self.small_font.render(f"Algorithm: {self.game_state.selected_algorithm}", True, (255, 255, 255))
        screen.blit(algo_text, (5, 50)) 
        
        # Display solution time
        if self.game_state.solution_time is not None:
            time_text = self.normal_font.render(f"Solution time: {self.game_state.solution_time:.2f} seconds", True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            screen.blit(time_text, time_rect)
        
        # Display solution if available
        if self.game_state.solution:
            self._draw_board(screen, self.game_state.solution, True)
        
        # Draw back button
        self.back_button.draw(screen)
        
    def _draw_board(self, screen, board, is_solution):
        rows, cols = len(board), len(board[0])
        
        # Identify cell size
        cell_size = min(500 // max(rows, cols), 50)
        board_width = cols * cell_size
        board_height = rows * cell_size
        
        start_x = (SCREEN_WIDTH - board_width) // 2
        start_y = (SCREEN_HEIGHT - board_height) // 2
        
        # Draw the grid
        for i in range(rows):
            for j in range(cols):
                cell_value = board[i][j]
                
                # Identify color based on cell value
                if cell_value == '_':
                    color = self.cell_colors["empty"]
                elif cell_value in ['T', 'G']:
                    color = self.cell_colors["trap"] if cell_value == 'T' else self.cell_colors["gem"]
                else:
                    color = self.cell_colors["number"]
                
                cell_rect = pygame.Rect(
                    start_x + j * cell_size,
                    start_y + i * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Border
                
                # Draw the cell value
                if cell_value != '_':
                    text_color = (0, 0, 0) if is_solution else (255, 255, 255)
                    text = self.small_font.render(cell_value, True, text_color)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
    
    def update(self, mouse_pos, dt=0):
        # Update loading spinner animation
        if self.game_state.is_solving:
            self.loading_spinner.update(dt)
            
        if self.game_state.current_screen == self.game_state.MAIN_MENU:
            self.start_button.check_hover(mouse_pos)
        
        elif self.game_state.current_screen == self.game_state.LEVEL_SELECT:
            for grid_option in self.grid_options:
                grid_option.check_hover(mouse_pos)
            self.back_button.check_hover(mouse_pos)
        
        elif self.game_state.current_screen == self.game_state.ALGORITHM_SELECT:
            for button in self.algorithm_buttons:
                button.check_hover(mouse_pos)
            self.back_button.check_hover(mouse_pos)
        
        elif self.game_state.current_screen in [self.game_state.PUZZLE_SCREEN, self.game_state.RESULT_SCREEN]:
            self.back_button.check_hover(mouse_pos)
            if self.game_state.current_screen == self.game_state.PUZZLE_SCREEN:
                if self.game_state.is_solving:
                    self.cancel_button.check_hover(mouse_pos)
                else:
                    self.solve_button.check_hover(mouse_pos)

