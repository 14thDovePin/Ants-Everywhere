"""Game overlays."""

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
        # self.overlay_rect = self.fs_text_rect.union(self.fs_slider_rect)

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


