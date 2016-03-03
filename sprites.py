from settings import *
from resources import *
import pygame
import math
vec = pygame.math.Vector2

# Creating a player class
class Player(pygame.sprite.Sprite):
    # Initialize the player class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_standing.convert_alpha()
        self.image_original = self.image.copy()


        self.rect = self.image.get_rect(center = (display_width/2, display_height/2))
        self.radius = 25
        self.old_rect = self.rect.copy()

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.moving_up = False
        self.moving_left = False
        self.moving_down = False
        self.moving_right = False

        self.up_lock = False
        self.left_lock = False
        self.down_lock = False
        self.right_lock = False

        self.pos = vec(display_width/2, display_height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.walk_counter = 0
        self.walk_number = 0

    # Update the player class
    def update(self):
        self.old_rect = self.rect.copy()
        self.acc = vec(0, 0)
        self.pos_change = vec(0, 0)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Event handling
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.up_lock:
            self.moving_up = True
            self.down_lock = True
        else:
            self.moving_up = False
            self.down_lock = False

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.left_lock:
            self.moving_left = True
            self.right_lock = True
        else:
            self.moving_left = False
            self.right_lock = False

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.down_lock:
            self.moving_down = True
            self.up_lock = True
        else:
            self.moving_down = False
            self.up_lock = False

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.right_lock:
            self.moving_right = True
            self.left_lock = True
        else:
            self.moving_right = False
            self.left_lock = False

        # Make player accelerate
        if self.moving_up:
            self.acc.y = -player_acc
            #self.pos.y -= 5
        if self.moving_left:
            self.acc.x = -player_acc
            #self.pos.x -= 5
        if self.moving_down:
            self.acc.y = player_acc
            #self.pos.y += 5
        if self.moving_right:
            self.acc.x = player_acc
            #self.pos.x += 5

        # Make diagonal movement as fast as vertical/horizontal
        if self.moving_up and self.moving_left or self.moving_up and self.moving_right:
            self.acc *= 0.707
        if self.moving_down and self.moving_left or self.moving_down and self.moving_right:
            self.acc *= 0.707

        # Apply friction
        self.acc += self.vel * player_friction

        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Walking animations
        if self.moving_up or self.moving_left or self.moving_down or self.moving_right:

            self.walk_counter += 1

            if self.walk_counter >= 5:

                self.walk_counter = 0
                self.image_original = player_walk_list[self.walk_number]
                self.walk_number += 1

                if self.walk_number >= 11:
                    self.walk_number = 0
        else:
            self.image_original = player_standing.convert_alpha()

        # Make player look at mouse

        self.angle = math.atan2(self.mouse_x - self.rect.center[0], self.mouse_y - self.rect.center[1])
        self.angle_degrees = (180 * self.angle / math.pi) + 180

        self.image = pygame.transform.rotate(self.image_original, int(self.angle_degrees))
        self.rect = self.image.get_rect(center=self.old_rect.center)

        # Make player change position
        self.rect.center = self.pos.x, self.pos.y

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

# Create mouse pointer class
class Pointer(pygame.sprite.Sprite):
    # Initialize the pointer class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mouse_pointer
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
