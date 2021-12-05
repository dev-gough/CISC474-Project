"""
Agent class for CISC 474 final project
Written By: Alex Darcovich, Devon Gough, and Jack Taylor
"""
import random

class Agent:

    """
    The agent class contains all methods and attributes necessary to
    enable reinforcement learning.
    """

    def __init__(self, x, y, dir, colour) -> None:
        """
        Initialize an Agent object.

        Args:
            x (int): The x coordinate of the agent.
            y (int): The y coordinate of the agent.
            dir (str) : The direction the agent is facing. ['n','e','s','w'] supported.
            colour (tuple): The RGB values for the colour trail of the agent. (int,int,int)
        """

        self.x = x
        self.y = y
        self.dir = dir
        self.score = 0
        self.alive = True
        self.colour = colour

    def return_state(self, p1x, p1y, p1dir, size, grid):
        """
        Return the next state (s') after the agent has moved.
        Player 2 is `self` here.

        Args:
            p1x (int): The x coordinate of the player 1.
            p1y (int): The y coordinate of the player 1.
            p1dir (int): The direction player 1 is moving.
            size (int): The size of the board.
            grid (list[list]): A 2d list of boolean values, 
                indicating if an agent has been to a square on the grid before.

        Returns:
            A 10-tuple where the first 8 elements are the vision grid, 
            either 0 if the grid location is neither a boundry nor has been visited, and 1 otherwise.  
            The 9th is the current  direction of the opponent.
            The 10th determines whether the opponent's head is in the vision grid, and if so, returns the index of where it is, else returning 8.
        """

        ring = [0 for i in range(8)]
        counter = 0
        ringOpp = 8
        for k in range(-1, 2):
            for j in range(-1, 2):
                if k != 0 or j != 0:
                    if int(self.x / 20) + k == p1x/20 and int(self.y / 20) + j == p1y/20:
                        ringOpp = counter

                    if int(self.x / 20) + k < 0 or int(self.x / 20) + k >= size or \
                            int(self.y / 20) + j < 0 or int(self.y / 20) + j >= size:
                        ring[counter] = 1
                    elif grid[int(self.x / 20) + k][int(self.y / 20) + j]:
                        ring[counter] = 1
                    else:
                        ring[counter] = 0
                    counter = counter + 1

        return (ring[0], ring[1], ring[2], ring[3], ring[4], ring[5], ring[6], ring[7], p1dir, ringOpp)

    def epsilon_greedy(self, p1x, p1y, p1dir, size, grid, policy, iter):
        """
        Generate an e-greedy decision for the agent.

        Args:
            p1x (int): The x coordinate of player 1.
            p1y (int): The y coordinate of player 1.
            p1dir (int): The direction player 1 is moving.
            size (int): The size of the board.
            grid (list[list]): A 2d list of boolean values, 
                indicating if an agent has been to a square on the grid before.
            policy (dict{dict}): A nested dictionary of state-action pairs.
            iter (int): The current iteration.
        
        Returns:
            The state-action pair in a tuple.

        """
        if iter == 0 or random.uniform(0, 1) < 1/iter:
            state = self.return_state(p1x, p1y, p1dir, size, grid)
            return state, random.choice(["w", "e", "n", "s"])
        else:
            state = self.return_state(p1x, p1y, p1dir, size, grid)
            return state, policy[state]

    

    def __repr__(self) -> str:
        return 'x: {x}, y: {y}, dir: {dir}, score: {s}, alive: {a}, colour: {c}'.format(
            x=self.x,y=self.y,dir=self.dir,s=self.score,a=self.alive,c=self.colour)

    def move(self, dist:int) -> None:
        """Move the agent repending on its direction and distance provided."""
        if self.dir == 'n':
            self.y -= dist
        elif self.dir == 'e':
            self.x += dist
        elif self.dir == 's':
            self.y += dist
        else:
            self.x -= dist
    
    def check_oob(self, size: int):
        """Check to see if the agent is going to go out of bounds."""
        if self.x >= size or self.x < 0 or self.y >= size or self.y < 0:
            self.alive = False
            self.colour = (255, 0, 0)
            return True
        return False

    def check_collide(self, grid: list) -> bool:
        """Check to see if the agent is going to collide with a trail/head."""
        if grid[int(self.x/20)][int(self.y/20)]:
            self.alive = False
            self.colour = (255, 0, 0)
            return True
        else:
            return False

    def value_of_best_action(self, state, Q):
        """Return the maximum Q value of any action given a state."""
        best_Q = -float("inf")
        for action in Q[state]:
            best_Q = max(best_Q, Q[state][action])
        return best_Q

    def update_policy(self, state, Q):
        """Return the best action corresponding to the Q value of a state."""
        best_Q = -float("inf")
        for action in Q[state]:
            if best_Q < Q[state][action]:
                best_Q = Q[state][action]
                bestAction = action
        return bestAction