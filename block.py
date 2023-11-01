import colors

class Block:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = colors.RED

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy