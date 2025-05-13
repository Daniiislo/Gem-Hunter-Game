import pygame
import math

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont("Arial", 32)
        
    def draw(self, screen):
        # Draw button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Button border
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click
        
class GridOption:
    def __init__(self, x, y, size, grid_size, text):
        self.rect = pygame.Rect(x, y, size, size)
        self.grid_size = grid_size  # Number of cells in the grid
        self.text = text  # "5x5", "11x11", or "20x20"
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.is_hovered = False
        self.font = pygame.font.SysFont("Arial", 24)
        
    def draw(self, screen):
        # Draw grid option
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Draw the cells in the grid (only numbers)
        cell_size = self.rect.width / self.grid_size
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_rect = pygame.Rect(
                    self.rect.x + j * cell_size,
                    self.rect.y + i * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, (200, 200, 200), cell_rect, 1)
        
        # Draw text under the grid
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class LoadingSpinner:
    def __init__(self, x, y, radius=15, width=5, color=(255, 255, 255), speed=0.15):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.color = color
        self.speed = speed
        self.angle = 0
        
    def update(self, dt):
        self.angle += self.speed * dt * 1000
        if self.angle >= 360:
            self.angle = 0
            
    def draw(self, screen):
        # Calculate the start and end points of the arc
        start_angle = math.radians(self.angle)
        end_angle = math.radians(self.angle + 270)
        
        # Draw a thicker arc that fades in transparency
        for i in range(self.width):
            adjusted_radius = self.radius - i
            
            # Calculate color with fading transparency
            alpha = 255 - int(255 * i/self.width)
            arc_color = (self.color[0], self.color[1], self.color[2], alpha)
            
            # Create a surface with per-pixel alpha
            surface = pygame.Surface((adjusted_radius * 2, adjusted_radius * 2), pygame.SRCALPHA)
            rect = pygame.Rect(0, 0, adjusted_radius * 2, adjusted_radius * 2)
            
            # Draw the arc on the surface
            pygame.draw.arc(surface, arc_color, rect, start_angle, end_angle, 1)
            
            # Blit the surface onto the screen
            screen.blit(surface, (self.x - adjusted_radius, self.y - adjusted_radius))
