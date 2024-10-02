import pygame
import random
import time
from backend import *


class SlidingPuzzle:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sliding Puzzle")
        self.clock = pygame.time.Clock()
        self.prev_choice = ""
        self.start_shuffle = False
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.shuffle_time = 0
        self.high_score_easy = float(self.get_high_scores()[0])
        self.high_score_medium = float(self.get_high_scores()[1])
        self.high_score_hard = float(self.get_high_scores()[2])
        
    #open high score file and get information
    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    #save the new high score to file
    def save_score(self):
        with open("high_score.txt", "w") as file:
            #write new high score to file
            file.write(str("%.3f\n" % self.high_score_easy))
            file.write(str("%.3f\n" % self.high_score_medium))
            file.write(str("%.3f" % self.high_score_hard))

    #create game board according to game mode
    def create_board(self):
        grid = [[x + y * game_size for x in range(1, game_size + 1)] for y in range(game_size)]
        grid[-1][-1] = 0
        return grid

    #shuffle the tiles in the game board randomly
    def shuffle(self):
        # find the empty tile and add the possible move of it to the list
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.prev_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.prev_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.prev_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.prev_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        # swap empty tiles with texted tiles randomly
        choice = random.choice(possible_moves)
        self.prev_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]                                                                       
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]                                                                     
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]                                                                      
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                                                                    

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def draw_grid(self):
        for row in range(-1, game_size * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, GREY, (row, 0), (row, game_size * TILESIZE))
        for col in range(-1, game_size * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, GREY, (0, col), (game_size * TILESIZE, col))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_board()
        self.tiles_grid_completed = self.create_board()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        # generate new buttons and put them in the buttons list
        self.buttons_list = []
        self.buttons_list.append(Button(TILESIZE * game_size + 50, 100, 200, 50, "Shuffle", WHITE, BLUE))
        self.buttons_list.append(Button(TILESIZE * game_size + 50, 170, 200, 50, "Reset", WHITE, BLUE))
        self.draw_tiles()

    def run(self):
        self.playing = True
        start_sound.play()
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    #save information during playing game
    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                # take different high score from different game mode
                if x == 1:
                    if self.high_score_easy > 0:
                        self.high_score_easy = self.elapsed_time if self.elapsed_time < self.high_score_easy else self.high_score_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif x == 2:
                    if self.high_score_medium > 0:
                        self.high_score_medium = self.elapsed_time if self.elapsed_time < self.high_score_medium else self.high_score_medium
                    else:
                        self.high_score_medium = self.elapsed_time
                elif x == 3:
                    if self.high_score_hard > 0:
                        self.high_score_hard = self.elapsed_time if self.elapsed_time < self.high_score_hard else self.high_score_hard
                    else:
                        self.high_score_hard = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer


        if self.start_shuffle:
            switch_sound.play()
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            #start timer after shuffling tiles
            if self.shuffle_time > 111:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    #draw grid, button and text on the screen
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        #modify the text on the screen according to the game size
        ScreenText(TILESIZE * game_size + 80, 250, game_mode).draw(self.screen)
        # display different high scores for different game mode
        if x == 1:
            ScreenText(TILESIZE * game_size + 60, 300, "High Score: %.3f" % (self.high_score_easy if self.high_score_easy > 0 else 0)).draw(self.screen)
        elif x == 2:
            ScreenText(TILESIZE * game_size + 60, 300, "High Score: %.3f" % (self.high_score_medium if self.high_score_medium > 0 else 0)).draw(self.screen)
        elif x == 3:
            ScreenText(TILESIZE * game_size + 60, 300, "High Score: %.3f" % (self.high_score_hard if self.high_score_hard > 0 else 0)).draw(self.screen)
        ScreenText(TILESIZE * game_size + 80, 35, "Time: %.3f" % self.elapsed_time).draw(self.screen)
        #Update the full display Surface to the screen
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            #click tiles in the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                # return the movement of the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            switch_sound.play()
                            #swap empty tiles with texted tiles
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                #click button
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            click_sound.play()
                        if button.text == "Reset":
                            self.new()
                            reset_sound.play()

game = SlidingPuzzle()
while True:
    game.new()
    game.run()