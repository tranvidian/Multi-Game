#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import pygame
#Important for our application to close
from sys import exit

pygame.init()


var_x_length = 800
var_y_length = 400
screen = pygame.display.set_mode((var_x_length,var_y_length))
#set title on application
pygame.display.set_caption("Vidian Game")


#frames setup (animation fixed on this variable not changed yet)
clock = pygame.time.Clock()


#--------------------------------------------------------------------------------------------------------------
#surfaces
#call for creating surface
test_surface = pygame.Surface((100,200))
test_surface.fill("Red")

sky_surface = pygame.image.load("graphics/Sky.png").convert()#use convert_alpha for player models
ground_surface = pygame.image.load("graphics/ground.png").convert()

test_font= pygame.font.Font(None,50)
text_surface= test_font.render("My game", False, "Red")

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
#positional method that helps places it (returns position based on what we grabbed)
player_rect= player_surface.get_rect(midbottom = (80,300))
var_gravity = 0
# ! New addition to code
print("test get rect return info\n", player_rect, "\n" , player_rect.topleft)
#--------------------------------------------------------------------------------------------------------------
#Functions
def events():
    for event in pygame.event.get():
        global var_gravity
        if event.type == pygame.QUIT:
            #close our screen variable when one event (x button) in list
            pygame.quit()
            print("Credit for making lessons on making pygames https://youtu.be/AY9MnQ4x3zk \n https://github.com/clear-code-projects/UltimatePygameIntro")
            #from sys import (closes the loop code)
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >=300:
                var_gravity = -20
        elif event.type == pygame.MOUSEMOTION:
            if player_rect.collidepoint(event.pos):
                var_gravity = -20


def static_blits():
    #how its plots its surface is based on the top left of the image
    # and puts the top left image at that point given (x,y)
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300)) #ground position y is 300
    #screen.blit(test_surface,(0,0))
    screen.blit(text_surface,(50,0))

def non_static_blits():
    global var_gravity
    #how we access a variable from class??
    #player_rect.x -= 1

#what are these method variables is grabbing??
    var_gravity += 1
    player_rect.y += var_gravity
    if player_rect.right == -100: player_rect.left = 800
    if player_rect.bottom >= 300: player_rect.bottom = 300
    screen.blit(player_surface,player_rect)#ground position y is 300


#--------------------------------------------------------------------------------------------------------------
#Main Loop to play game

while True: #draw all stuff/element and update all in while loop

    events()
    #active pieces for screen
    static_blits()
    non_static_blits()

    #collision test
#    if rect1.colliderect(rect2):
#        print("collision to other named object")
#    if rect1.collidepoint((x,y)):
#        print("collide point")

#applies all the blits to the original screen
    pygame.display.update()
    clock.tick(60)

