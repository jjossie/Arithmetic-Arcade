"""
Designed to make file mananging easier. This is just the subtraction room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from FallingTileStuff.falling_tile import FallingTile
from numbers_and_math import VisualMathProblem
from door import Door
    
def setupSubtractionRoom(self):
    map_name = "maps/falling-tile-demo.tmx"
    room_operator = "-"
    self.is_falling_tile_map = True

    # Custom map options
    layer_options = {
        LAYER_NAME_FALLING_TILE: {
            "custom_class": FallingTile,
            "custom_class_args": {
            }
        }
    }

    # Load tile_map
    self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

    # Initialize Scene from the tilemap
    self.scene = arcade.Scene.from_tilemap(self.tile_map)
    # repeat line 91 and line 88
    # Create the Sprite lists
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
    self.scene.add_sprite_list(LAYER_NAME_PLAYER)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)
    self.scene.add_sprite_list(LAYER_NAME_DOORS)

    self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)


    for tile in self.scene.get_sprite_list(LAYER_NAME_FALLING_TILE):
        tile.setup(self.scene)

    problems = [
        VisualMathProblem(self.scene, 235, 1055, 1, 10, operator_str="-"),

    ]
    for problem in problems:
        problem.draw()

    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEngineSimple(
        self.player, [
            self.scene.get_sprite_list(LAYER_NAME_WALLS),
            self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        ]
    )