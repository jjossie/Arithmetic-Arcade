import arcade


class NumberBlock(arcade.Sprite):
    def __init__(self, value=0):
        super().__init__()
        self.value = value
