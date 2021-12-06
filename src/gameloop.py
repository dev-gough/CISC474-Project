"""
Gameloop class for CISC 474 final project
Written By: Alex Darcovich, Devon Gough, and Jack Taylor

Player 1 in this file refers to the agent that we are only using
to train our reinforcement learning agent.  Player 1 does not recieve
updates that alter it's behaviour, as it does not have a Q table.

Player 2 is the agent that we are conducting learning on.

Can be run as a standard python module in the command line (from the main git directory)
by running `python3 src/gameloop.py`.

Required Modules:
pip install pygame
pip install numpy
pip install matplotlib
"""

import time as t
import sys
import pygame
import numpy as np
import random
import matplotlib.pyplot as plt
import pickle

from agent import Agent

# Initialize pygame
pygame.init()
TICKRATE = 512

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


# Initialize the Q table
policy = {}
Q = {}
for state in [(a, b, c, d, e, f, g, h, direction, opp) 
    for a in range(2) for b in range(2) 
    for c in range(2) for d in range(2) 
    for e in range(2) for f in range(2) 
    for g in range(2) for h in range(2)
    for direction in ["w", "e", "n", "s"] for opp in range(9)]:

    Q[state] = {}
    policy[state] = random.choice(["w", "e", "n", "s"])
    for action in ["w", "e", "n", "s"]:
        Q[state][action] = 0


def run_loop(iters: int, accept_inputs: bool = False, smarter_p1: bool = True, draw_screen: bool = False, verbose: bool = False) -> tuple:
    """
    Run a game loop.

    Args:
        iters (int): The number of iterations to run.
        accept_inputs (bool): If the game will accept inputs from the player.
        smarter_p1 (bool): If player 1 (not the one we are applying Q-learning to)
            will use out-of-bounds avoidance.
        draw_screen (bool): Draw the screen using pygame. (not required)
        verbose (bool): Print various output for debugging.

    Returns:
        stats (list[list]): A 2d list of iteration stats of the form  [[iter, p1_wins, p2_wins],...]
        Q (dict{dict}): The final Q table representing the state-action pairs and their Q-values after training.
    
    """

    # Metrics to track
    stats = []
    p1_wins = 0
    p2_wins = 0

    if draw_screen:
        screen = pygame.display.set_mode([SIZE2,SIZE2])
        pygame.display.set_caption("Tron: CISC 474")

    for itr in range(iters):

        if draw_screen:
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

            if accept_inputs:
            # Event handling if accepting inputs from keyboard
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
                            
                            if draw_screen:
                                # Reset the game
                                
                                screen.fill(BLACK)
                                for i in range(0,SIZE2,20):
                                    pygame.draw.line(screen, WHITE, [i,0], [i,SIZE2])
                                    pygame.draw.line(screen, WHITE, [0,i], [SIZE2,i])

                            p1 = Agent(20, SIZE2/2, 'e', BLUE)
                            p2 = Agent(SIZE2 - 20, SIZE2/2, 'w', YELLOW)
                            grid = [[False for _ in range(int(SIZE2/20))] for _ in range(int(SIZE2/20))]

                            if draw_screen:
                                pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                                pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                            grid[int(p1.x / 20)][int(p1.y / 20)] = True
                            grid[int(p2.x / 20)][int(p2.y / 20)] = True

            else:
                moves = []
                x_moves = ["w", "e"]
                y_moves = ["n", "s"]

                # Don't go backwards
                if p1.dir in x_moves:
                    moves = [p1.dir] + y_moves
                if p1.dir in y_moves:
                    moves = x_moves + [p1.dir]

                # Remove moves that result in hitting boundaries
                if smarter_p1:
                    if p1.x + 20 >= SIZE2 and "w" in moves:
                        moves.remove("w")
                    if p1.x -20 < 0 and "e" in moves:
                        moves.remove("e")
                    if p1.y + 20 >= SIZE2 and "s" in moves:
                        moves.remove("s")
                    if p1.y -20 < 0 and "n" in moves:
                        moves.remove("n")

                if len(moves) > 0:
                    # Choose randomly from subset of moves
                    p1.dir = random.choice(moves)
                # Catch for no available moves
                else:
                    p1.dir = random.choice(["w", "e", "n", "s"])

                if verbose:
                    print("p1 move choices:" + str(moves))

            # Current state and action are returned from the epsilon greedy method.
            state, direction = p2.epsilon_greedy(p1.x, p1.y, p1.dir, SIZE3, grid, policy, itr)
            p2.dir = direction

            # Redraws the players based on their movement
            if (p1.alive or p2.alive) and draw_screen:
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

            # The following group of statements deal with rewards, changing the state, and updating the Q-table.
            
            if p2.alive:
                reward = 1

            if p1.alive and not p2.alive:
                if draw_screen:
                    pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                    pygame.draw.rect(screen, p2.colour, [p2.x + 1, p2.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                    pygame.display.flip()
                p1.score = p1.score + 1
                reward = -5
                done = True

                p1_wins = p1_wins + 1
                stats.append([itr, p1_wins, p2_wins])
            
            if p2.alive and not p1.alive:
                if draw_screen:
                    pygame.draw.rect(screen, p1.colour, [p1.x + 1, p1.y + 1, (SIZE2 / SIZE3) - 1, (SIZE2 / SIZE3) - 1])
                    pygame.display.flip()
                p2.score = p2.score + 1
                reward = 1
                done = True
                p2_wins = p2_wins + 1
                stats.append([itr, p1_wins, p2_wins])

            if not p1.alive and not p2.alive:
                reward = -5
                done = True
                stats.append([itr, p1_wins, p2_wins])

            # Updating state and Q-table.
            newState = p2.return_state(p1.x, p1.y, p1.dir, SIZE3, grid)
            Q[state][p2.dir] = Q[state][p2.dir] + 0.5 * (reward + 0.5 * p2.value_of_best_action(newState, Q) - Q[state][p2.dir])
            
            if verbose:
                print("State: " + str(state))
                print("NewState: " + str(newState))
                print("Action: " + str(p2.dir))
                print("Reward: " + str(reward))
                print(Q[state])
                print("Q: " + str(Q[state][p2.dir]))
            
            policy[state] = p2.update_policy(state, Q)
            clock.tick(TICKRATE)

    return stats, Q


def plot(stats: list, p1_label: str, p2_label: str) -> None:
    """
    Plot the stats list that returns from a successful training of an agent.

    Args:
        stats (list[list]): A 2d list of iteration stats.
        p1_label (str): The label for p1's portion of the graph
        p2_label (str): The label for p2's portion of the graph
    """
    x = []
    p1_y = []
    p2_y = []
    for entry in stats:
        #Time step
        x.append(entry[0])
        p1_y.append(entry[1])
        p2_y.append(entry[2])

    plt.plot(x, p1_y, label = p1_label)
    plt.plot(x, p2_y, label= p2_label)
    plt.legend()
    plt.ylabel('wins')
    plt.xlabel('number of games')
    plt.show()


def save(file: str, data, policy: bool = False) -> None:
    """Save a csv of the stats, or a numpy object of the policy."""
    file = "saves\\" + file
    if not policy:
        np.savetxt(file, data, fmt='%i', delimiter=',')
    else:
        np.save(file, data)
    

def load(file: str) -> dict:
    """Load a numpy object of a saved policy."""
    file = "saves\\" + file
    return np.load(file, allow_pickle='TRUE').item()

if __name__ == '__main__':
    """Run a training task with smarter_p1 and without smarter_p1"""
    NUM_ITERS = 5000

    start_time1 = t.time()
    dumb_stats, dumb_Q = run_loop(NUM_ITERS, smarter_p1=False)
    end_time1 = t.time()

    print("Run with smarter_p1=False succeeded.")
    print("Time elapsed: {t:.5}s".format(t=end_time1 - start_time1))

    start_time2 = t.time()
    smart_stats, smart_Q = run_loop(NUM_ITERS)
    end_time2 = t.time()

    print("Run with smarter_p1=True succeeded.")
    print("Time elapsed: {t:.5}s".format(t=end_time2 - start_time2))

    # Write stats into csv
    save('dumb_stats.csv', dumb_stats)
    save('smart_stats.csv', smart_stats)

    # Write policies to numpy object

    save('dumb_policy.npy',dumb_Q, policy=True)
    save('smart_policy.npy',smart_Q, policy=True)

    pygame.quit()