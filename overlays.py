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

    def fs_slider(self):
        """Fear strength slider."""
        self.fs_slider_value = 0

        # Text
        self.fs_text = "Fear Strength"
        self.fs_text_color = (0, 0, 0)
        self.fs_text_image = self.font_24tnr.render(self.fs_text, True, self.fs_text_color)
        self.fs_text_rect = self.fs_text_image.get_rect()
        self.fs_text_rect.topleft = self.screen_rect.topleft
        self.fs_text_rect.x += self.fs_text_rect.height/2
        self.fs_text_rect.y += self.fs_text_rect.height/2

        # Slider
        self.fs_slider_image = pygame.image.load('assets/slider.png')
        self.fs_slider_rect = self.fs_slider_image.get_rect()
        self.fs_slider_rect.centery = self.fs_text_rect.centery
        self.fs_slider_rect.left = self.fs_text_rect.right + self.fs_text_rect.height/2

        # Hex Button
        self.fs_button_image = pygame.image.load('assets/slider_hex_button.png')
        self.fs_button_image1 = pygame.image.load('assets/slider_hex_button1.png')
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
        else:
            self.fsb_drag = False

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


