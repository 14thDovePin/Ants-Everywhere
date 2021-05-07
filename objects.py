"""
Game objects.
"""

import math

import pygame
from pygame.sprite import Sprite

Vec2 = pygame.math.Vector2


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

        self._load_attributes()

    def _load_attributes(self):
        """Main object attributes."""
        self.vel = Vec2(0, 0)
        self.speed = 0.2
        self.friction = 0.02
        self.rotation = 0  # ↓↓↓ #
        # Initial object rotation in degrees. Facing down.
        # 0° sits at the south direction rather than east.
        self.max_speed = 2
        self.position = Vec2(self.rect.centerx, self.rect.centery)

    def cah(self, a, b):
        """Calculates the object's degree of rotation based on it's velocity vectors."""
        float(a)
        b = float(-b)

        if (a > 0) and (b == 0):
            return 0
        elif (a == 0) and (b > 0):
            return 90
        elif (a < 0) and (b == 0):
            return 180
        elif (a == 0) and (b < 0):
            return 270
        elif (a == 0) and (b == 0):
            return self.rotation
        else:
            h = math.sqrt(a**2 + b**2)
            rads = math.acos(a/h)
            final = math.degrees(rads)
            if b < 0:
                final = abs(final - 360)
            return round(final)

    def loop_update(self):
        """Attach to main game loop."""
        self.acceleration = Vec2(0, 0)
        keys = pygame.key.get_pressed()

        # Acceleration
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -self.speed
            self.rotate()
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.speed
            self.rotate()
        if keys[pygame.K_UP]:
            self.acceleration.y = -self.speed
            self.rotate()
        if keys[pygame.K_DOWN]:
            self.acceleration.y = self.speed
            self.rotate()

        # Friction.
        if not any([keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT],
            keys[pygame.K_UP],
            keys[pygame.K_DOWN]
            ]):

            self.vel.x -= self.vel.x * self.friction
            self.vel.y -= self.vel.y * self.friction
            if (-0.1 < self.vel.x < 0.1) and (-0.1 < self.vel.y < 0.1):
                self.vel.x = 0
                self.vel.y = 0

        # Break.
        if keys[pygame.K_SPACE]:
            self.vel.x -= self.vel.x * 0.1
            self.vel.y -= self.vel.y * 0.1
            if (-0.1 < self.vel.x < 0.1) and (-0.1 < self.vel.y < 0.1):
                self.vel.x = 0
                self.vel.y = 0

        # Speed limit.
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Updates velocity, internal position, and rectangle location.
        self.vel += self.acceleration
        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        """Rotates object image."""
        self.rotation = self.cah(self.vel.x, self.vel.y)
        self.image = pygame.transform.rotozoom(self.fresh_image, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def blitme(self):
        """Draws the object at it's predetermined location."""
        self.screen.blit(self.image, self.rect)
