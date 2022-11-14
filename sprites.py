import pygame
from pygame.math import Vector2
import random

'''
# ? Recall that these classes only contains sprites information
# ? not displaying on screen

# ! Every sprite class must have an instance attribute named "image"
# ? structure for loading player info first then as variable self.image based on
# ? pygame.sprite.GroupSingle() or pygame.sprite.Group()
'''
class Player(pygame.sprite.Sprite): # ? These are used for inheritance and copy and paste for new type of objects
    '''

    The Player Class is the basic structure for other classes

    Parameters
    ----------
    background_rect: Rectangle
        This is what subgame gives as the main source of position and placement

    Important Class Instance
    ----------
    self.player: Rectangle/image.load
        Used as the primary player for user inputs and to setup for self.image

    self.image: Rectangle/image.load
        for subgame/game class to use pygame.sprite.GroupSingle() or pygame.sprite.Group()
        to draw with.

    '''
    def __init__(self, background_rect):
        super().__init__()

        #self.player = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.player  = pygame.Surface((50,50))
        self.player.fill(pygame.Color(44, 54, 182))
        #player image-----------------
        self.image   = self.player
        #-----------------------------
        self.x_pos   = background_rect.center[0]
        self.y_pos   = background_rect.center[1]
        self.pos     = Vector2(self.x_pos, self.y_pos)
        self.gravity = 0
        self.rect    = self.player.get_rect(midbottom = (self.x_pos, self.y_pos))

    def player_input(self):
        #logic input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

        elif keys[pygame.K_RIGHT]:
            self.rect.x  += 1

        elif keys[pygame.K_LEFT]:
            self.rect.x  -= 1

        elif keys[pygame.K_a]:
            self.kill()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y  += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        pass

    def update(self):#main function to use
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class NonPlayer(pygame.sprite.Sprite): # ? These are used for inheritance and copy and paste for new type of objects
    def __init__(self, background_rect):
        super().__init__()
        self.x_pos      = background_rect.center[0]
        self.y_pos      = background_rect.center[1]
        self.pos        = Vector2(self.x_pos, self.y_pos)
        #call for creating surface
        self.non_player = pygame.Surface((100,200))
        self.non_player.fill("Red")
        self.rect       = self.non_player.get_rect(midbottom = (self.x_pos, self.y_pos))
        self.image      = self.non_player

    def animation_state(self):
        pass

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class SnakeSprite(pygame.sprite.Sprite):

    def __init__(self, cell_size, background_rect):
        super().__init__()

        #max boundarys for x,y position
        self.bound = [
                    background_rect.x, #x min/top left pos at x
                    background_rect.x + background_rect.width, #x max
                    background_rect.y, #y min/top left pos at y
                    background_rect.y + background_rect.height] #y man

        #Snake/Player Head--------------------------------------------------------
        # ? structure for loading player info first then as variable self.image based on
        # ? pygame.sprite.GroupSingle() or pygame.sprite.Group()

        self.snake_size     = cell_size
        #self.player = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.snake_head     = pygame.Surface((cell_size, cell_size))
        self.snake_head.fill(pygame.Color(195, 32, 32))

        #player image------------------------
        self.image     = self.snake_head
        #------------------------------------

        #starting position of the snake
        self.x_pos          = background_rect.center[0]
        self.y_pos          = background_rect.center[1]
        self.pos            = Vector2(self.x_pos, self.y_pos) #true position of snake
        self.direction      = Vector2(1,0)
        #starts at positon (grabbing top left) in terms of cell_size (non-zero)
        # and coordinates of the background
        self.rect           = self.snake_head.get_rect(topleft = (self.pos.x, self.pos.y))
        #------------------------------------------------------------------------


    def player_input(self):
        #logic input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if self.direction != Vector2(-1,0):
                self.direction = Vector2(1,0)

        elif keys[pygame.K_a]:
            if self.direction != Vector2(1,0):
                self.direction = Vector2(-1,0)

        elif keys[pygame.K_s]:
            if self.direction != Vector2(0,-1):
                self.direction = Vector2(0,1)

        elif keys[pygame.K_w]:
            if self.direction != Vector2(0,1):
                self.direction = Vector2(0,-1)


        self.pos += (self.direction * self.snake_size)
        #This updates the position of the rectnagle of snake by adding self.pos
        self.rect = self.snake_head.get_rect(topleft = (self.pos.x, self.pos.y))

    def animation_state(self):
        pass

    # ! Snake stops moving once it is in!!!! out of bound
    def out_boundary(self):
        predict = self.pos + (self.direction * self.snake_size)
        #check if snake is out of boundary
        x_center = self.rect.center[0]
        y_center = self.rect.center[1]
        #x pos out of bound
        if x_center > self.bound[1] or x_center < self.bound[0]:
            return True
        elif y_center > self.bound[3] or y_center < self.bound[2]:
            return True

        return False

    def update(self):
        if not self.out_boundary():
            self.player_input()
            self.animation_state()
        else:
            #important to leave the game
            return True

class Fruit(pygame.sprite.Sprite):

    def __init__(self, cell_size, background_rect):
        super().__init__()

        self.WIDTH  = background_rect.width
        self.HEIGHT = background_rect.height

        self.bound  = [
                    background_rect.x, #x min/top left pos at x
                    background_rect.x + self.WIDTH, #x max
                    background_rect.y, #y min/top left pos at y
                    background_rect.y + self.HEIGHT] #y man

        # ? starts at screen position topleft then add randomized amount of space in cell_sized position
        self.x_pos  = self.bound[0] + cell_size*(int((random.random())*(self.WIDTH/cell_size)))
        self.y_pos  = self.bound[2] + cell_size*(int((random.random())*(self.HEIGHT/cell_size)))
        self.pos    = Vector2(self.x_pos, self.y_pos)

        #had to minus one for x size because collision was sized on edge for snake
        self.image  = pygame.Surface((cell_size - .5 , cell_size - .5))
        self.image.fill(pygame.Color(132, 15, 15))

        self.rect   = self.image.get_rect(topleft = (self.pos.x, self.pos.y))

    def randomize_pos(self):
        cell_size = self.cell_size
        self.x_pos  = self.bound[0] + cell_size*(int((random.random())*(self.WIDTH/cell_size)))
        self.y_pos  = self.bound[2] + cell_size*(int((random.random())*(self.HEIGHT/cell_size)))
        self.pos    = Vector2(self.x_pos, self.y_pos)

        self.rect   = self.image.get_rect(topleft = (self.pos.x, self.pos.y))

class SnakeBody(pygame.sprite.Sprite): # ? this is a node type class
    def __init__(self, cell_size, pos): # pos parameter is the rectangle coords of the player/snake head rectangle tuple(i think tuple)
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(pygame.Color(33, 223, 198))
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))


    def move(self, new_pos):
        self.rect = self.image.get_rect(topleft = (new_pos[0], new_pos[1]))

class SnakeBodySetup(): # ? We can call group single still with .add() method to add all nodes

    def __init__(self, cell_size, head):
        self.head = head
        self.head_pos = self.head.pos
        self.math_1 = Vector2(cell_size, 0)
        self.cell_size = cell_size

        # old but reliable way
        #self.snake_body = [
        #                    SnakeBody(cell_size, self.head_pos - self.math_1),
        #                    SnakeBody(cell_size, self.head_pos - (2 * self.math_1)),
        #                    SnakeBody(cell_size, self.head_pos - (3* self.math_1))
        #                    ]
        self.snake_body = []
        add_more = 3
        for i in range(1, 1 + add_more):
            self.snake_body.append(SnakeBody(cell_size, self.head_pos - (i* self.math_1)))


    def add_body(self, head_pos): # When moving the body we let it follow the other upper body in the list (in terms of index)
        new_body = SnakeBody(self.cell_size, self.snake_body[-1].rect.topleft)
        self.snake_body.append(new_body)
        return new_body # Needed to add into body group in snake game

    def move_bodies(self, head_pos):
        self.snake_body[-1].move(head_pos)
        self.snake_body.insert(0, self.snake_body[-1])
        self.snake_body = self.snake_body[:-1]

class Jump(pygame.sprite.Sprite): # ? These are used for inheritance and copy and paste for new type of objects

    def __init__(self, background_rect):
        super().__init__()
        self.bound         = [] #from different rectangle

        self.ground_rect   = background_rect

        self.player_walk_r = [
                                pygame.image.load('graphics/player/player_walk_1_right.png').convert_alpha(),
                                pygame.image.load('graphics/player/player_walk_2_right.png').convert_alpha()]
        self.player_walk_l = [
                                pygame.image.load('graphics/player/player_walk_1_left.png').convert_alpha(),
                                pygame.image.load('graphics/player/player_walk_2_left.png').convert_alpha()]

        self.walk_index    = 0.00
        self.walk_increase = 0.1

        self.player_jump   = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_stand  = pygame.image.load('graphics/player/player_stand.png').convert_alpha()

        #player image-----------------
        self.image         = self.player_stand
        #-----------------------------
        self.x_pos         = self.ground_rect.x
        self.y_pos         = self.ground_rect.y
        self.gravity       = 0
        self.velocity      = 3
        self.rect          = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

    def player_input(self):
        #logic input
        keys = pygame.key.get_pressed()
        new_image = self.player_stand

        #-----------------------------
        if self.walk_index + 0.10 >=  2:
            self.walk_index = 0.00
        #-----------------------------

        if (keys[pygame.K_SPACE] or keys[pygame.K_w])  and self.rect.bottom >= self.y_pos:
            self.gravity += -20

        elif keys[pygame.K_d] and self.rect.right < self.bound[1]:
            self.rect.x  += self.velocity
            self.walk_index += self.walk_increase
            new_image = self.player_walk_r[int(self.walk_index)]

        elif keys[pygame.K_a]  and self.rect.left > self.bound[0]:
            self.rect.x  -= self.velocity
            self.walk_index += self.walk_increase
            new_image = self.player_walk_l[int(self.walk_index)]

        if self.rect.bottom < self.ground_rect.top:
            new_image = self.player_jump
        self.image = new_image

    def set_boundary(self, background_surface):
        self.bound = [
            background_surface.x, #x min/top left pos at x
            background_surface.x + background_surface.width, #x max
            background_surface.y, #y min/top left pos at y
            background_surface.y + background_surface.height] #y man

    def boundary_x(self):
        if self.rect.left < self.bound[0]:
            self.rect.left = self.bound[0]
        if self.rect.right > self.bound[1]:
            self.rect.right = self.bound[1]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y  += self.gravity
        if self.rect.bottom >= self.ground_rect.top:
            self.rect.bottom = self.ground_rect.top
            self.gravity = 0

    def update(self):#main function to use
        self.player_input()
        self.boundary_x()
        self.apply_gravity()

class NoJumps(pygame.sprite.Sprite): # ? These are used for inheritance and copy and paste for new type of objects

    def __init__(self, background_rect, type = None):
        super().__init__()
        self.bound         = [] #from different rectangle (Screen Rectangle)
        self.ground_rect   = background_rect #basically weird code to know where to place on a surface (usually the TRUE_SCREEN.get_rect() with position values it has)

        self.walk_index    = 0.00
        self.walk_increase = 0.1

        self.fly = [
                pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]
        self.snail = [
                pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
                pygame.image.load('graphics/snail/snail2.png').convert_alpha()]

        self.enemy = None
        if type == "Fly":
            self.enemy = self.fly
        else:
            self.enemy = self.snail

        #player image-----------------
        self.image   = self.enemy[0]
        #-----------------------------

        self.animation_index    = 0.00
        self.animation_increase = 0.05
        self.velocity           = 3

        self.x_pos   = self.ground_rect.x
        self.y_pos   = self.ground_rect.y

        self.gravity = 0
        self.rect    = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

    def set_boundary(self, background_surface):
        self.bound = [
            background_surface.x, #x min/top left pos at x
            background_surface.x + background_surface.width, #x max
            background_surface.y, #y min/top left pos at y
            background_surface.y + background_surface.height] #y man

    def set_pos_bottlef(self, x_y):
        self.rect = self.image.get_rect(bottomleft = (x_y[0], x_y[1]))

    def move(self):
        #logic input
        new_image = self.enemy[0]

        #-----------------------------
        if self.animation_index + 0.10 >=  2:
            self.animation_index = 0.00
        #-----------------------------

        new_image = self.enemy[int(self.animation_index)]
        self.animation_index += self.animation_increase
        self.rect.x  -= self.velocity

        self.image = new_image

    def move_to_position(self):
        self.rect.x = self.bound[1]
        self.rect.y = self.ground_rect.y - 100

    def update(self):
        self.move()
        self.destroy()

    def destroy(self):
        if self.rect.left <= self.bound[0]*(.666):
            self.kill()
