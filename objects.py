"""
Game objects.
"""

from math import *
import pygame
from pygame.sprite import Sprite

Vec2 = pygame.Vector2


class Ant(Sprite):
    """Ant class."""

    def __init__(self, main_game):
        super().__init__()
        # Load main_game screen rectangle.
        self.screen = main_game.screen
        self.screen_rect = main_game.screen.get_rect()

        # Load object image and rectangles.
        self.image = pygame.image.load('assets/pointer_slim.png')
        self.fresh_image = self.image  # Used for transform.
        self.rect = self.image.get_rect()

        # Predetermine object's screen location.  ####
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.position = Vec2(self.rect.centerx, self.rect.centery)

        self._load_attributes()

    def _load_attributes(self):
        """Main object attributes."""
        self.vel = Vec2(0, 0)
        self.acceleration = Vec2(0.2, 0)
        self.speed = 0.2  # Movement speed.
        self.friction = True
        self.friction_speed = 0.02
        self.rotation = 0  # Facing left.
        self.rotation_speed = 2  # Degrees.
        self.max_speed = 2

    def loop_update(self):
        """Attach to main game loop."""

        # Speed limit.
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Friction.
        keys = pygame.key.get_pressed()
        if not any([
            keys[pygame.K_UP],
            keys[pygame.K_DOWN]
            ]) and self.friction:

            self.vel.x -= self.vel.x * self.friction_speed
            self.vel.y -= self.vel.y * self.friction_speed
            if (-0.1 < self.vel.x < 0.1) and (-0.1 < self.vel.y < 0.1):
                self.vel.x = 0
                self.vel.y = 0

        self.manual_ctrl()  # Manual control.

        # Updates velocity, internal position, and rectangle location.
        self.position += self.vel
        self.rect.center = self.position

    def manual_ctrl(self):
        """Manual Ant control."""
        keys = pygame.key.get_pressed()

        # Acceleration
        if keys[pygame.K_LEFT]:
            self.rotate(-self.rotation_speed)
        if keys[pygame.K_RIGHT]:
            self.rotate(self.rotation_speed)
        if keys[pygame.K_UP]:
            self.vel += self.acceleration
        if keys[pygame.K_DOWN]:
            self.vel -= self.acceleration

        # Break.
        if keys[pygame.K_SPACE]:
            self.vel.x -= self.vel.x * 0.1
            self.vel.y -= self.vel.y * 0.1
            if (-0.1 < self.vel.x < 0.1) and (-0.1 < self.vel.y < 0.1):
                self.vel.x = 0
                self.vel.y = 0

    def rotate(self, rotation_speed):
        """Rotate the acceleration vector."""
        self.acceleration.rotate_ip(rotation_speed)
        self.rotation += rotation_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
        self.image = pygame.transform.rotozoom(self.fresh_image, -self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def blitme(self):
        """Draws the object at it's predetermined location."""
        self.screen.blit(self.image, self.rect)
