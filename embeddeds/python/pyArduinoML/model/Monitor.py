from .Brick import Brick

class Monitor():

    def __init__(self):
        self.bricks: list = []
        # here we could also add mode and state

    def addBrick(self, brick: Brick):
        self.bricks.append(brick)

    def setup(self):
        return "\tSerial.begin(9600);"
