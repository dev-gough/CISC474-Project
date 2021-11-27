"""
Agent class for CISC 474 final project
Written By: Devon Gough
"""

class Agent:

    def __init__(self, x, y, dir, colour) -> None:
        self.x = x
        self.y = y
        self.dir = dir
        self.score = 0
        self.alive = True
        self.colour = colour

    def __repr__(self) -> str:
        return 'x: {x}, y: {y}, dir: {dir}, score: {s}, alive: {a}, colour: {c}'.format(
            x=self.x,y=self.y,dir=self.dir,s=self.score,a=self.alive,c=self.colour)

    def move(self, dist:int) -> None:
        if self.dir == 'n':
            self.y += dist
        elif self.dir == 'e':
            self.x += dist
        elif self.dir == 's':
            self.y -= dist
        else:
            self.x -= dist
    
    