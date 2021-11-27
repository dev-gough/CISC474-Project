"""
Gameloop class for CISC 474 final project
Written By: Devon Gough
"""


import random as r
import time as t
import sys

import pygame
import numpy as np

from policy import Policy
from agent import Agent

# Initialize pygame
pygame.init()
TICKRATE = 8

# Colours

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Window settings

SIZE2 = 160
SIZE3 = 8
MOVEMENTSPEED = 20

screen = pygame.display.set_mode([160,160])
pygame.display.set_caption("Tron: CISC 474")

# Policy stuff?
# TODO: Work with Alex to decide how to implement the Policy Class
policy = Policy()
reward = 0

# Sets initial map.

screen.fill(BLACK)

for i in range(0, SIZE2, 20):
    pygame.draw.line(screen, WHITE, [i,0], [i,SIZE2])
    pygame.draw.line(screen, WHITE, [0,i], [SIZE2,i])

pygame.display.flip()

# Initiates player1
p1 = Agent(SIZE2/4, SIZE2/4, 'e', BLUE)
p2 = Agent((SIZE2*3)/4, (SIZE2*3)/4, 'w', YELLOW)

# A boolean list of whether a given square has already been traveled
grid = [[False for _ in range(int(SIZE2/20))] for _ in range(int(SIZE2/20))]

clock = pygame.time.Clock()

# Main game loop.
while True:
    # Event handling

    for event in pygame.event.get():

        # If the user wants to quit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            e = event.key

            if e == pygame.K_a:
                p1.dir = 'w'
            elif e == pygame.K_d:
                p1.dir = 'e'
            elif e == pygame.K_w:
                p1.dir = 'n'
            elif e == pygame.K_s:
                p1.dir = 's'
            elif e == pygame.K_SPACE:
                # Reset the game
                # TODO: See if you can make this into a function (to also call at the start)
                
                screen.fill(BLACK)
                for i in range(0,SIZE2,20):
                    pygame.draw.line(screen, WHITE, [i,0], [i,SIZE2])
                    pygame.draw.line(screen, WHITE, [0,i], [SIZE2,i])
                
                p1 = Agent(SIZE2/4, SIZE2/4, 'e', BLUE)
                p2 = Agent((SIZE2*3)/4, (SIZE2*3)/4, 'w', YELLOW)
                grid = [[False for _ in range(int(SIZE2/20))] for _ in range(int(SIZE2/20))]

                pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])

    # TODO: Alex add your policy stuff here, I didn't copy it over because I'm not deleting main.py
    # TODO: Copy over anything you need here and leave both files.

    # Redraws the players based on their movement
    if p1.alive or p2.alive:
        pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
        pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
        pygame.display.flip()
    
    # Checks to see if p1 will go OOB
    # TODO: Make this a function
    if p1.x >= SIZE2 or p1.x < 0 or p1.y >= SIZE2 or p1.y < 0:
        p1.alive = False
        p1.colour = RED
    # Checks to see if they will collide with a trail
    else:
        if grid[int(p1.x/(20-1))][int(p1.y/(20-1))]:
            p1.alive == False
            p1.colour = RED
        # Sets the square p1 is on to True
        grid[int(p1.x/(20-1))][int(p1.y/(20-1))] == True

    # Checks to see if p2 will go OOB
    # TODO: Make this a function call
    if p2.x >= SIZE2 or p2.x < 0 or p2.y >= SIZE2 or p2.y < 0:
        p2.alive = False
        p2.colour = RED
    # Checks to see if p2 will collide with a trail
    else:
        if grid[int(p2.x/(20-1))][int(p2.y/(20-1))]:
            p2.alive = False
            p2.colour = RED
        # Sets the square p2 is on to True
        grid[int(p2.x/(20-1))][int(p2.y/(20-1))] == True

    # Updates positions
    # TODO: Make this a function

    # P1:
    if p1.alive and p2.alive:
        if p1.dir == 'w':
            p1.x -= MOVEMENTSPEED
        elif p1.dir == 'e':
            p1.x += MOVEMENTSPEED
        elif p1.dir == 'n':
            p1.y += MOVEMENTSPEED
        else:
            p1.y -= MOVEMENTSPEED
    
        #TODO: Make this a function call
        if p2.dir == 'w':
            p2.x -= MOVEMENTSPEED
        elif p2.dir == 'e':
            p2.x += MOVEMENTSPEED
        elif p2.dir == 'n':
            p2.y += MOVEMENTSPEED
        else:
            p2.y -= MOVEMENTSPEED

    if p1.alive and not p2.alive:
        pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
        pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
        pygame.display.flip()
        p1.score = p1.score + 1
        print(p1.score)
        print(p2.score)
        reward = reward - 5
        print("Reward " + str(reward))
        t.sleep(5.5)
        pygame.quit()
        sys.exit()
    
    if p2.alive and not p1.alive:
        p2.score = p2.score + 1
        print(p1.score)
        print(p2.score)
        reward = reward + 5
        print("Reward: " + str(reward))
        t.sleep(5.5)
        pygame.quit()
        sys.exit()

    clock.tick(TICKRATE)
    
    

