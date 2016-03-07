from settings import *
from resources import *
import pygame
import math
vec = pygame.math.Vector2

# Creating a player class
class Player(pygame.sprite.Sprite):
    # Initialize the player class
    def __init__(self, collide_list):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/player/player_standing.png")
        self.rect = pygame.Rect((0, 0, 40, 40))
        self.rect.center = (display_width/2, display_height/2)
        self.collide_list = collide_list

        self.moving_up = False
        self.moving_left = False
        self.moving_down = False
        self.moving_right = False

        self.up_lock = False
        self.left_lock = False
        self.down_lock = False
        self.right_lock = False

        self.speed_x = 0
        self.speed_y = 0

    # Update the player class
    def update(self):
        self.speed_x = 0
        self.speed_y = 0

        # Event handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.up_lock:
            self.moving_up = True
            self.down_lock = True
        else:
            self.moving_up = False
            self.down_lock = False

        if keys[pygame.K_LEFT] and not self.left_lock:
            self.moving_left = True
            self.right_lock = True
        else:
            self.moving_left = False
            self.right_lock = False

        if keys[pygame.K_DOWN] and not self.down_lock:
            self.moving_down = True
            self.up_lock = True
        else:
            self.moving_down = False
            self.up_lock = False

        if keys[pygame.K_RIGHT] and not self.right_lock:
            self.moving_right = True
            self.left_lock = True
        else:
            self.moving_right = False
            self.left_lock = False

        # Make player movement
        if self.moving_up:
            self.speed_y = -5
        if self.moving_left:
            self.speed_x = -5
        if self.moving_down:
            self.speed_y = 5
        if self.moving_right:
            self.speed_x = 5

        # Make diagonal movment as fast as normal:
        if self.moving_up and self.moving_left or self.moving_up and self.moving_right:
            self.speed_x *= 0.707
            self.speed_y *= 0.707

        if self.moving_down and self.moving_left or self.moving_down and self.moving_right:
            self.speed_x *= 0.707
            self.speed_y *= 0.707

        # X-axis movement
        self.rect.x += self.speed_x

        # Check if the player hit anything during X-movement
        hit_list = pygame.sprite.spritecollide(self, self.collide_list, False)
        for hits in hit_list:
            if self.speed_x > 0:
                self.rect.right = hits.rect.left
            else:
                self.rect.left = hits.rect.right

        # Y-axis movement
        self.rect.y += self.speed_y

        # Check if the player hit anything during Y-movement
        hit_list = pygame.sprite.spritecollide(self, self.collide_list, False)
        for hits in hit_list:
            if self.speed_y > 0:
                self.rect.bottom = hits.rect.top
            else:
                self.rect.top = hits.rect.bottom

# Create a wall class
class Wall(pygame.sprite.Sprite):
    # Initialize the wall class
    def __init__(self, x, y, w, h, color = black, id=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.id = id
