#################################
#                               #
#   Family Christmas Showdown!  #
#                               #
#################################

# This is a multiplayer fighter game.  Up to 4 players.
# Designed to showcase on Christmas 2021.
# Chase down or avoid opponents.  Once you collide, fight.

# Installations

import pygame
import random
import time
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
from pygame.sprite import collide_rect

# Settings

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
QTY_PLAYERS = 4
QTY_GIFTS = 10

KEY_SET_1 = {"up": K_w, "left": K_a, "down": K_s, "right": K_d}
KEY_SET_2 = {"up": K_u, "left": K_h, "down": K_j, "right": K_k}
KEY_SET_3 = {"up": K_UP, "left": K_LEFT, "down": K_DOWN, "right": K_RIGHT}
KEY_SET_4 = {"up": K_KP8, "left": K_KP4, "down": K_KP5, "right": K_KP6}

GIFT = ".\images\\25gift.png"
GILL = ".\images\\50Gill.jpg"
DOUG = ".\images\\50Doug.jpg"
JAMES = ".\images\\50James.jpg"
KATHLEEN = ".\images\\50Kathleen.jpg"
IAN = ".\images\\50Ian.jpg"
JACK = ".\images\\50Jack.jpg"           # TODO: pick different image

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

    def __init__(self, keyset, image, startingZone):
        super(Player, self).__init__()
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        # place player in random location within specified zone
        self.rect = self.surf.get_rect(
            center = startingZone
        )
        self.up = keyset["up"]
        self.left = keyset["left"]
        self.down = keyset["down"]
        self.right = keyset["right"]

        # list of other players
        # self.otherPlayers = pygame.sprite.Group()

        # player's score
        self.score = 0

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
        # correct any moves offscreen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # handle once player collides with gift (ie. remove gift once collected)
        if pygame.sprite.spritecollide(self, allGifts, True):
            self.score += 1
        
# gift sprite class
class Gift(pygame.sprite.Sprite):

    def __init__(self):
        super(Gift, self).__init__()
        self.surf = pygame.image.load(GIFT).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        # place gift in random location
        self.rect = self.surf.get_rect(
            center = (
                random.randint(25, SCREEN_WIDTH - 25),
                random.randint(25, SCREEN_HEIGHT - 25)
            )
        )

        # get rid of the gift if it overlaps another gift
        pygame.sprite.spritecollide(self, allGifts, True)

# Initialize

pygame.init()

# Set Up Window and Framerate Clock

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Define Arrow Key Sets and Images

playerKeysets = (KEY_SET_1,KEY_SET_2, KEY_SET_3, KEY_SET_4)
playerImages = [GILL, DOUG, JAMES, KATHLEEN, IAN, JACK]
startingZones = (ZONE_1, ZONE_2, ZONE_3, ZONE_4)

# Create Sprite Objects
allPlayers = pygame.sprite.Group()
allGifts = pygame.sprite.Group()

# Create Players
random.shuffle(playerImages)    # randomize images
i = 0
while i < QTY_PLAYERS:
    newPlayer = Player(playerKeysets[i],playerImages[i],startingZones[i])
    allPlayers.add(newPlayer)
    i += 1

# Create Gifts
i = 0
while len(allGifts) < QTY_GIFTS:
    newGift = Gift()
    # check if new Gift intersects with any Players
    if pygame.sprite.spritecollideany(newGift, allPlayers):
        # if it overlaps, kill it so it can be recreated
        newGift.kill()
    else:
        # otherwise add it to the Gift sprite group
        allGifts.add(newGift)


# Create "Other Player" Sprints
# for focusSprite in allPlayers:
#     for otherSprite in allPlayers:
#         if otherSprite != focusSprite:
#             focusSprite.otherPlayers.add(otherSprite)


# Run Game

# run until window is closed
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
    allPlayers.update(pressedKeys)

    screen.fill((135,206, 250))
    screen.blit(pygame.image.load(".\images\skating-ice.jpg"), (0,0))

    # load gifts
    for sprite in allGifts:
        screen.blit(sprite.surf, sprite.rect)

    # load players
    for sprite in allPlayers:
        screen.blit(sprite.surf, sprite.rect)

    # end game condition: no gifts left
    if len(allGifts) < 1:
        # identify highest score (TODO: move to it's own function)
        winner = pygame.sprite.GroupSingle()
        # temp
        for player in allPlayers:
            print("Score: ", player.score)
        # highest winner
        if not winner:
            # put a placeholder winner in "Winner"      # TODO: make this less weird
            for player in allPlayers:
                winner.sprite = player
        for player in allPlayers:
            if player.score > winner.sprite.score:
                winner.sprite = player
        # print("Winning score is: ", winner.sprite.score)
        # kill non-winner sprites
        for player in allPlayers:
            if player != winner.sprite:
                player.kill()
        # pause for 1 second
        # time.sleep(1)
        # add box to screen
        # **************************************
        # display winner in the middle (TODO: move this into class)
        winner.sprite.rect.x = SCREEN_WIDTH / 2
        winner.sprite.rect.y = SCREEN_HEIGHT / 2
        # winner.sprite.rect.center(      
        #     SCREEN_WIDTH / 2,
        #     SCREEN_HEIGHT / 2
        # )
                
        # TODO: make text window appear
        # TODO: make icon of winner appear
        # TODO: print all scores
        # TODO: handle ties
        None


    # update the window
    pygame.display.flip()

    # set frame rate
    clock.tick(30)

# quit when loop has exited
pygame.quit()
