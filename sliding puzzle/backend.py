
import pygame 
from pygame import mixer

mixer.init()
pygame.font.init()

# game colors(constants)
WHITE = (249, 249, 249)
NAVY = (32, 42, 68)
BLUE = (176, 224, 230)
GREY = (219, 220, 220)
BACKGROUND = NAVY

# game menu
print("Welcome to Sliding Puzzle Game!")
#get information of game mode to modify the screen size, game size and high score
x =  int(input("Please choose the mode to start playing (1-3):\n 1 - Easy\n 2 - Medium\n 3 - Hard\n"))
game_mode = ("Easy", "Medium", "Hard")
game_size = (3,4,5)
while x < 1 or x > 3:
    print("Please enter a value between 1 and 3")
    x =  input("Please choose the mode to start playing (1-3):\n 1 - Easy\n 2 - Medium\n 3 - Hard\n")
game_size = game_size[x - 1]
game_mode  = "Mode: " + game_mode[x - 1]

# game settings(constants)
TILESIZE = 128
WIDTH = TILESIZE * game_size + 300
HEIGHT = TILESIZE * game_size 
FONT = "Spacia"

# game sounds
start_sound = mixer.Sound("sounds\game-start.wav")
reset_sound = mixer.Sound("sounds\game reset.wav")
click_sound = mixer.Sound("sounds\click.wav")
switch_sound = mixer.Sound("sounds\switch.wav")


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        #Simple base class for visible game objects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        #draw tile if tile is not empty
        if self.text != "empty": 
            self.font = pygame.font.SysFont(FONT, 50)
            font_surface = self.font.render(self.text, True, BLUE)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BACKGROUND)

    #draw square size
    def update(self):
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    # moving functions
    def right(self):
        return self.rect.x + TILESIZE < game_size * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < game_size * TILESIZE


class ScreenText:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont(FONT, 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.color, self.text_color = color, text_color
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(FONT, 30)
        text = font.render(self.text, True, self.text_color)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height