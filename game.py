import pygame

# initialize pygame
pygame.init()

# creating a game display
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("")

# colors
white = (255, 255, 255, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 100, 0)
magenta = (255, 0, 255)
gray = (150, 150, 150)
black = (0, 0, 0, 50)

# FPS variables
FPS = 60
clock = pygame.time.Clock()

# pixels per frame variable that doesn't change
pixels_per_frame = 5

# font variables
font_file = "8-Bit-Madness.ttf"
smallfont = pygame.font.Font(font_file, 25)
medfont = pygame.font.Font(font_file, 50)
largefont = pygame.font.Font(font_file, 75)
hugefont = pygame.font.Font(font_file, 150)

# UI variables
padding = 20
border_width = 5

border_color = white
background_color = black

active_text_color = orange
inactive_text_color = white


# item classes
class Weapon(object):

    name = ""
    worth = 0
    weight = 0
    dmg = 0

    def __init__(self, name, worth, weight, dmg):
        self.name = name
        self.worth = worth
        self.weight = weight
        self.dmg = dmg


# item variables
sword = Weapon("sword", 50, 40, 10)
spear = Weapon("spear", 75, 50, 12)
inventory_list = (sword, spear)


# simple game quit function
def game_quit():
    pygame.quit()
    quit()


# simple collision detecting function
def collide_detect(x1, y1, w1, h1, x2, y2, w2, h2):
    if x2 < x1 < x2+w2 or x2 < x1+w1 < x2+w2:
        if y2 < y1 < y2+h2 or y2 < y1+h1 < y2+h2:
            return True
    return False


# make text object
def text_object(msg, color, size):

    if size == "small":
        text_surface = smallfont.render(msg, False, color)
    elif size == "medium":
        text_surface = medfont.render(msg, False, color)
    elif size == "large":
        text_surface = largefont.render(msg, False, color)
    elif size == "huge":
        text_surface = hugefont.render(msg, False, color)

    return text_surface, text_surface.get_rect()


# function that renders the text object + returns its rect
def render_text(msg, color, y_displace=0, x_displace=0,  size="small"):
    text_surface, text_rect = text_object(msg, color, size)
    text_rect.center = (display_width / 2) + x_displace, (display_height / 2) + y_displace
    game_display.blit(text_surface, text_rect)
    return text_rect


# function that creates a text box
def text_box(box_padding, box_border_width, top_rect, bottom_rect):

    top_to_bottom_length = bottom_rect[1] - top_rect[1]

    pygame.draw.rect(game_display, border_color, (top_rect[0]-(box_padding+box_border_width),
                                                  top_rect[1]-(box_padding+box_border_width),
                                                  top_rect[2]+(box_padding+box_border_width)*2,
                                                  top_rect[3] + (top_to_bottom_length + (padding+border_width)*2)))
    pygame.draw.rect(game_display, background_color, (top_rect[0]-box_padding,
                                                      top_rect[1]-box_padding,
                                                      top_rect[2]+box_padding*2,
                                                      top_rect[3] + (top_to_bottom_length + (padding*2))))


# pause function
def pause():

    running = True

    selected = "menu"

    paused_rect = render_text("PAUSED", black, y_displace=-175, size="large")
    quit_rect = render_text("QUIT", black, y_displace=25, size="medium")

    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "menu"
                if event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "menu":
                        menu_loop()
                    if selected == "quit":
                        game_quit()
                if event.key == pygame.K_ESCAPE:
                    running = False

        # draw box behind text
        text_box(padding, border_width, paused_rect, quit_rect)

        # text rendering
        render_text("PAUSED", inactive_text_color, y_displace=-175, size="large")

        if selected == "menu":
            render_text("MAIN MENU", active_text_color, y_displace=-50, size="medium")
        else:
            render_text("MAIN MENU", inactive_text_color, y_displace=-50, size="medium")

        if selected == "quit":
            render_text("QUIT", active_text_color, y_displace=25, size="medium")
        else:
            render_text("QUIT", inactive_text_color, y_displace=25, size="medium")

        # update display
        pygame.display.update()
        clock.tick(FPS/2)


# inventory screen function
def inventory_screen():

    running = True
    y_displace = 0

    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    running = False

        # text rendering
        for render_inventory in inventory_list:
            render_text(render_inventory.name, inactive_text_color, y_displace=y_displace, size="medium")
            y_displace += 25

        # update display
        pygame.display.update()
        clock.tick(FPS/2)


def menu_loop():

    running = True

    selected = "play"

    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "play"
                if event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "play":
                        game_loop()
                    if selected == "quit":
                        game_quit()

        # rendering
        game_display.fill(background_color)

        render_text("TITLE", inactive_text_color, y_displace=-175, size="huge")

        if selected == "play":
            render_text("PLAY", active_text_color, y_displace=-50, size="large")
        else:
            render_text("PLAY", inactive_text_color, y_displace=-50, size="large")

        if selected == "quit":
            render_text("QUIT", active_text_color, y_displace=25, size="large")
        else:
            render_text("QUIT", inactive_text_color, y_displace=25, size="large")

        pygame.display.update()
        clock.tick(FPS/2)


# main game loop
def game_loop():

    running = True

    # player variables
    player_x = display_width/2
    player_y = display_height/2

    # speed variable that may change depending on direction of movement
    speed = pixels_per_frame

    moving_up = False
    moving_left = False
    moving_down = False
    moving_right = False

    while running:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_DOWN:
                    moving_down = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_ESCAPE:
                    moving_up = False
                    moving_left = False
                    moving_down = False
                    moving_right = False
                    pause()
                if event.key == pygame.K_i:
                    moving_up = False
                    moving_left = False
                    moving_down = False
                    moving_right = False
                    inventory_screen()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    moving_up = False
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_DOWN:
                    moving_down = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False

        # make diogonal speed equal to horizontal/vertical speed
        if (moving_up and moving_left) or (moving_up and moving_right):
            speed = pixels_per_frame * 0.707
        if (moving_down and moving_left) or (moving_down and moving_right):
            speed = pixels_per_frame * 0.707

        # player movement
        if moving_up:
            player_y -= speed
        if moving_left:
            player_x -= speed
        if moving_down:
            player_y += speed
        if moving_right:
            player_x += speed

        # collision detection
        if collide_detect(player_x, player_y, 20, 20, 100, 100, 50, 50):
            if moving_up:
                moving_up = False
                player_y += 5

            if moving_left:
                moving_left = False
                player_x += 5
            if moving_down:
                moving_down = False
                player_y -= 5
            if moving_right:
                moving_right = False
                player_x -= 5

        # rendering
        game_display.fill(gray)

        pygame.draw.rect(game_display, black, (player_x, player_y, 20, 20))

        pygame.draw.rect(game_display, black, (100, 100, 50, 50))

        pygame.display.update()
        clock.tick(FPS)

menu_loop()

game_quit()
