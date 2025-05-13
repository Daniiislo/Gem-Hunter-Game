import pygame
import sys

from src.config import SCREEN_HEIGHT, SCREEN_WIDTH
from src.Game.state_management import GameState
from src.Game.event_management import EventHandler
from src.Game.screen_management import ScreenManager

class GameRunner:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gem Hunter Game")

        self.game_state = GameState()
        self.all_sprites = pygame.sprite.Group()
        self.gui = ScreenManager(self.game_state)
        self.events = EventHandler(self.game_state, self.gui)

    def main(self):
        clock = pygame.time.Clock()
        dt = 0

        while self.game_state.running:
            self.game_state.current_time = pygame.time.get_ticks()
            
            # Get all events once
            events = pygame.event.get()
            
            # Let EventHandler process all events
            self.events.handle_all_events(events)
            
            self.screen.fill((0, 0, 0))

            # Draw current UI
            self.gui.draw(self.screen)
            
            pygame.display.flip()
            dt = clock.tick(self.game_state.fps) / 1000

        pygame.quit()
        sys.exit()