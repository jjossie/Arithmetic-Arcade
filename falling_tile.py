import arcade
import random

from constant import FALLING_TILE_PATH, LAYER_NAME_FALLING_TILE, LAYER_NAME_PLAYER
# from constant import *
# from numbers_and_math import BlockType
# from enum import Enum


class FallingTile(arcade.Sprite):

    def __init__(
        self,
        filename: str = None,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        flipped_horizontally: bool = False,
        flipped_vertically: bool = False,
        flipped_diagonally: bool = False,
        hit_box_algorithm: str = "Simple",
        hit_box_detail: float = 4.5,
        texture: arcade.Texture = None,
        angle: float = 0,
        # scene = None,
    ):

        super().__init__(scale=scale / 2)

        self.isFalling = False

        self.texture = arcade.load_texture(FALLING_TILE_PATH)
        self.player_sprite_list = None
    
    def setup(self, scene):

        print(f"FallingTile Scene: {scene}")

        self.player_sprite_list = scene.get_sprite_list(LAYER_NAME_PLAYER)
        


    def update(self):
        """ 
            - Move the tile. 
            - Then move the tile when the player touches it.
            - Then get numbers to show up on the tiles.
            - Then get the equation to show up in the top part of the screen.
            - Then make tiles only fall when player bumps into the wrong answer.
            - Then make room reset at the end door.
        """
        # Tile go fall down
        if self.collides_with_list(self.player_sprite_list):
            self.isFalling = True

        if self.isFalling:
            self.center_y -= 2

        print(f"Y: {self.center_y}")
        if self.center_y <= 0:
            self.kill()