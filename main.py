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

        self.create_level(levels.level_1)
        self.player = Player(self.walls)

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
        self.players.update()

    # Game loop - Rendering/Drawing
    def draw(self):
        self.game_display.fill(dark_gray)

        self.walls.draw(self.game_display)
        self.players.draw(self.game_display)

        # Makes hitbox green
        pygame.draw.rect(self.game_display, green, self.player.rect)

        pygame.display.update()
        pygame.display.set_caption(title + " running at " + str(int(self.clock.get_fps())) + " frames per second")

game = Game()

while game.running:
    game.new()

pygame.quit()
quit()
