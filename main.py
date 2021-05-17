import sys  # Created from pygame_initial_template v1.3 -TherLaf (My own template lol)
import time
from random import randint

import pygame

from objects import *
from preference import *


class MainGame:  # ++++++++++++++++++++++++++++++++ MAIN GAME ++++++++++++++++++++++++++++++++
    """Overall class to manage game behavior and assets."""

    # ================================ GAME INITIALIZATION ================================
    def __init__(self):
        """Initialize game setup, presets and assets."""
        pygame.init()

        self.settings = GameSettings()
        self.stats = Stats(self)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.game_window_caption)

        self._assets()

        self.cycle_start = time.time()  # Starts fps limiter cycle.

    def _assets(self):
        """Insert game objects here ################"""

        # Colony
        self.colony = pygame.sprite.Group()
        for _ in range(360):  # y=90 Ant samples that forms a circle.
            ant = Ant(self)
            ant.rotate(_*1)  # x = 360 / y
            # ant.friction = False
            # ant.manual_mode = True
            self.colony.add(ant)
        self.ccirc = CursorCircle(self)

    # ================================ MAIN GAME LOOP ================================
    def run_game(self):
        """Starts the main loop of the game."""
        while True:
            self._check_events()
            if self.stats.GAME_ACTIVE:
                # Insert Object rect update function or other functions here ################
                self._border_pass()
                for ant in self.colony:
                    ant.loop_update()
                self.ccirc.loop_update()

                # Collision evasion.
                for i in pygame.sprite.spritecollide(self.ccirc, self.colony, False, pygame.sprite.collide_mask):
                    i.run_away()

            self._update_screen()
            self._limit_fps()

    # ================================ KEYBOARD CONTROLS ================================
    def _check_events(self):
        """Response to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Response to keys pressed"""
        if event.key == pygame.K_UP:
            print('pressed up button')
        elif event.key == pygame.K_DOWN:
            print('pressed down button')
        elif event.key == pygame.K_LEFT:
            print('pressed left button')
        elif event.key == pygame.K_RIGHT:
            print('pressed right button')
        elif event.key == pygame.K_SPACE:
            print('pressed space bar')
        # Insert more key events here ################

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Response to keys released"""
        if event.key == pygame.K_UP:
            print('released up button')
        elif event.key == pygame.K_DOWN:
            print('released down button')
        elif event.key == pygame.K_LEFT:
            print('released left button')
        elif event.key == pygame.K_RIGHT:
            print('released right button')
        elif event.key == pygame.K_SPACE:
            print('released space bar')
        # Insert more key events here ################

    # ================================ KEYBOARD FUNCTIONS ================================
    # Insert more keyboard function, method or helper methods here.

    # ================================ MAIN SCREEN FUNCTIONS ================================
    def _update_screen(self):
        """Updates images/game objects on the screen, and flip to the most recent screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)  # Background color fill.

        # Insert game object/s' blit or surface update here ################
        # self.ccirc.blitme()  ###
        for ant in self.colony:
            ant.blitme()

        pygame.display.flip()  # Draws most recent surface.

    def _limit_fps(self):
        """Monitors and limits frames per second."""
        curr_time = time.time()  # Current time.
        diff = curr_time - self.cycle_start  # Takes time difference.
        delay = max(1.0 / self.settings.target_fps - diff, 0)  # Calculates delay to limit fps.
        time.sleep(delay)  # Delays program to reach target fps.
        fps = 1.0 / (delay + diff)  # FPS is based on total time ("processing" diff time + "wasted" delay time)
        self.cycle_start = curr_time  # Resets timing cycle.
        pygame.display.set_caption(
            f'{self.settings.game_window_caption} | [{int(fps)}]'  # Displays fps in game caption.
        )

    # ================================ GAME FUNCTIONS ================================
    # Insert more function, method or helper methods here.

    def _border_pass(self):
        """Moves objects passing through one edge of the window to the opposite."""
        for ant in self.colony:
            if ant.rect.left > self.settings.screen_width:
                ant.rect.right = 0
                ant.position[0] = ant.rect.centerx
            if ant.rect.right < 0:
                ant.rect.left = self.settings.screen_width
                ant.position[0] = ant.rect.centerx
            if ant.rect.top > self.settings.screen_height:
                ant.rect.bottom = 0
                ant.position[1] = ant.rect.centery
            if ant.rect.bottom < 0:
                ant.rect.top = self.settings.screen_height
                ant.position[1] = ant.rect.centery
            # ant.position = pygame.math.Vector2(ant.rect.centerx, ant.rect.centery)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- GAME OBJECTS =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Insert more game class here


if __name__ == '__main__':  # %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%- MAIN PROGRAM %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-
    main_game = MainGame()
    main_game.run_game()
