import pygame
import random
import levels
from sprites import *
from settings import *

# Create game class
class Game:
    # Initialize the game class
    def __init__(self):
        pygame.init()

        self.game_display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

    # Creating the level
    def create_level(self, level):
        for rows in level:
            for cols in rows:
                if cols == 1:
                    w = Wall(levels.level_x, levels.level_y, 40, 40)
                    self.walls.add(w)
                elif cols == 2:
                    w = Wall(levels.level_x, levels.level_y, 40, 40, color=white, id="1")
                    self.exits.add(w)
                levels.level_x += 40
            levels.level_x = 0
            levels.level_y += 40


    # Starting a new game
    def new(self):
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.gui = pygame.sprite.Group()

        self.create_level(levels.level_1)
        self.player = Player()
        self.pointer = Pointer()

        self.gui.add(self.pointer)
        self.players.add(self.player)

        self.run()

    # Game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # Game loop - Events
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    # Game loop - Update
    def update(self):

        hits_walls =  pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_circle)

        if hits_walls:

            print("collision {0}".format(random.randint(0, 10)))

            if self.player.vel.y < 0:
                self.player.pos.y -= self.player.vel.y + 0.5 * self.player.acc.y
                self.player.vel.y = 0
            elif self.player.vel.y > 0:
                self.player.pos.y -= self.player.vel.y + 0.5 * self.player.acc.y
                self.player.vel.y = 0

            if self.player.vel.x < 0:
                self.player.pos.x -= self.player.vel.x + 0.5 * self.player.acc.x
                self.player.vel.x = 0
            elif self.player.vel.x > 0:
                self.player.pos.x -= self.player.vel.x + 0.5 * self.player.acc.x
                self.player.vel.x = 0

        self.players.update()
        self.gui.update()


    # Game loop - Rendering/Drawing
    def draw(self):
        self.game_display.fill(dark_gray)

        self.exits.draw(self.game_display)
        self.players.draw(self.game_display)
        self.walls.draw(self.game_display)
        self.gui.draw(self.game_display)
        pygame.draw.circle(self.game_display, green, self.player.rect.center, self.player.radius)

        pygame.mouse.set_visible(0)
        pygame.display.update()
        pygame.display.set_caption(title + " running at " + str(int(self.clock.get_fps())) + " frames per second")

game = Game()

while game.running:
    game.new()

pygame.quit()
quit()
