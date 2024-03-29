"""Game objects."""

from math import *
from random import *
import time

import pygame
from pygame.sprite import Sprite

Vec2 = pygame.Vector2


class Ant(Sprite):
    """Ant class."""

    def __init__(self, main_game):
        super().__init__()
        # Load main_game screen rectangle.
        self.screen = main_game.screen
        self.screen_rect = main_game.screen_rect

        # Load object image and rectangles.
        self.image = pygame.image.load('assets/pointer_center.png').convert_alpha()
        self.image1 = pygame.image.load('assets/pointer_center1.png').convert_alpha()
        self.image_pointer = pygame.image.load('assets/pointer_slim.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.fresh_image_pointer = self.image_pointer  # Used for transform.
        self.rect = self.image.get_rect()  # Rectangle for pointer center.
        self.rectp = self.image_pointer.get_rect()  # Rectangle for pointer.

        # Predetermine object's screen location.  ####
        self.rect.centerx = randint(1, self.screen_rect.width)
        self.rect.centery = randint(1, self.screen_rect.height)
        self.position = Vec2(self.rect.centerx, self.rect.centery)

        self.rectp.center = self.rect.center
        # self.mask = pygame.mask.from_surface(self.image_center)

        self._load_attributes()

    def _load_attributes(self):
        """Main object attributes."""
        self.vel = Vec2(0, 0)
        self.friction = True
        self.rotation = 0  # Facing right.
        self.max_speed = 0.5  # 2
        self.manual_mode = False
        self.running = False
        self.touch = False

        self.acceleration = Vec2(0.2, 0)
        self.friction_speed = 0.02
        self.rotation_speed = 1  # 2 | Degrees.

        self.turning_angle = 0  # Degrees.
        self.time_snap = time.time()  # Snapshot of current time.
        self.time_left = 0  # Seconds.

    def loop_update(self):
        """Attach to main game loop."""

        # Speed limit.
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        if self.manual_mode:
            self.manual_ctrl()  # Manual control.
        else:
            self.auto_ctrl()

        # Updates velocity, internal position, and rectangle location.
        self.position += self.vel
        self.rectp.center = self.position

        self.rect.center = self.rectp.center
        self.touch = False

    def run_away(self):
        """Runs away from specific x y point."""
        if not self.running:
            # Running switch
            self.running = True

            # Calculate point to point angle.
            cursor_pos = pygame.mouse.get_pos()
            dx = self.rectp.x - cursor_pos[0]
            dy = self.rectp.y - cursor_pos[1]
            rads = atan2(-dy,dx)
            final = degrees(rads)
            if final < 0:
                final = final + 360

            # print(f'Away Angle: {final}')  ###
            # print(f'Object Rotation: {self.rotation}')  ###
            # print(f'Calculated: {final - self.rotation}')  ###
            # print()  ###

            # Set final away angle
            self.away_angle = final - self.rotation
            if self.away_angle > 180:
                self.away_angle -=360
            elif self.away_angle < -180:
                self.away_angle +=360
            self.turning_angle = self.away_angle
            self.rotation_speed = 2

    def auto_ctrl(self):
        """Automatic Ant movement."""
        self.time_current = time.time()

        # Random choice time.
        if self.time_left < self.time_current:
            self.time_left = self.time_current + uniform(0.5, 1)
            # Random turning angle.
            if self.turning_angle == 0:
                self.turning_angle = randint(-120, 120)
                self.rotation_speed = uniform(0.2, 2)

        # Turning mechanics.
        if self.turning_angle > self.rotation_speed:
            self.rotate(self.rotation_speed)
            # print('left')  ###
            self.turning_angle -= self.rotation_speed
        elif self.turning_angle < -self.rotation_speed:
            self.rotate(-self.rotation_speed)
            # print('right')  ###
            self.turning_angle += self.rotation_speed
        else:
            self.running = False
            self.turning_angle = 0

        # Continious acceleration
        self.vel += self.acceleration

    def manual_ctrl(self):
        """Manual Ant control."""
        keys = pygame.key.get_pressed()

        # Acceleration
        if keys[pygame.K_LEFT]:
            self.rotate(self.rotation_speed)
        if keys[pygame.K_RIGHT]:
            self.rotate(-self.rotation_speed)
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

        # Friction.
        if not any([
            keys[pygame.K_UP],
            keys[pygame.K_DOWN]
            ]) and self.friction:

            self.vel.x -= self.vel.x * self.friction_speed
            self.vel.y -= self.vel.y * self.friction_speed
            if (-0.1 < self.vel.x < 0.1) and (-0.1 < self.vel.y < 0.1):
                self.vel.x = 0
                self.vel.y = 0

    def rotate(self, rotation_speed):
        """Rotate the acceleration vector."""
        self.acceleration.rotate_ip(-rotation_speed)
        self.rotation += rotation_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
        self.image_pointer = pygame.transform.rotozoom(self.fresh_image_pointer, self.rotation, 1)
        self.rectp = self.image_pointer.get_rect(center=self.rectp.center)

    def blitme(self):
        """Draws the object at it's predetermined location."""
        # pygame.draw.rect(self.screen, (230, 230, 230), self.rectp)  ###
        self.screen.blit(self.image_pointer, self.rectp)

        # pygame.draw.rect(self.screen, (255, 102, 255), self.rect)  ###
        if not self.touch:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image1, self.rect)


class CursorCircle(Sprite):
    """The Circle of phobia for the cursor."""

    def __init__(self, main_game):
        super().__init__()
        # Load main_game screen rectangle.
        self.screen = main_game.screen
        self.screen_rect = main_game.screen_rect
        self.font = pygame.font.SysFont(None, 24, False, False)

        # self.image = pygame.image.load('assets/circle_of_fear.png').convert_alpha()
        self.image = pygame.image.load('assets/circle.png').convert_alpha()
        self.fresh_image = self.image  # Used for transform.
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.wxh = (self.rect.width, self.rect.height) ###
        self.scale = 1

        self.show = False

    def loop_update(self, center_circle):
        """Object loop update."""
        if not center_circle:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center = self.screen_rect.center

    def resize(self, new_scale):
        """Resizes circle."""
        if new_scale != self.scale:
            self.scale = new_scale
            new_scale = new_scale/100
            set_scale = (
                round(self.wxh[0]+self.wxh[0]*new_scale),
                round(self.wxh[1]+self.wxh[1]*new_scale)
                )
            self.image = pygame.transform.scale(self.fresh_image, set_scale)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draws the object at it's predetermined location."""
        if self.show:
            self.screen.blit(self.image, self.rect)
