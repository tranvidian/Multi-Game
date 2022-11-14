import sprites
import pygame
from game import Game

# ? Specifically made to be copy and paste code for making new games
class Subgame(Game): # testing inheritance of shorter redundant code

    def __init__(self):

        self.BACKGROUND = pygame.Surface((Game.GAME_SIZE[0], Game.GAME_SIZE[1])) # converted space available into cell space
        self.BACKGROUND.fill(pygame.Color(59, 83, 12))
        #this is a rectangle object of the surface background
        self.background_rect = self.BACKGROUND.get_rect(center = (Game.GAME_POS_MID[0], Game.GAME_POS_MID[1]))

        # ! ----------------
        #setup the scene with rectangles (backgrounds and interactive object)
        # ! ----------------

        self.player       = sprites.Player(self.background_rect)
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        self.enemy        = sprites.NonPlayer(self.background_rect)
        self.enemy_group  = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def reset(self):
        pygame.sprite.Sprite.kill()
        self.player_group.add(self.player)
        self.enemy_group.add(self.enemy)

    def start_loop(self, clock, clock_speed):
        user_exit = False
            # ! ----------------
            #setup the game logic
            # ! ----------------



        while not user_exit:
            self.blit_main() #blit main is highly important to making new games

            self.SCREEN.blit(self.BACKGROUND, self.background_rect)
            self.events()
            self.player_group.draw(self.SCREEN)
            self.player.update()
            self.enemy_group.draw(self.SCREEN)
            self.enemy_group.update()
            # ! ----------------
            #setup the game logic
            # ! ----------------
            pygame.display.update()
            clock.tick(clock_speed)

class Snake(Game):

    def __init__(self):


        # ! ----------------
        #setup the scene with rectangles (backgrounds and interactive object)
        #have all class variables ready
        # ! ----------------
        # TODO: Screen size is not the same for all computers, change it
        # TODO: to ensure it will correctly popup in all screen types
        #formualically what the size of the cell should be

        self.cell_side_size  = self.set_screen(Game.GAME_SIZE, cell_side_num = 20)
        cell_x_count         = int(Game.GAME_SIZE[0] / self.cell_side_size)
        cell_y_count         = int(Game.GAME_SIZE[1]/ self.cell_side_size)

        #Remaking the background into cell size
        self.background      = pygame.Surface((self.cell_side_size * cell_x_count , self.cell_side_size* cell_y_count)) # converted space available into cell space
        self.background.fill(pygame.Color(59, 83, 164))
        #this is a rectangle object of the surface background
        self.background_rect = self.background.get_rect(center = (Game.GAME_POS_MID[0], Game.GAME_POS_MID[1]))

        #position player position to where the rectangle is at
        self.player          = sprites.SnakeSprite(self.cell_side_size, self.background_rect)
        self.fruit           = sprites.Fruit(self.cell_side_size, self.background_rect)

        self.fruit_group     = pygame.sprite.Group()
        self.player_group    = pygame.sprite.GroupSingle()

        self.snake_body      = sprites.SnakeBodySetup(self.cell_side_size, self.player) #does not inherit pygame.sprites
        self.body_group      = pygame.sprite.Group()
        for body in self.snake_body.snake_body:
            self.body_group.add(body)

        self.player_group.add(self.player)
        self.fruit_group.add(self.fruit)
        # ? ------------------------------------------------
        # Counters (maybe useful for things)
        self.apple_score = 0

    def set_screen(self, GAME_SIZE, cell_side_num = 20):
        if GAME_SIZE[0] > GAME_SIZE[1]:
            get_cell_side = (GAME_SIZE[1] / cell_side_num) / 2
        else:
            get_cell_side = (GAME_SIZE[0] / cell_side_num) / 2
        return get_cell_side

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def more_apples(self, how_many):
        for i in range(how_many):
            self.fruit_group.add(sprites.Fruit(self.cell_side_size, self.background_rect))


    def collision(self):
        collide_player_fruit = pygame.sprite.groupcollide(self.player_group, self.fruit_group, False, True)
        collide_player_body = pygame.sprite.groupcollide(self.player_group, self.body_group, False, False)

        if len(collide_player_fruit) == 1:
            self.apple_score += 1
            if self.apple_score % 5 == 0:
                self.more_apples(5)
            else:
                self.more_apples(1)

            self.body_group.add(self.snake_body.add_body(self.player.pos)) #inside parameters returns the new body from the add # ! (two layers)

        if len(collide_player_body) == 1:
            return True
        return False

    def start_loop(self,clock,clock_speed):
        self.user_exit = False

        while not self.user_exit:

            self.blit_main()
            self.events()

            self.SCREEN.blit(self.background, self.background_rect)

            self.player_group.draw(self.SCREEN)
            self.body_group.draw(self.SCREEN)
            self.fruit_group.draw(self.SCREEN)

            self.snake_body.move_bodies(self.player.pos) #bodies moves first then
            self.user_exit = self.player.update() # snake head moves last
            self.user_exit = self.collision()

            pygame.display.update()

            # ! tick is 25
            clock.tick(25)
        return self.apple_score

class JumpMan(Game): # testing inheritance of shorter redundant code

    def __init__(self):

        self.main_screen_rect = Game.TRUE_SCREEN.get_rect(center = Game.GAME_POS_MID)
        self.ground           = pygame.image.load('graphics/ground.png').convert_alpha()
        self.sky              = pygame.image.load('graphics/Sky.png').convert_alpha()

        #resizing scale(Surface, (new size)) new size is new width, hight
        ground_size           = (Game.TRUE_SCREEN.get_size()[0],
                            self.ground.get_size()[1])
        self.ground           = pygame.transform.scale(self.ground, ground_size)
        ground_x              = Game.GAME_POS_MID[0]
        ground_y              = Game.GAME_POS_MID[1] + (Game.GAME_SIZE[1] / 2)
        self.ground_rect      = self.ground.get_rect(midbottom = (ground_x, ground_y))

        background_size       = (Game.TRUE_SCREEN.get_size()[0],
                            Game.TRUE_SCREEN.get_size()[1] - self.ground.get_size()[1])

        self.sky              = pygame.transform.scale(self.sky, background_size)
        sky_x                 = self.main_screen_rect.x
        sky_y                 = self.main_screen_rect.y
        self.sky_rect         = self.sky.get_rect(topleft = (sky_x, sky_y))

        # ! Potential Revision
        # ? If make one background picture it make sense to use that as an arguement
        # ? But for mutliple backgrounds (Ground and Sky) its complicated to get X,Y Coords for these Sprites
        self.player       = sprites.Jump(self.ground_rect)
        self.player.set_boundary(self.main_screen_rect)
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        self.enemy        = sprites.NoJumps(self.ground_rect, "Fly")
        self.enemy.set_boundary(self.main_screen_rect)
        self.enemy.set_pos_bottlef(self.ground_rect.topright)
        self.enemy_group  = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)
        #need a list to refer back to spawning new sprites
        self.enemy_list   = [self.enemy]

        # ? Need a new Screen/Rectangle to cover the rectangles
        # size is an approximation lazy
        self.cover_up       = pygame.Surface((Game.GAME_SIZE[0]/2,Game.GAME_SIZE[1]))
        self.cover_up.fill(pygame.Color(192, 192, 192))
        self.cover_up_rect  = self.cover_up.get_rect(midleft = (self.sky_rect.right,Game.GAME_POS_MID[1]))
        self.cover_up_rect2 = self.cover_up.get_rect(midright = (self.sky_rect.left,Game.GAME_POS_MID[1]))

        self.score = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def collision_check(self): # ? Used for user_exit
        collide_player_enemy = pygame.sprite.groupcollide(self.player_group, self.enemy_group, False, False)
        if len(collide_player_enemy) >= 1:
            return True
        return False

    def spawn_new(self):
        for enemy in self.enemy_list:
            pl = self.player.rect
            en = enemy.rect
            if pl.x >= en.x and pl.x <= en.x + en.width:
                # new enemy instance for our groups
                enemy = sprites.NoJumps(self.ground_rect)
                enemy.set_boundary(self.main_screen_rect)
                enemy.set_pos_bottlef(self.ground_rect.topright)

                self.enemy_group.add(enemy)
                self.enemy_list.append(enemy)
                self.enemy_list.pop(0)
                self.score += 10


    def start_loop(self, clock, clock_speed):
        user_exit = False
        while not user_exit:
            user_exit = self.collision_check()
            self.spawn_new()
            self.blit_main() #blit main is highly important to making new games

            self.SCREEN.blit(self.sky, self.sky_rect)
            self.SCREEN.blit(self.ground, self.ground_rect)
            self.events()

            self.player_group.draw(self.SCREEN)
            self.player.update()
            self.enemy_group.draw(self.SCREEN)
            self.enemy_group.update()

            # ! Cover ups
            self.SCREEN.blit(self.cover_up, self.cover_up_rect2) #Left Side
            self.SCREEN.blit(self.cover_up, self.cover_up_rect) #Right Side


            pygame.display.update()
            clock.tick(clock_speed)
        Game.games_total_score += self.score
        return self.score


