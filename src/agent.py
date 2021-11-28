"""
Agent class for CISC 474 final project
Written By: Devon Gough
"""
import random

class Agent:

    def __init__(self, x, y, dir, colour, pol={}) -> None:
        self.x = x
        self.y = y
        self.dir = dir
        self.score = 0
        self.alive = True
        self.colour = colour
        self.policy = self.initializePolicy()
        self.Q = self.initializeStateAction()

    def initializePolicy(self):
        policy = {}
        for state in [(a, b, c, d, e, f, g, h, direction, opp) for a in range(2) for b in range(2) for c in range(2)
                      for d in range(2) for e in range(2) for f in range(2) for g in range(2) for h in range(2)
                      for direction in ["w", "e", "n", "s"] for opp in range(9)]:
            policy[state] = random.choice(["w", "e", "n", "s"])
        return policy

    def initializeStateAction(self):
        Q = {}
        for state in [(a, b, c, d, e, f, g, h, direction, opp) for a in range(2) for b in range(2) for c in range(2)
                      for d in range(2) for e in range(2) for f in range(2) for g in range(2) for h in range(2)
                      for direction in ["w", "e", "n", "s"] for opp in range(9)]:
            Q[state] = {}
            for action in ["w", "e", "n", "s"]:
                Q[state][action] = 0
        return Q

    def epsilonGreedy(self, p1x, p1y, p1dir, size2, grid):
        if random.uniform(0, 1) < 0.1:
            return random.choice(["w", "e", "n", "s"])
        else:
            ring = [0 for i in range(8)]
            counter = 0
            ringOpp = 8
            for k in range(-1, 2):
                for j in range(-1, 2):
                    if k != 0 or j != 0:
                        if int(self.x / 20) + k == p1x and int(self.y / 20) + j == p1y:
                            ringOpp = counter

                        if int(self.x / 20) + k < 0 or int(self.x / 20) + k >= size2 or \
                                int(self.y / 20) + j < 0 or int(self.x / 20) + j >= 0:
                            ring[counter] = 1
                        elif grid[int(self.x / 20) + k][int(self.y / 20) + j]:
                            ring[counter] = 1
                        else:
                            ring[counter] = 0

            return self.policy[(ring[0], ring[1], ring[2], ring[3], ring[4], ring[5], ring[6], ring[7], p1dir, ringOpp)]



    def __repr__(self) -> str:
        return 'x: {x}, y: {y}, dir: {dir}, score: {s}, alive: {a}, colour: {c}'.format(
            x=self.x,y=self.y,dir=self.dir,s=self.score,a=self.alive,c=self.colour)

    def move(self, dist:int) -> None:
        if self.dir == 'n':
            self.y -= dist
        elif self.dir == 'e':
            self.x += dist
        elif self.dir == 's':
            self.y += dist
        else:
            self.x -= dist
    
    def check_oob(self, size: int):
        if self.x >= size or self.x < 0 or self.y >= size or self.y < 0:
            self.alive = False
            self.colour = (255, 0, 0)
            return True
        return False

    def check_collide(self, grid: list) -> bool:
        if grid[int(self.x/20)][int(self.y/20)]:
            self.alive = False
            self.colour = (255, 0, 0)
            return True
        else:
            return False

    def update_q(self):
        self._update_policy()
        pass

    def _update_policy(self):
        pass