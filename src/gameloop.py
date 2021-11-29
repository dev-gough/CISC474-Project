"""
Gameloop class for CISC 474 final project
Written By: Devon Gough
"""


import random as r
import time as t
import sys

import pygame
import numpy as np
import random

from agent import Agent

# Initialize pygame
pygame.init()
TICKRATE = 4

# Colours

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Window settings

SIZE2 = 240
SIZE3 = 12
MOVEMENTSPEED = 20

screen = pygame.display.set_mode([SIZE2,SIZE2])
pygame.display.set_caption("Tron: CISC 474")

# Policy stuff?
# TODO: Work with Alex to decide how to implement the Policy Class

policy = {}
Q = {}
for state in [(a, b, c, d, e, f, g, h, direction, opp) for a in range(2) for b in range(2) for c in range(2)
                      for d in range(2) for e in range(2) for f in range(2) for g in range(2) for h in range(2)
                      for direction in ["w", "e", "n", "s"] for opp in range(9)]:
    Q[state] = {}
    policy[state] = random.choice(["w", "e", "n", "s"])
    for action in ["w", "e", "n", "s"]:
        Q[state][action] = 0


def run_loop(iters: int):
    for itr in range(iters):

        # Sets initial map.
        screen.fill(BLACK)

        for i in range(0, SIZE2, 20):
            pygame.draw.line(screen, WHITE, [i,0], [i,SIZE2])
            pygame.draw.line(screen, WHITE, [0,i], [SIZE2,i])
        pygame.display.flip()

        # Initiates player1
        p1 = Agent(20, SIZE2/2, 'e', BLUE)
        p2 = Agent(SIZE2 - 20, SIZE2/2, 'w', YELLOW)
        agents = [p1,p2]

        # A boolean list of whether a given square has already been traveled
        grid = [[False for _ in range(int(SIZE2/20))] for _ in range(int(SIZE2/20))]
        grid[int(p1.x / 20)][int(p1.y / 20)] = True
        grid[int(p2.x / 20)][int(p2.y / 20)] = True
        done = False
        reward = 0

        clock = pygame.time.Clock()

        # Main game loop.
        while not done:

            # Event handling
            for event in pygame.event.get():

                # If the user wants to quit the game.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # p1 movement
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

                        p1 = Agent(20, SIZE2/2, 'e', BLUE)
                        p2 = Agent(SIZE2 - 20, SIZE2/2, 'w', YELLOW)
                        grid = [[False for _ in range(int(SIZE2/20))] for _ in range(int(SIZE2/20))]

                        pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                        pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                        grid[int(p1.x / 20)][int(p1.y / 20)] = True
                        grid[int(p2.x / 20)][int(p2.y / 20)] = True


            # TODO: Alex add your policy stuff here, I didn't copy it over because I'm not deleting main.py
            # TODO: Copy over anything you need here and leave both files.
            state, direction = p2.epsilonGreedy(p1.x, p1.y, p1.dir, SIZE3, grid, policy, itr)
            p2.dir = direction
            '''
            TODO - List
            
            Update Q value of current state and action and then immediately afterwards update policy of state
            Rewards
            '''

            # Redraws the players based on their movement
            if p1.alive or p2.alive:
                pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.display.flip()

            # Updates positions
            if p1.alive and p2.alive:
                p1.move(MOVEMENTSPEED)
                p2.move(MOVEMENTSPEED)

            # Checks to see if p1 will go OOB
            for a in agents:
                if not a.check_oob(SIZE2):
                    if not a.check_collide(grid):
                        grid[int(a.x / 20)][int(a.y / 20)] = True

            if p2.alive:
                reward = 1

            if p1.alive and not p2.alive:
                pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.display.flip()
                p1.score = p1.score + 1
                #print(p1.score)
                #print(p2.score)
                reward = -5
                #print("Reward " + str(reward))
                #t.sleep(5.5)
                done = True
            
            if p2.alive and not p1.alive:
                pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                #pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                pygame.display.flip()
                p2.score = p2.score + 1
                #print(p1.score)
                #print(p2.score)
                reward = 1
                #print("Reward: " + str(reward))
                #t.sleep(5.5)
                done = True

            if not p1.alive and not p2.alive:
                reward = -5
                done = True

            newState = p2.returnState(p1.x, p1.y, p1.dir, SIZE3, grid)
            Q[state][p2.dir] = Q[state][p2.dir] + 0.5 * (reward + 0.5 * p2.valueOfBestAction(newState, Q) - Q[state][p2.dir])
            print("State: " + str(state))
            print("NewState: " + str(newState))
            print("Action: " + str(p2.dir))
            print("Reward: " + str(reward))
            print(Q[state])
            print("Q: " + str(Q[state][p2.dir]))
            policy[state] = p2.updatePolicy(state, Q)

            clock.tick(TICKRATE)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_loop(500)