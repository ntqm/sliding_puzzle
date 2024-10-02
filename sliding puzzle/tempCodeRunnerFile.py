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