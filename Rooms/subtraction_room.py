"""
Designed to make file mananging easier. This is just the subtraction room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from FallingTileStuff.falling_tile import FallingTile
from numbers_and_math import VisualMathProblem
from door import Door
from Level import Level


class SubtractionRoom(Level):
    def __init__(self):
        super().__init__()
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

        # Make the scene using the inherited method
        self.scene = self.make_scene(map_name, room_operator, layer_options)

        # Set up the falling tiles
        for tile in self.scene.get_sprite_list(LAYER_NAME_FALLING_TILE):
            tile.setup(self.scene)

        problems = [
            VisualMathProblem(self.scene, 235, 1055, 1, 10, operator_str="-"),
        ]
        for problem in problems:
            problem.draw()

        home_door = Door("home")
        home_door.setCoordinates(500, 500)
        home_door.setTargetPlayerCoordinates(600, 330)
        self.scene.add_sprite(LAYER_NAME_DOORS, home_door)
