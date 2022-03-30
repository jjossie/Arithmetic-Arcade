"""
Designed to make file mananging easier. This is just the subtraction room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from FallingTileStuff.falling_tile import FallingTile
from numbers_and_math import VisualMathProblemLocation
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
            LAYER_NAME_MATH_PROBLEM_ORIGIN: {
                "custom_class": VisualMathProblemLocation,
                "custom_class_args": {
                    "operator_str": room_operator
                }
            },
            LAYER_NAME_WALLS: {
                "hit_box_algorithm": "None",
                "use_spatial_hash": True
            },
            LAYER_NAME_FALLING_TILE: {
                "custom_class": FallingTile,
                "custom_class_args": {
                }
            }
        }

        # Make the scene using the inherited method
        self.scene = self.make_scene(map_name, room_operator, layer_options)

        # self.scene.add_sprite_list(LAYER_NAME_FALLING_TILE)

        # Set up the falling tiles
        for tile in self.scene.get_sprite_list(LAYER_NAME_FALLING_TILE):
            tile.setup(self.scene)

        for prob in self.scene.get_sprite_list(LAYER_NAME_MATH_PROBLEM_ORIGIN):
            assert (isinstance(prob, VisualMathProblemLocation))
            prob.setup(self.scene)
            self.problem_list.append(prob.vmp)

        self.score = 0
        if self.problem_list is not None:
            self.max_score = len(self.problem_list)
        else:
            self.max_score = 0

        home_door = Door("home")
        home_door.setCoordinates(500, 500)
        home_door.setTargetPlayerCoordinates(400, 330)
        self.scene.add_sprite(LAYER_NAME_DOORS, home_door)
