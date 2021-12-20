#####################################
#                                   #
#   Family Christmas Showdown!      #
#                                   #
#####################################
#                                   #
# This is a multiplayer game for 4  #
# players.                          #
#                                   #
# Designed to showcase at Christmas #
# 2021 Demo Day.                    #
#                                   #
#####################################
#                                   #
# Instructions:                     #
#                                   #
# Gather gifts as quickly as        #
# possible.  The player with the    #
# most gifts wins!                  #
#                                   #
#####################################

# Installations

import pygame
import random
import time
from pygame.constants import K_1, K_2, K_3, K_4, RLEACCEL

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

QTY_PLAYERS = 4
QTY_GIFTS = 1

# screen size
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700

# key set groupings
KEY_SET_1 = {"up": K_w, "left": K_a, "down": K_s, "right": K_d}
KEY_SET_2 = {"up": K_u, "left": K_h, "down": K_j, "right": K_k}
KEY_SET_3 = {"up": K_UP, "left": K_LEFT, "down": K_DOWN, "right": K_RIGHT}
KEY_SET_4 = {"up": K_KP8, "left": K_KP4, "down": K_KP5, "right": K_KP6}

# player images
GIFT = ".\images\\25gift.png"
GILL = ".\images\\50Gill.jpg"
DOUG = ".\images\\50Doug.jpg"
JAMES = ".\images\\50James.jpg"
KATHLEEN = ".\images\\50Kathleen.jpg"
IAN = ".\images\\50Ian.jpg"
JACK = ".\images\\50Jack.jpg"

# starting zones so character don't start off overlapping or really close to each other
ZONE_1 = (
        # top left quadrant
        random.randint(0, SCREEN_WIDTH / 2),
        random.randint(0, SCREEN_HEIGHT / 2)
    )
ZONE_2 = (
        # bottom left quadrant
        random.randint(0, SCREEN_WIDTH / 2),
        random.randint(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
    )
ZONE_3 = (
        # top right quadrant
        random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT / 2)
    )
ZONE_4 = (
        # bottom right quadrant
        random.randint(SCREEN_WIDTH / 2, SCREEN_WIDTH),
        random.randint(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
    )

# to track whether I've already entered the endgame
# (solves issue where scoreboard disappears)
beforeEndGame = True

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
        # map keyset
        self.up = keyset["up"]
        self.left = keyset["left"]
        self.down = keyset["down"]
        self.right = keyset["right"]

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

        # handle player collision with gift (remove gift once collected)
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

# Functions

def findHighScore(playerGroup):
    currentHighScore = 0
    currentHighScorer = pygame.sprite.GroupSingle()
    for player in playerGroup:
        # find highest scorer
        if player.score >= currentHighScore:
            currentHighScore = player.score
            currentHighScorer.add(player)
    for player in playerGroup:
        if player == currentHighScorer.sprite:
            playerGroup.remove(player)
    return currentHighScorer, playerGroup


# Initialize Pygame

pygame.init()

# Set Up Window and Framerate Clock

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Collect Arrow Key Sets, Images, Zones
playerKeysets = (KEY_SET_1,KEY_SET_2, KEY_SET_3, KEY_SET_4)
playerImages = [GILL, DOUG, JAMES, KATHLEEN, IAN, JACK]
startingZones = (ZONE_1, ZONE_2, ZONE_3, ZONE_4)

# Create Sprite Groups
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

    if beforeEndGame:   # don't run after the game has ended (overwrites scoresheet)

        # load background
        screen.blit(pygame.image.load(".\images\skating-ice.jpg"), (0,0))

        # load gifts
        for sprite in allGifts:
            screen.blit(sprite.surf, sprite.rect)

        # load players
        for sprite in allPlayers:
            screen.blit(sprite.surf, sprite.rect)

    # end game condition: no gifts left
    if len(allGifts) < 1 and beforeEndGame:
        
        beforeEndGame = False

        # create single sprite group for each rank
        winner = pygame.sprite.GroupSingle()
        second = pygame.sprite.GroupSingle()
        third = pygame.sprite.GroupSingle()
        fourth = pygame.sprite.GroupSingle()

        # find each rank and move player from allPlayers to rank group
        winner, allPlayers = findHighScore(allPlayers)
        second, allPlayers = findHighScore(allPlayers)
        third, allPlayers = findHighScore(allPlayers)
        fourth, allPlayers = findHighScore(allPlayers)

# -------------------------------------------------------------------

# NEXT: unfuck the below

        '''
        items to handle:
        - main results box  "resultsBox"
        - winner box    "winBox"
        - losers box    "loseBox"
        - text?
        '''

        # Endgame Layout Specs

        # colours

        WHITE = (255,255,255)
        BLACK = (0,0,0)
        ICE_BLUE = (200,233,233)

        # fonts

        WINNER_FONT = pygame.font.SysFont('vivaldi', 40)
        LOSERS_FONT = pygame.font.SysFont('vivaldi', 30)

        # relative distances

        SPRITE_SIZE = 50
        BOX_PADDING = 10
        PLAYER_PADDING = 15
        TEXT_PADDING = 30

        # box dimensions

        RESULTS_BOX_WIDTH = 400
        RESULTS_BOX_HEIGHT = (SPRITE_SIZE * 4) + (PLAYER_PADDING * 6) + (BOX_PADDING * 3)

        WINNER_BOX_WIDTH = RESULTS_BOX_WIDTH - (BOX_PADDING * 2)
        WINNER_BOX_HEIGHT = SPRITE_SIZE + (PLAYER_PADDING * 2)

        LOSER_BOX_WIDTH = RESULTS_BOX_WIDTH - (BOX_PADDING * 2)
        LOSER_BOX_HEIGHT = (SPRITE_SIZE * 3) + (PLAYER_PADDING * 4)

        # box locations

        RESULTS_BOX_LOC_X = (SCREEN_WIDTH - RESULTS_BOX_WIDTH) / 2
        RESULTS_BOX_LOC_Y = (SCREEN_HEIGHT - RESULTS_BOX_HEIGHT) / 2

        WINNER_BOX_LOC_X = RESULTS_BOX_LOC_X + BOX_PADDING
        WINNER_BOX_LOC_Y = RESULTS_BOX_LOC_Y + BOX_PADDING

        LOSER_BOX_LOC_X = RESULTS_BOX_LOC_X + BOX_PADDING
        LOSER_BOX_LOC_Y = RESULTS_BOX_LOC_Y + WINNER_BOX_HEIGHT + (BOX_PADDING * 2)

        # sprite locations

        WINNER_SPRITE_LOC_X = WINNER_BOX_LOC_X + PLAYER_PADDING
        WINNER_SPRITE_LOC_Y = WINNER_BOX_LOC_Y + PLAYER_PADDING
        
        SECOND_SPRITE_LOC_X = LOSER_BOX_LOC_X + PLAYER_PADDING
        SECOND_SPRITE_LOC_Y = LOSER_BOX_LOC_Y + PLAYER_PADDING
        
        THIRD_SPRITE_LOC_X = LOSER_BOX_LOC_X + PLAYER_PADDING
        THIRD_SPRITE_LOC_Y = SECOND_SPRITE_LOC_Y + SPRITE_SIZE + PLAYER_PADDING
        
        FOURTH_SPRITE_LOC_X = LOSER_BOX_LOC_X + PLAYER_PADDING
        FOURTH_SPRITE_LOC_Y = THIRD_SPRITE_LOC_Y + SPRITE_SIZE + PLAYER_PADDING
        
        # text locations

        WINNER_TEXT_CENTER_X = (SCREEN_WIDTH + SPRITE_SIZE) / 2
        WINNER_TEXT_CENTER_Y = WINNER_BOX_LOC_Y + (WINNER_BOX_HEIGHT / 2)

        SECOND_TEXT_CENTER_X = (SCREEN_WIDTH + SPRITE_SIZE) / 2
        SECOND_TEXT_CENTER_Y = LOSER_BOX_LOC_Y + PLAYER_PADDING + (SPRITE_SIZE / 2)

        THIRD_TEXT_CENTER_X = (SCREEN_WIDTH + SPRITE_SIZE) / 2
        THIRD_TEXT_CENTER_Y = SECOND_TEXT_CENTER_Y + PLAYER_PADDING + SPRITE_SIZE

        FOURTH_TEXT_CENTER_X = (SCREEN_WIDTH + SPRITE_SIZE) / 2
        FOURTH_TEXT_CENTER_Y = THIRD_TEXT_CENTER_Y + PLAYER_PADDING + SPRITE_SIZE


        # create results box
        resultsBox = pygame.Surface((RESULTS_BOX_WIDTH, RESULTS_BOX_HEIGHT))
        resultsBoxRect = resultsBox.get_rect()
        resultsBox.fill(ICE_BLUE)

        # create winner box
        winnerBox = pygame.Surface((WINNER_BOX_WIDTH, WINNER_BOX_HEIGHT))
        winnerBoxRect = winnerBox.get_rect()
        winnerBox.fill(WHITE)

        # create loser box
        loserBox = pygame.Surface((LOSER_BOX_WIDTH, LOSER_BOX_HEIGHT))
        loserBoxRect = loserBox.get_rect()
        loserBox.fill(WHITE)

        # put boxes on screen
        screen.blit(resultsBox, (RESULTS_BOX_LOC_X, RESULTS_BOX_LOC_Y))
        screen.blit(winnerBox, (WINNER_BOX_LOC_X, WINNER_BOX_LOC_Y))
        screen.blit(loserBox, (LOSER_BOX_LOC_X, LOSER_BOX_LOC_Y))

        # add sprites to boxes
        winner.sprite.rect.x = WINNER_SPRITE_LOC_X
        winner.sprite.rect.y = WINNER_SPRITE_LOC_Y

        second.sprite.rect.x = SECOND_SPRITE_LOC_X
        second.sprite.rect.y = SECOND_SPRITE_LOC_Y
        
        third.sprite.rect.x = THIRD_SPRITE_LOC_X
        third.sprite.rect.y = THIRD_SPRITE_LOC_Y
        
        fourth.sprite.rect.x = FOURTH_SPRITE_LOC_X
        fourth.sprite.rect.y = FOURTH_SPRITE_LOC_Y

        # put sprites on screen
        screen.blit(winner.sprite.surf, winner.sprite.rect)
        screen.blit(second.sprite.surf, second.sprite.rect)
        screen.blit(third.sprite.surf, third.sprite.rect)
        screen.blit(fourth.sprite.surf, fourth.sprite.rect)

        # add texts to boxes
        
        winnerText = WINNER_FONT.render("Winner! Score:" + str(winner.sprite.score), True, BLACK)
        winnerTextRect = winnerText.get_rect()
        winnerTextRect.center = (WINNER_TEXT_CENTER_X, WINNER_TEXT_CENTER_Y)

        secondText = LOSERS_FONT.render("Second place.  Score:" + str(second.sprite.score), True, BLACK)
        secondTextRect = secondText.get_rect()
        secondTextRect.center = (SECOND_TEXT_CENTER_X, SECOND_TEXT_CENTER_Y)

        thirdText = LOSERS_FONT.render("Third place.  Score:" + str(third.sprite.score), True, BLACK)
        thirdTextRect = thirdText.get_rect()
        thirdTextRect.center = (THIRD_TEXT_CENTER_X, THIRD_TEXT_CENTER_Y)

        fourthText = LOSERS_FONT.render("Fourth place.  Score:" + str(fourth.sprite.score), True, BLACK)
        fourthTextRect = fourthText.get_rect()
        fourthTextRect.center = (FOURTH_TEXT_CENTER_X, FOURTH_TEXT_CENTER_Y)

        # put texts on screen
        screen.blit(winnerText, winnerTextRect)
        screen.blit(secondText, secondTextRect)
        screen.blit(thirdText, thirdTextRect)
        screen.blit(fourthText, fourthTextRect)

    # update the window
    pygame.display.flip()

    # set frame rate
    clock.tick(30)

# quit when loop has exited
pygame.quit()
