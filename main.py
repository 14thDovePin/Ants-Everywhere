import sys  # Created from pygame_initial_template v1.3 -TherLaf (My own template lol)
import time
from random import randint

import pygame

from objects import *
from overlays import *
from preference import *


class MainGame:  # ++++++++++++++++++++++++++++++++ MAIN GAME ++++++++++++++++++++++++++++++++
    """Overall class to manage game behavior and assets."""

    # ================================ GAME INITIALIZATION ================================
    def __init__(self):
        """Initialize game setup, presets and assets."""
        pygame.init()

        self.settings = GameSettings()
        self.stats = Stats(self)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.game_window_caption)

        self._assets()

    def _assets(self):
        """Insert game objects here ################"""

        # Overlays
        self.ingame_overlay = InGame(self)
        self.menu_overlay = MenuOverlay(self)

        # Colony.
        self.colony = pygame.sprite.Group()
        for _ in range(800):  # Max 800
            ant = Ant(self)
            ant.rotate(randint(1, 360))
            # ant.manual_mode = True
            # ant.friction = False
            self.colony.add(ant)
        self.ccirc = CursorCircle(self)

    # ================================ MAIN GAME LOOP ================================
    def run_game(self):
        """Starts the main loop of the game."""
        while True:
            self._check_events()
            if self.stats.GAME_ACTIVE:
                # Update caption, limit frames.
                caption = self.settings.game_window_caption+" ["+str(round(self.clock.get_fps()))+"]"
                pygame.display.set_caption(caption)
                self.clock.tick(self.settings.target_fps)

                # Overlay updates.
                self.ingame_overlay.fss_loop_update()
                self.ingame_overlay.sc_cb_loop_update()
                self.ingame_overlay.pause_loop_update()

                # Insert Object rect update function or other functions here ################
                self._border_pass()
                for ant in self.colony:
                    ant.loop_update()

                fss = (  # Fear Strength Slider values.
                    self.ingame_overlay.fs_button_press,
                    self.ingame_overlay.fs_slider_value
                    )
                sc_cb = (  # Show Circle Check Box values.
                    self.ingame_overlay.sc_cb_touching,
                    self.ingame_overlay.sc_cb_pressed
                    )
                self.ccirc.loop_update(any([fss[0], sc_cb[0]]))
                self.ccirc.resize(fss[1])

                if any([fss[0], sc_cb[0]]) or sc_cb[1]:
                    self.ccirc.show = True
                else:
                    self.ccirc.show = False

                # Ant collision evasion.
                if not any([fss[0], sc_cb[0]]):
                    collisions = pygame.sprite.spritecollide(self.ccirc, self.colony, False, pygame.sprite.collide_mask)
                    for ant in collisions:
                        ant.run_away()
                        ant.touch = True
            else:
                self.menu_overlay.buttons_loop_update()

            self._update_screen()
            # self._limit_fps()

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

        # Pause keys.
        elif event.key == pygame.K_ESCAPE:
            if not self.menu_overlay.first_run:
                if self.stats.GAME_ACTIVE:
                    self.stats.GAME_ACTIVE = False
                else:
                    self.stats.GAME_ACTIVE = True
        elif event.key == pygame.K_PAUSE:
            if not self.menu_overlay.first_run:
                if self.stats.GAME_ACTIVE:
                    self.stats.GAME_ACTIVE = False
                else:
                    self.stats.GAME_ACTIVE = True

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
        for ant in self.colony:
            ant.blitme()
        self.ccirc.blitme()  ###

        # In-game overlay.
        # pygame.draw.ellipse(self.screen, (204, 0, 204), self.ingame_overlay.overlay_rect)
        self.ingame_overlay.ob_blit()
        self.ingame_overlay.fs_slider_blit()
        self.ingame_overlay.sc_cb_blit()
        self.ingame_overlay.pause_blit()

        # Menu overlay.
        if not self.stats.GAME_ACTIVE:
            self.menu_overlay.blit_buttons()

        pygame.display.flip()  # Draws most recent surface.

    # ================================ GAME FUNCTIONS ================================
    # Insert more function, method or helper methods here.

    def _border_pass(self):
        """Moves objects passing through one edge of the window to the opposite."""
        for ant in self.colony:
            if ant.rectp.left > self.settings.screen_width:
                ant.rectp.right = 0
                ant.position[0] = ant.rectp.centerx
            if ant.rectp.right < 0:
                ant.rectp.left = self.settings.screen_width
                ant.position[0] = ant.rectp.centerx
            if ant.rectp.top > self.settings.screen_height:
                ant.rectp.bottom = 0
                ant.position[1] = ant.rectp.centery
            if ant.rectp.bottom < 0:
                ant.rectp.top = self.settings.screen_height
                ant.position[1] = ant.rectp.centery


if __name__ == '__main__':  # %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%- MAIN PROGRAM %-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-
    main_game = MainGame()
    main_game.run_game()
