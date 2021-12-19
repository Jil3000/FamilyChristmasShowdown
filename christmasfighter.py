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

        # add box to screen
        winBox = pygame.Surface((400, 335))
        winBox.fill((200,233,233))
        winBoxRect = winBox.get_rect()
        # make box appear
        winBoxLocX = (SCREEN_WIDTH - winBox.get_width()) / 2
        winBoxLocY = (SCREEN_HEIGHT - winBox.get_height()) / 2
        screen.blit(winBox, (winBoxLocX, winBoxLocY))
        # add smaller box
        podiumBox = pygame.Surface((380, 75))
        podiumBox.fill((255,255,255))
        podiumBoxRect = podiumBox.get_rect()
        # make smaller box appear
        screen.blit(podiumBox, (winBoxLocX + 10, winBoxLocY + 10))

        # display winner in the middle (TODO: move this into class??)
        winner.sprite.rect.x = winBoxLocX + 25
        winner.sprite.rect.y = winBoxLocY + 25
        screen.blit(winner.sprite.surf, winner.sprite.rect)
        # add text to box
        winnerFont = pygame.font.SysFont('vivaldi', 40)
        winnerText = winnerFont.render("Winner! Score:" + str(winner.sprite.score), True, (0,0,0))
        winnerTextRect = winnerText.get_rect()
        winnerTextRect.center = (winBoxLocX + 225, winBoxLocY + 50)
        # make text appear
        screen.blit(winnerText, winnerTextRect)

        # make box to print other scores
        loserBox = pygame.Surface((380, 230))
        loserBox.fill((255,255,255))
        loserBoxRect = loserBox.get_rect()
        # make smaller box appear
        screen.blit(loserBox, (winBoxLocX + 10, winBoxLocY + 95))

        # TODO: print rest of scores on the box (move all 4 into some kind of class or function)
        second.sprite.rect.x = winBoxLocX + 25
        second.sprite.rect.y = winBoxLocY + 105
        # screen.blit(second.sprite.surf, (55, 75))
        screen.blit(second.sprite.surf, (second.sprite.rect))
        # add text to box
        secondFont = pygame.font.SysFont('vivaldi', 30)
        secondText = secondFont.render("Second place.  Score: " + str(second.sprite.score), True, (0,0,0))
        secondTextRect = secondText.get_rect()
        secondTextRect.center = (winBoxLocX + 225, winBoxLocY + 130)
        # make text appear
        screen.blit(secondText, secondTextRect)
        # TODO: handle ties

                # display third place in the middle (TODO: move this into class??)
        third.sprite.rect.x = winBoxLocX + 25
        third.sprite.rect.y = winBoxLocY + 185
        screen.blit(third.sprite.surf, third.sprite.rect)
        # add text to box
        thirdFont = pygame.font.SysFont('vivaldi', 30)
        thirdText = thirdFont.render("Third place.  Score: " + str(third.sprite.score), True, (0,0,0))
        thirdTextRect = thirdText.get_rect()
        thirdTextRect.center = (winBoxLocX + 225, winBoxLocY + 210)
        # make text appear
        screen.blit(thirdText, thirdTextRect)

                # display fourth place in the middle (TODO: move this into class??)
        fourth.sprite.rect.x = winBoxLocX + 25
        fourth.sprite.rect.y = winBoxLocY + 265
        screen.blit(fourth.sprite.surf, fourth.sprite.rect)
        # add text to box
        fourthFont = pygame.font.SysFont('vivaldi', 30)
        fourthText = fourthFont.render("Fourth place.  Score: " + str(fourth.sprite.score), True, (0,0,0))
        fourthTextRect = fourthText.get_rect()
        fourthTextRect.center = (winBoxLocX + 225, winBoxLocY + 290)
        # make text appear
        screen.blit(fourthText, fourthTextRect)

        pygame.display.flip()

        # pause         #TODO: fix so that subsequent loops don't run the win-screen related code
        beforeEndGame = False

    # update the window
    pygame.display.flip()

    # set frame rate
    clock.tick(30)

# quit when loop has exited
pygame.quit()
