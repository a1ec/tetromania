class Block:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = 2

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy