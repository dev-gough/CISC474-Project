import random
import time

import pygame
import numpy as np

# initialize the game engine
pygame.init()

# colour definitions
black = (0, 0, 0)
white = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# sets up the window
size2 = 160
x = size2
y = size2
size3 = 8
size = [x, y]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tron")

Q = {}
policy = {}
'''for state in [(a, b, c, d, e, f, g, h, dir, opp) for a in range(2) for b in range(2) for c in range(2)
              for d in range(2) for e in range(2) for f in range(2) for g in range(2) for h in range(2)
              for dir in ["up", "down", "left", "right"] for opp in range(9)]:'''
for state in [(row, column, row2, column2) for row in range(size3) for column in range(size3)
              for row2 in range(size3) for column2 in range(size3)]:
    Q[state] = {}
    policy[state] = random.choice(["up", "down", "left", "right"])
    print(policy[state])
    #print(policy[state])
    for action in ["up", "down", "left", "right"]:
        Q[state][action] = 0

reward = 0


for i in range(2):
    print(Q[(1,1,1,1)]["up"])
    # sets the initial map
    screen.fill(black)
    for i in range(0, x, 20):
        pygame.draw.line(screen, white, [i, 0], [i, x], 1)
        pygame.draw.line(screen, white, [0, i], [y, i], 1)
    pygame.display.flip()
    # Variables for the first player
    p1x = x / 4
    p1y = y / 4
    p1alive = True
    p1colour = blue
    p1score = 0

    # Variables for the second player
    p2x = (x * 3) / 4
    p2y = (y * 3) / 4
    p2alive = True
    p2colour = yellow
    p2score = 0

    # Stores a bool as to whether or not the square has been traveled already
    grid = [[False for temp in range(int(x / 20))] for temp in range(int(y / 20))]

    # Sets up the loop for the game
    done = False

    # Sets the players initial directions
    p1direction = "right"
    p2direction = "left"

    clock = pygame.time.Clock()
    while not done:
        # Event handling
        for event in pygame.event.get():
            # Allows the loop to terminate when the user closes the window
            #if event.type == pygame.QUIT:
                #done = True

            # Handles keyboard input
            if event.type == pygame.KEYDOWN:

                # Changes Player 1's direction based off the key the player pressed
                if event.key == pygame.K_a:
                    if p1direction != "right":
                        p1direction = "left"
                elif event.key == pygame.K_d:
                    if p1direction != "left":
                        p1direction = "right"
                elif event.key == pygame.K_w:
                    if p1direction != "down":
                        p1direction = "up"
                elif event.key == pygame.K_s:
                    if p1direction != "up":
                        p1direction = "down"

                # Changes Player 2's direction based off the key the player pressed
                '''elif event.key == pygame.K_RIGHT:
                    if p2direction != "left":
                        p2direction = "right"
                elif event.key == pygame.K_UP:
                    if p2direction != "down":
                        p2direction = "up"
                elif event.key == pygame.K_DOWN:
                    if p2direction != "up":
                        p2direction = "down"
                elif event.key == pygame.K_LEFT:
                    if p2direction != "right":
                        p2direction = "left"'''

                # Allows the user to reset the game if the space bar is hit
                if event.key == pygame.K_SPACE:
                    screen.fill(black)
                    for i in range(0, x, 20):
                        pygame.draw.line(screen, white, [i, 0], [i, x], 1)
                        pygame.draw.line(screen, white, [0, i], [y, i], 1)
                    p1x = x / 4
                    p1y = y / 4
                    p1colour = blue
                    p2x = (x * 3) / 4
                    p2y = (y * 3) / 4
                    p2colour = yellow
                    grid = [[False for temp in range(int(x / 20))] for temp in range(int(y / 20))]
                    pygame.draw.rect(screen, p1colour, [p1x + 1, p1y + 1, (x / size3) - 1, (x / size3) - 1])
                    pygame.draw.rect(screen, p2colour, [p2x + 1, p2y + 1, (x / size3) - 1, (x / size3) - 1])
                    pygame.display.flip()
                    p1alive = True
                    p2alive = True

        print(policy[(int(p1x/20)-1, int(p1y/20)-1, int(p2x/20)-1, int(p2y/20)-1)])
        '''if p2direction != policy[(int(p1x / 20) - 1, int(p1y / 20) - 1, int(p2x / 20) - 1, int(p2y / 20) - 1)]:
            if p2direction != "left" and policy[(int(p1x / 20) - 1, int(p1y / 20) - 1, int(p2x / 20) - 1, int(p2y / 20) - 1)]:
                p2direction = "right"
            if p2direction != "down":
                p2direction = "up"
            if p2direction != "up":
                p2direction = "down"
            if p2direction != "right":
                p2direction = "left"'''
        p2direction = policy[(int(p1x/20)-1, int(p1y/20)-1, int(p2x/20)-1, int(p2y/20)-1)]

        if p2alive:
            reward = reward + 1
            print(reward)

        # Redraws the players based of their movement direction
        if p1alive or p2alive:
            p2colour = yellow
            pygame.draw.rect(screen, p1colour, [p1x + 1, p1y + 1, (x / size3) - 1, (x / size3) - 1])
            pygame.draw.rect(screen, p2colour, [p2x + 1, p2y + 1, (x / size3) - 1, (x / size3) - 1])
            pygame.display.flip()

        # checks player 1 will travel off the map
        if p1x >= size2 or p1x < 0 or p1y >= size2 or p1y < 0:
            p1alive = False
        # checks if player 1 will collide with another square
        else:
            if grid[int(p1x / 20 - 1)][int(p1y / 20 - 1)]:
                p1alive = False
            # sets the sqare p1 is on to true
            grid[int(p1x / 20 - 1)][int(p1y / 20 - 1)] = True

        # checks player 2 will travel off the map
        if p2x >= size2 or p2x < 0 or p2y >= size2 or p2y < 0:
            p2alive = False
            p2colour = red
        # checks if player 2 will collide with another square
        else:
            if grid[int(p2x / 20 - 1)][int(p2y / 20 - 1)]:
                p2alive = False
                p2colour = red
            # sets the sqare p1 is on to true
            grid[int(p2x / 20 - 1)][int(p2y / 20 - 1)] = True

        # Updates player 1's position if they have not collided
        if p1alive and p2alive:
            if p1direction == "left":
                p1x -= 20
            elif p1direction == "right":
                p1x += 20
            elif p1direction == "up":
                p1y -= 20
            elif p1direction == "down":
                p1y += 20
        # Updates player 2's position if they have not collided
        if p2alive and p1alive:
            if p2direction == "left":
                p2x -= 20
            elif p2direction == "right":
                p2x += 20
            elif p2direction == "up":
                p2y -= 20
            elif p2direction == "down":
                p2y += 20
        # Changes the player's current square to red if a collision occured
        if p1alive == False:
            p1colour = red
        if p2alive == False:
            p2colour = red

        if p1alive and p2alive == False:
            pygame.draw.rect(screen, p1colour, [p1x + 1, p1y + 1, (x / size3) - 1, (x / size3) - 1])
            pygame.draw.rect(screen, p2colour, [p2x + 1, p2y + 1, (x / size3) - 1, (x / size3) - 1])
            pygame.display.flip()
            p1score = p1score + 1
            print(p1score)
            print(p2score)
            reward = reward - 5
            print("Reward " + str(reward))
            time.sleep(5.5)
            done = True
        if p2alive and p1alive == False:
            p2score = p2score + 1
            print(p1score)
            print(p2score)
            reward = reward + 5
            print("Reward: " + str(reward))
            done = True

        clock.tick(8)
    #pygame.quit()

#peak()
#peak()
