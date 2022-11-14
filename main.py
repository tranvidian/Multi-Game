from random import random
import pygame
import subgame
from sys import exit # ? Important for our application to close
import json # ? for saving highscore


pygame.init()

MONITOR_SIZE  = [pygame.display.Info().current_w, pygame.display.Info().current_h - 100]
GAME_SIZE     = [int(MONITOR_SIZE[0] / 2), int( (2/3)*MONITOR_SIZE[1])]
GAME_POS_MID  = [int(MONITOR_SIZE[0] / 2), int(MONITOR_SIZE[1] / 2)]
#screen        = pygame.display.set_mode((800,400))
#screen        = pygame.display.set_mode((game_screen[0], game_screen[1]))
SCREEN        = pygame.display.set_mode((MONITOR_SIZE[0], MONITOR_SIZE[1]))
bak_grnd      = pygame.Surface((MONITOR_SIZE[0], MONITOR_SIZE[1]))
bak_grnd.fill(pygame.Color(192, 192, 192))
BACKGROUND    = bak_grnd

pygame.display.set_caption("Vidian Game")
clock_main    = pygame.time.Clock()
game_active   = True
main_menu     = True

# ! ---------------------------------------
data_highscore = 0 # ! Kinda want to display highscore on a board using dict {name: score}
try:
    with open("data.txt") as file_score:
        data_highscore = json.load(file_score)
except:
    pass
# ! ---------------------------------------
font          = pygame.font.Font(None,50)
score         = 0
score_mess    = "Score:{}".format(data_highscore)
total_score   = font.render(score_mess, True, "Black")

initialize_all_game = subgame.Game(SCREEN, BACKGROUND, GAME_SIZE, GAME_POS_MID, data_highscore)
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #close our screen variable when one event (x button) in list
            pygame.quit()
            #from sys import (closes the loop code)
            exit()

game_list = [subgame.JumpMan(),subgame.Snake()]

def subgames():
# ! Switching back into a game is hard,
# ! so we have to reinitialize the class to restart
    while True:
        #calling this class will initiate the
        #game loop (loop of code that will play the game)
        random_game = int(random()*(len(game_list))) # 0 < x < size |or| 0 < x <= last index
        game_list[random_game].__init__()
        game_list[random_game].start_loop(clock_main, 60)

def subgame_test():
    # retesting functionality of instance data
    # also used to test singular games if needed
    random_game = 0 # 0 < x < size |or| 0 < x <= last index
    while random_game < 1:
        game_list[0].__init__()
        game_list[0].start_loop(clock_main, 60)
        data_highscore = subgame.Game.total_score
        random_game+=1
    total_score = font.render("Score:{}".format(data_highscore), True, "Black")
# ! fix total score and finish implementing total scores to subgames
while True:

    events() #just in cases

    SCREEN.blit(BACKGROUND, (0,0))
    SCREEN.blit(total_score,(0,0))
    if game_active:
        subgames()
        game_active = False

        #break

    elif not game_active and main_menu:
        pass
    pygame.display.update()
    clock_main.tick(60)
with open("data.txt", "w") as file_score:
    json.dump(data_highscore, file_score)
print("------------------------------------------------------------------------")
print("Credit for making lessons on making pygames https://youtu.be/AY9MnQ4x3zk")
print("https://github.com/clear-code-projects/UltimatePygameIntro")
print("------------------------------------------------------------------------")
