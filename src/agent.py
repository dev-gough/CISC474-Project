"""
Agent class for CISC 474 final project
Written By: Devon Gough
"""


class Agent:

    def __init__(self, x, y, dir, colour, pol={}) -> None:
        self.x = x
        self.y = y
        self.dir = dir
        self.score = 0
        self.alive = True
        self.colour = colour
        self.policy = pol

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