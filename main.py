import pygame
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
                levels.level_x += 40
            levels.level_x = 0
            levels.level_y += 40


    # Starting a new game
    def new(self):
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
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
        self.players.update()
        self.gui.update()

        hits =  pygame.sprite.spritecollide(self.player, self.walls, False)

        if hits:
            print(hits)

    # Game loop - Rendering/Drawing
    def draw(self):
        self.game_display.fill(dark_gray)

        self.players.draw(self.game_display)
        self.walls.draw(self.game_display)
        self.gui.draw(self.game_display)

        pygame.mouse.set_visible(0)
        pygame.display.update()
        pygame.display.set_caption(title + " running at " + str(int(self.clock.get_fps())) + " frames per second")

game = Game()

while game.running:
    game.new()

pygame.quit()
quit()  