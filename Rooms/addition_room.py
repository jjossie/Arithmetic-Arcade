"""
Designed to make file mananging easier. This is just the addition room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from door import Door
from numbers_and_math import VisualMathProblemLocation, VisualMathProblem
from Level import Level


class AdditionRoom(Level):

    def __init__(self):
        super().__init__()

        map_name = "maps/Castle-Area.tmx"
        room_operator = "+"
        self.is_falling_tile_map = False

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
        }

        # Make the scene and attach it to this Level
        self.scene = self.make_scene(map_name, room_operator, layer_options)

        # Must be done AFTER scene is fully initialized
        # Set up the math problems
        for prob in self.scene.get_sprite_list(LAYER_NAME_MATH_PROBLEM_ORIGIN):
            assert (isinstance(prob, VisualMathProblemLocation))
            prob.setup(self.scene)
            self.problem_list.append(prob.vmp)

        # Math Problem Logic
        self.score = 0
        if self.problem_list is not None:
            self.max_score = len(self.problem_list)
        else:
            self.max_score = 0

        # Add the doors specific to this map
        home_door = Door("home")
        home_door.setCoordinates(500, 500)
        home_door.setTargetPlayerCoordinates(400, 330)
        self.scene.add_sprite(LAYER_NAME_DOORS, home_door)
