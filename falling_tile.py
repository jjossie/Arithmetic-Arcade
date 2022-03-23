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
            self.center_y -= 2


# class BlockGroupPosition(Enum):
#     """
#     Stores the file suffixes for the images representing relative block positions.
#     So like left/right/standalone/middle. I don't know man just look at the values
#     """
#     LEFT = "leftend"
#     RIGHT = "rightend"
#     MIDDLE = "middle"
#     STANDALONE = "edit"



# class BlockType(Enum):
#     """
#     Determines whether the block is movable, immovable, correct, etc. Basically
#     the block's status.
#     """
#     MOVABLE = "ground_03"
#     IMMOVABLE = "crate_42"
#     CORRECT = "crate_45"
#     INCORRECT = "crate_43"
#     OPERATION = "crate_01"




# class FallingTile(arcade.Sprite):
#     """
#         A falling tile class. For starters I want to have the tiles simply fall when they are stepped on.
#     """

#     def __init__(self, scene, value):
#         # I don't know why the super.init needs to be here.
#         super().__init__()
#         assert (value is not None and scene is not None)
#         self.value = value

#         self.block_type = BlockType.MOVABLE

#         self.block_group_position: BlockGroupPosition = BlockGroupPosition.STANDALONE
#         self.configure_texture()


#         self.texture = arcade.load_texture(CRATE_BLUE_PATH)
#         self.scale = TILE_SCALING
#         self._hit_box_algorithm = "None"

#         self.hit_box_sprite = arcade.Sprite(TRANSPARENT_BOX_PATH,
#                                             scale=TILE_SCALING * 1.1,
#                                             hit_box_algorithm="None",  # This is important
#                                             center_x=self.center_x,
#                                             center_y=self.center_y)
#         self.symbol_sprite = arcade.Sprite(self._get_symbol_path(),
#                                            scale=NUMBER_SCALING,
#                                            hit_box_algorithm="None")


#         scene.get_sprite_list(LAYER_NAME_FALLING_FLOOR).append(self)


#     def move_to(self, x, y):
#         """
#         Use this to move a NumberBlock rather than setting center_x and center_y directly.
#         Moves the sprite along with its accompanying hit box and symbol sprites.
#         This also exists for the purpose of polymorphism - to be synonymous with NumberBlockGroup,
#         which has the same function.
#         """
#         self.center_x = x
#         self.center_y = y
#         self.hit_box_sprite.center_x = x
#         self.hit_box_sprite.center_y = y
#         self.symbol_sprite.center_x = x
#         self.symbol_sprite.center_y = y


#     def set_block_type(self, block_type: BlockType):
#         self.block_type = block_type
#         self.configure_texture()




#     def configure_texture(self):
#         path = f"{FALLING_TILE_BASE_PATH}{self.block_type.value}{self.block_group_position.value}{IMG_PATH_EXT}"
#         # print(path)  # For debugging purposes
#         self.texture = arcade.load_texture(path)

