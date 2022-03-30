from constant import *

class Door(arcade.Sprite):

    target_room_string = ""
    room_operator = ""

    def __init__(self, target_room_string):
        super().__init__()

        self.target_room_string = target_room_string

        self.texture = arcade.load_texture(DOOR_TEXTURE)
        self.scale = TILE_SCALING


    # These should probably be required parameters in the initializer.
    def setCoordinates(self, set_x, set_y):
        self.center_x = set_x
        self.center_y = set_y

    def setTargetPlayerCoordinates(self, set_x, set_y):
        self.player_center_x = set_x
        self.player_center_y = set_y