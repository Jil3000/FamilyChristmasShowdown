#################################
#                               #
#   Family Chritmas Showdown!   #
#                               #
#################################

# This is a multiplayer fighter game.  Up to 4 players.
# Designed to showcase on Christmas 2021.
# Chase down or avoid opponents.  Once you collide, fight.

# Installations

import pygame
import random
from pygame.constants import RLEACCEL

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    # key set 1
    K_w,
    K_a,
    K_s,
    K_d,
    # key set 2
    K_u,
    K_h,
    K_j,
    K_k,
    # key set 3
    K_UP,
    K_LEFT,
    K_DOWN,
    K_RIGHT,
    # key set 4
    K_KP8,
    K_KP4,
    K_KP5,
    K_KP6
)

# Settings

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
QTY_PLAYERS = 4

KEY_SET_1 = {"up": K_w, "left": K_a, "down": K_s, "right": K_d}
KEY_SET_2 = {"up": K_u, "left": K_h, "down": K_j, "right": K_k}
KEY_SET_3 = {"up": K_UP, "left": K_LEFT, "down": K_DOWN, "right": K_RIGHT}
KEY_SET_4 = {"up": K_KP8, "left": K_KP4, "down": K_KP5, "right": K_KP6}

GILL = ".\images\\50Gill.jpg"
DOUG = ".\images\\50Doug.jpg"
JAMES = ".\images\\50James.jpg"
KATHLEEN = ".\images\\50Kathleen.jpg"
IAN = ".\images\\50Ian.jpg"
EVELYN = ".\images\\50Evelyn.jpg"

# starting zones so character don't start off overlapping or really close to each other
ZONE_1 = (
        random.randint(0, SCREEN_WIDTH / 2),
        random.randint(0, SCREEN_HEIGHT / 2)
    )
ZONE_2 = (
        random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT / 2)
    )
ZONE_3 = (
        random.randint(0, SCREEN_WIDTH / 2),
        random.randint(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
    )
ZONE_4 = (
        random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH),
        random.randint(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
    )    

# player sprite class
class Player(pygame.sprite.Sprite):

    def __init__(self, keyset, image, startingZone):     # TODO: need to figure out how I'm passing the arrow key and image info.  currently I'm assuming "keyset" will be a dict
        super(Player, self).__init__()
        self.surf = pygame.image.load(image).convert()    # TODO: each player will need a unique image. how??
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        # place player in random location   # TODO: deal with edge case of starting in the exact same or overlapping location
        self.rect = self.surf.get_rect(
            center = startingZone
        )
        self.up = keyset["up"]
        self.left = keyset["left"]
        self.down = keyset["down"]
        self.right = keyset["right"]

    # move player based on keyset
    def update(self, pressedKeys):
        if pressedKeys[self.up]:
            self.rect.move_ip(0,-5)
        if pressedKeys[self.left]:
            self.rect.move_ip(-5,0)
        if pressedKeys[self.down]:
            self.rect.move_ip(0,5)
        if pressedKeys[self.right]:
            self.rect.move_ip(5,0)
        # correct any moes offscreen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        # detect collisions?
        battleOpponents = pygame.sprite.spritecollide(self, allPlayers,False)
        # print("battleOpponents: ", battleOpponents.sprites())
        # if len(battleOpponents) > 1:    # this method left a problem (see TODO below) but kinda worked
        #     battleOpponents[1].kill()       # TODO: figure out how I wouuld just kill the one who initiated
        # NEW TODO: just select those two sprites, so I can use them for a battle.  add them into a new group.
        return battleOpponents

# Initialize

pygame.init()

# Set Up Window and Framerate Clock

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Define Arrow Key Sets and Images

playerKeysets = (KEY_SET_1,KEY_SET_2, KEY_SET_3, KEY_SET_4)
playerImages = [GILL, DOUG, JAMES, KATHLEEN, IAN, EVELYN]
startingZones = (ZONE_1, ZONE_2, ZONE_3, ZONE_4)

# Create Sprite Object

allPlayers = pygame.sprite.Group()

# Create Players

# randomize images
random.shuffle(playerImages)
i = 0
while i < QTY_PLAYERS:
    newPlayer = Player(playerKeysets[i],playerImages[i],startingZones[i])
    allPlayers.add(newPlayer)
    i += 1

# Run Game

# run until player quits
running = True
while running:
    for event in pygame.event.get():
        # check if user closes window
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # check if user presses ESC
        elif event.type == QUIT:
            running = False

    # pull pressed keys from the queue
    pressedKeys = pygame.key.get_pressed()

    # update players and get collision opponents
    battleOpponents = allPlayers.update(pressedKeys)

    screen.fill((135,206, 250))     #TODO: replace with background image of snow
    screen.blit(pygame.image.load(".\images\skating-ice.jpg"), (0,0))

    # load players
    for sprite in allPlayers:
        screen.blit(sprite.surf, sprite.rect)

    # collision event: initiate fight
    if battleOpponents:
        print(battleOpponents.sprites())
    # battleOpponents = pygame.sprite.spritecollide()
    # if battleOpponents:
    #     print("collision detected")
    # TODO: this

    # end game condition: one player left
    # TODO: this (I assume I'll just check the quantity of allPlayers?)

    # update the window
    pygame.display.flip()

    # set frame rate
    clock.tick(30)

# quit when loop has exited
pygame.quit()
