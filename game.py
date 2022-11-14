
import pygame
import pygame.tests
import sprites
from sys import exit


class Game(pygame.sprite.Sprite):
    '''

The Game Class is the Parent Class for other subgames we will make

    Parameters
    ----------
    SCREEN : Surface
        The very first Surface that setup the window (cannot modify, only read).
        The first initial screen
    BACKGROUND : Surface
        2nd Surface that we are given to place in our Game/Subgame class.
        Its the overall background for all games (it covers the whole screen).
        Our game screen (2nd surface) also called stage screen (the red cloth that comes down for in person stages)
    GAME_SIZE : List [int, int]
        Size for our game/subgame Surface.
        It is for making a new surface for another child class of parent Game.
    GAME_POS_MID : List [int, int]
        Coordinates from SCREEN but only the center coordinates of SCREEN.
        Position of our new screen to make, but as the center coordinate of the surface's rectangle.
    total_score : int
        Something we can track with for score on disk/file

    Class Attributes
    ----------
    ==== Including Parameter ====
        Same as written in Parameters (all parameters are one-to-one for class attributes)
        i.e. SCREEN Class Attribute is set by SCREEN parameter

    TRUE_SCREEN : Surface
        Very basic Surface/screen for our new game/subgame class
        (so that we can see where we putting).
        DEBUGGER TOOL

    Class Instance
    ----------
    true_screen : Surface
        Used to set TRUE_SCREEN constant/Class Attribute
    true_screen_rec : Rectangle -> Surface
        Used to set TRUE_SCREEN constant/Class Attribute
    '''

    SCREEN       = None
    BACKGROUND   = None
    GAME_SIZE    = None
    GAME_POS_MID = None
    TRUE_SCREEN  = None
    total_score  = None
    games_total_score   = None
    def __init__(self, SCREEN, BACKGROUND, GAME_SIZE, GAME_POS_MID, total_score = None):
        '''
        This will initializes all the class attributes to the parameters

        this is also where the setup of rectangles/surfaces, sprites,
        and detection collisions will take place.
        '''
        super().__init__()
        Game.SCREEN       = SCREEN
        Game.GAME_SIZE    = GAME_SIZE
        Game.BACKGROUND   = BACKGROUND
        Game.GAME_POS_MID = GAME_POS_MID
        Game.total_score  = total_score #total score given by file
        Game.games_total_score   = 0
        # ! ----------------
        #setup the scene with rectangles (backgrounds and interactive object)
        # ! ----------------

        self.true_screen     = pygame.Surface((GAME_SIZE[0],GAME_SIZE[1]))
        self.true_screen.fill(pygame.Color(255, 255, 0))
        self.true_screen_rec = self.true_screen.get_rect(midbottom = (GAME_POS_MID[0], GAME_POS_MID[1]))
        Game.TRUE_SCREEN     = self.true_screen

        self.player          = sprites.Player(self.true_screen_rec)
        self.player_group    = pygame.sprite.GroupSingle()

        self.player_group.add(self.player)

        self.score = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# ! ---------------------------------------
#? Dedicated to be called on classes that inherited this Game class
    def surface_total_score(self):
        if Game.total_score != None:
            font = pygame.font.Font(None,50)
            if Game.total_score > Game.games_total_score:
                surf_total_score = font.render("Score:{}".format(Game.total_score), True, "Black")
                Game.total_score = Game.games_total_score
            else:
                surf_total_score = font.render("Score:{}".format(Game.games_total_score), True, "Black")
        else:
            surf_total_score = None
        return surf_total_score

    def blit_main(self):
        Game.SCREEN.blit(Game.BACKGROUND, (0,0))
        Game.SCREEN.blit(Game.surface_total_score(self), (0,0))
        true_screen_position = Game.TRUE_SCREEN.get_rect(center = (Game.GAME_POS_MID[0], Game.GAME_POS_MID[1]))
        Game.SCREEN.blit(Game.TRUE_SCREEN, true_screen_position)
# ! ---------------------------------------

    def start_loop(self,clock,clock_speed):
        '''Function that starts the game loop

            Parameters
            ----------
            clock : pygame.time.Clock()
                Main clock that all the games share and start with
            clock_speed : int
                optional- if wanted, pick the ame clock speed as before

            Raises
            ------


            Returns
            -------

            Setup
            -------
            Must always call blit_main() to put basic background (score, 2nd background, true screen)
            The true_screen is a debugger tool made to ensure that you are on the screen position needed.
        '''
        user_exit = False
        while not user_exit:
            self.blit_main()

            self.events()

            self.player_group.draw(self.SCREEN)
            self.player.update()
            # ! ----------------
            #setup the game logic
            # ! ----------------
            pygame.display.update()
            clock.tick(clock_speed)
        Game.games_total_score += self.score
        return self.score




