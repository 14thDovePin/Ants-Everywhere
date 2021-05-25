"""Game overlays."""
import sys

import pygame
from pygame.sprite import Sprite


class InGame(Sprite):
    """In game overlays."""

    def __init__(self, main_game):
        super().__init__()
        # Load main_game screen rectangle.
        self.screen = main_game.screen
        self.screen_rect = main_game.screen_rect

        self.font_24tnr = pygame.font.SysFont("timesnewroman", 24, False, False)

        # Initialize
        self.fs_slider()
        self.sc_check_box()
        self.overlay_border()

    def fs_slider(self):
        """Fear strength slider."""
        # Attributes for external use.
        self.fs_slider_value = 0  # Fear stength slider value.
        self.fs_button_press = False

        # Text
        self.fs_text = "Fear Strength"
        self.fs_text_color = (0, 0, 0)
        self.fs_text_image = self.font_24tnr.render(self.fs_text, True, self.fs_text_color)
        self.fs_text_rect = self.fs_text_image.get_rect()
        self.fs_text_rect.topleft = self.screen_rect.topleft
        self.fs_text_rect.x += self.fs_text_rect.height/2
        self.fs_text_rect.y += self.fs_text_rect.height/2

        # Slider
        self.fs_slider_image = pygame.image.load('assets/slider.png').convert_alpha()
        self.fs_slider_rect = self.fs_slider_image.get_rect()
        self.fs_slider_rect.centery = self.fs_text_rect.centery
        self.fs_slider_rect.left = self.fs_text_rect.right + self.fs_text_rect.height/2

        # Hex Button
        self.fs_button_image = pygame.image.load('assets/slider_hex_button.png').convert_alpha()
        self.fs_button_image1 = pygame.image.load('assets/slider_hex_button1.png').convert_alpha()
        self.fs_button_mask = pygame.mask.from_surface(self.fs_button_image)
        self.fs_button_rect = self.fs_button_image.get_rect()
        self.fs_button_rect.centery = self.fs_slider_rect.centery
        self.fs_button_rect.centerx = self.fs_slider_rect.left + (self.fs_slider_rect.height/2)
        self.fs_button_xlimit = (  # x axis button movement limit.
            self.fs_slider_rect.left + (self.fs_slider_rect.height/2),
            self.fs_slider_rect.right - (self.fs_slider_rect.height/2)
            )
        self.fsb_touching = False
        self.fsb_drag = False

    def fss_loop_update(self):
        """Fs slider main loop update."""
        mouse_press = pygame.mouse.get_pressed()

        # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
        mouse_pos = pygame.mouse.get_pos()
        pos_in_mask = mouse_pos[0] - self.fs_button_rect.x, mouse_pos[1] - self.fs_button_rect.y
        colliding = self.fs_button_rect.collidepoint(*mouse_pos) and self.fs_button_mask.get_at(pos_in_mask)
        # colliding = self.fs_button_rect.collidepoint(mouse_pos)

        # Slider button logic.
        if colliding or self.fsb_drag:
            self.fsb_touching = True
        else:
            self.fsb_touching = False

        if mouse_press[0] and (self.fs_button_xlimit[0] < mouse_pos[0] < self.fs_button_xlimit[1]) and colliding:
            self.fsb_drag = True

        if self.fsb_drag and mouse_press[0] and (self.fs_button_xlimit[0] < mouse_pos[0] < self.fs_button_xlimit[1]):
            self.fs_button_rect.centerx = mouse_pos[0]
            self.fs_button_press = True
        else:
            self.fsb_drag = False
            self.fs_button_press = False

        # Set slider value for external use.
        total = self.fs_button_xlimit[1]-self.fs_button_xlimit[0]
        current = self.fs_button_rect.centerx-self.fs_button_xlimit[0]
        self.fs_slider_value = round(current/total*100)
        # print(round(current/total*100))

    def fs_slider_blit(self):
        """Blits fs_slider."""
        self.screen.blit(self.fs_text_image, self.fs_text_rect)
        self.screen.blit(self.fs_slider_image, self.fs_slider_rect)
        if self.fsb_touching:
            self.screen.blit(self.fs_button_image1, self.fs_button_rect)
        else:
            self.screen.blit(self.fs_button_image, self.fs_button_rect)

    def sc_check_box(self):
        """Show Circle check box."""

        # Attributes for external use.
        self.sc_cb = 0  # Show circle check box state.

        # Text.
        self.sc_text = "Show Circle"
        self.sc_text_color = (0, 0, 0)
        self.sc_text_image = self.font_24tnr.render(self.sc_text, True, self.sc_text_color)
        self.sc_text_rect = self.sc_text_image.get_rect()
        self.sc_text_rect.topleft = self.fs_text_rect.bottomleft
        self.sc_text_rect.y += self.sc_text_rect.height/2

        # Check box.
        self.sc_cb_image = pygame.image.load('assets/check_box.png').convert_alpha()
        self.sc_cb_image1 = pygame.image.load('assets/check_box1.png').convert_alpha()
        self.sc_cb_mask = pygame.mask.from_surface(self.sc_cb_image)
        self.sc_cb_rect = self.sc_cb_image.get_rect()
        self.sc_cb_rect.left = self.sc_text_rect.right + self.sc_text_rect.height/2
        self.sc_cb_rect.y = self.sc_text_rect.y

        self.sc_cb_touching = False
        self.sc_cb_pressed = False
        self.sc_cb_lock = False

    def sc_cb_loop_update(self):
        """Sc check box main loop update."""
        mouse_press = pygame.mouse.get_pressed()

        # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
        mouse_pos = pygame.mouse.get_pos()
        pos_in_mask = mouse_pos[0] - self.sc_cb_rect.x, mouse_pos[1] - self.sc_cb_rect.y
        colliding = self.sc_cb_rect.collidepoint(*mouse_pos) and self.sc_cb_mask.get_at(pos_in_mask)

        # Checkbox logic.
        if colliding:
            self.sc_cb_touching = True
        else:
            self.sc_cb_touching = False

        if mouse_press[0] and colliding and not self.sc_cb_lock:
            if not self.sc_cb_pressed:
                self.sc_cb_pressed = True
            else:
                self.sc_cb_pressed = False
            self.sc_cb_lock = True

        if not mouse_press[0]:
            self.sc_cb_lock = False

    def sc_cb_blit(self):
        """Blits show circle check box."""
        self.screen.blit(self.sc_text_image, self.sc_text_rect)

        if not self.sc_cb_pressed:
            if self.sc_cb_touching:
                self.screen.blit(self.sc_cb_image1, self.sc_cb_rect)
            else:
                self.screen.blit(self.sc_cb_image, self.sc_cb_rect)
        else:
            self.screen.blit(self.sc_cb_image1, self.sc_cb_rect)

    def overlay_border(self):
        """Current overlay border box."""

        self.ob_image = pygame.image.load('assets/overlay_border_box.png').convert_alpha()
        rects = [
            self.fs_slider_rect,
            self.sc_text_rect,
            self.sc_cb_rect,
        ]
        self.ob_margine = 15
        self.ob_rect_temp = self.fs_text_rect.unionall(rects)
        wxh = (self.ob_rect_temp.width + self.ob_margine, self.ob_rect_temp.height + self.ob_margine)

        self.ob_image = pygame.transform.scale(self.ob_image, wxh)
        self.ob_rect = self.ob_image.get_rect(center=self.ob_rect_temp.center)

    def ob_blit(self):
        """Blits overlay border box."""
        # pygame.draw.rect(self.screen, (204, 51, 153), self.ob_rect)
        self.screen.blit(self.ob_image, self.ob_rect)


class MenuOverlay:
    """Menu overlays."""

    def __init__(self, main_game):
        """Initialize class asstets."""
        super().__init__()
        # Load main_game screen rectangle.
        self.screen = main_game.screen
        self.screen_rect = main_game.screen_rect
        self.main_game = main_game

        # Assets
        self.first_run = True
        self.button_margine = 15
        self.button_lock = False

        self._pause_mask()
        self._play()
        self._resume()
        self._quit()

    def _pause_mask(self):
        """A mask to cover the screen when paused."""
        self.pm_img = pygame.transform.scale(
            pygame.image.load('assets/pause_mask.png'),
            (self.screen_rect.width, self.screen_rect.height)
            ).convert_alpha()
        self.pm_rect = self.pm_img.get_rect()

        # Set rectangle position.
        self.pm_rect.center = self.screen_rect.center

    def _play(self):
        """Play button."""
        self.play_img = pygame.image.load('assets/play_button.png').convert_alpha()
        self.play_img1 = pygame.image.load('assets/play_button1.png').convert_alpha()
        self.play_mask = pygame.mask.from_surface(self.play_img)
        self.play_rect = self.play_img.get_rect()
        self.play_touching = False
        self.play_pressed = False

        # Set rectangle position.
        self.play_rect.centerx = self.screen_rect.centerx
        self.play_rect.bottom = self.screen_rect.centery - self.button_margine

    def _resume(self):
        """Resume button."""
        self.resume_img = pygame.image.load('assets/resume_button.png').convert_alpha()
        self.resume_img1 = pygame.image.load('assets/resume_button1.png').convert_alpha()
        self.resume_mask = pygame.mask.from_surface(self.resume_img)
        self.resume_rect = self.resume_img.get_rect()
        self.resume_touching = False
        self.resume_pressed = False

        # Set rectangle position.
        self.resume_rect.centerx = self.screen_rect.centerx
        self.resume_rect.bottom = self.screen_rect.centery - self.button_margine

    def _quit(self):
        """Quit button."""
        self.quit_img = pygame.image.load('assets/quit_button.png').convert_alpha()
        self.quit_img1 = pygame.image.load('assets/quit_button1.png').convert_alpha()
        self.quit_mask = pygame.mask.from_surface(self.quit_img)
        self.quit_rect = self.quit_img.get_rect()
        self.quit_touching = False
        self.quit_pressed = False

        # Set rectangle position.
        self.quit_rect.centerx = self.screen_rect.centerx
        self.quit_rect.top = self.screen_rect.centery + self.button_margine

    def buttons_loop_update(self):
        """Buttons loop update."""
        # Reset mouse button lock by condition.
        mouse_press = pygame.mouse.get_pressed()
        if not mouse_press[0]:
            self.button_lock = False

        # Reset buttons
        self.play_pressed = False
        self.resume_pressed = False
        self.quit_pressed = False

        # Logic event.
        self.play_touching = self.buttons_logic_update(
            self.play_rect,
            self.play_mask,
            self.play_touching
            )
        self.resume_touching = self.buttons_logic_update(
            self.resume_rect,
            self.resume_mask,
            self.resume_touching
            )
        self.quit_touching = self.buttons_logic_update(
            self.quit_rect,
            self.quit_mask,
            self.quit_touching
            )

        # Press event.
        if self.first_run:
            self.play_pressed = self.buttons_press_update(
                self.play_rect,
                self.play_mask,
                self.play_pressed
                )
        else:
            self.resume_pressed = self.buttons_press_update(
                self.resume_rect,
                self.resume_mask,
                self.resume_pressed
                )
        self.quit_pressed = self.buttons_press_update(
            self.quit_rect,
            self.quit_mask,
            self.quit_pressed
            )

        # Actions for press event.
        if self.play_pressed:
            print('Play pressed!')
            self.main_game.stats.GAME_ACTIVE = True
            self.first_run = False
        if self.resume_pressed:
            print('Resume pressed!')
            self.main_game.stats.GAME_ACTIVE = True
        if self.quit_pressed:
            print('Quit Pressed!')
            sys.exit()


    def buttons_logic_update(self, obj_rect, obj_mask, obj_touch):
        """Buttons logic update."""
        mouse_press = pygame.mouse.get_pressed()

        # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
        mouse_pos = pygame.mouse.get_pos()
        pos_in_mask = mouse_pos[0] - obj_rect.x, mouse_pos[1] - obj_rect.y
        colliding = obj_rect.collidepoint(*mouse_pos) and obj_mask.get_at(pos_in_mask)

        # Touch logic.
        if colliding:
            return True
        else:
            return False

    def buttons_press_update(self, obj_rect, obj_mask, obj_pressed):
        """Buttons logic update."""
        mouse_press = pygame.mouse.get_pressed()

        # https://stackoverflow.com/questions/52843879/detect-mouse-event-on-masked-image-pygame
        mouse_pos = pygame.mouse.get_pos()
        pos_in_mask = mouse_pos[0] - obj_rect.x, mouse_pos[1] - obj_rect.y
        colliding = obj_rect.collidepoint(*mouse_pos) and obj_mask.get_at(pos_in_mask)

        # Press logic.
        if colliding and mouse_press[0] and not self.button_lock:
            self.button_lock = True
            return True

    def blit_buttons(self):
        """Blits buttons."""
        self.screen.blit(self.pm_img, self.pm_rect)
        if self.first_run:
            if not self.play_touching:
                self.screen.blit(self.play_img, self.play_rect)
            else:
                self.screen.blit(self.play_img1, self.play_rect)

        else:
            if not self.resume_touching:
                self.screen.blit(self.resume_img, self.resume_rect)
            else:
                self.screen.blit(self.resume_img1, self.resume_rect)

        if not self.quit_touching:
            self.screen.blit(self.quit_img, self.quit_rect)
        else:
            self.screen.blit(self.quit_img1, self.quit_rect)
