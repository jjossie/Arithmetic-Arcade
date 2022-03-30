"""
Designed to make file mananging easier. This is just the addition room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from door import Door
from numbers_and_math import VisualMathProblemLocation, VisualMathProblem


class AdditionRoom:

    def __init__(self):

        # Score logic
        self.is_falling_tile_map = None
        self.score = None
        self.max_score = None
        self.problem_list = []

        self.scene = self.make_scene()

        # Set up the math problems
        for prob in self.scene.get_sprite_list(LAYER_NAME_MATH_PROBLEM_ORIGIN):
            assert (isinstance(prob, VisualMathProblemLocation))
            prob.setup(self.scene)
            self.problem_list.append(prob.vmp)

        # Game Logic
        self.score = 0
        if self.problem_list is not None:
            self.max_score = len(self.problem_list)
        else:
            self.max_score = 0

    def make_scene(self):
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

        # Load tile_map
        tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        scene = arcade.Scene.from_tilemap(tile_map)

        # Create the Sprite lists
        scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
        scene.add_sprite_list(LAYER_NAME_PLAYER)
        scene.add_sprite_list(LAYER_NAME_NUMBER)
        scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
        scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)
        scene.add_sprite_list(LAYER_NAME_DOORS)

        # Sprites to add to lists above

        home_door = Door("home")
        home_door.setCoordinates(500, 500)
        home_door.setTargetPlayerCoordinates(400, 330)
        scene.add_sprite(LAYER_NAME_DOORS, home_door)

        # Create the 'physics engine'
        # self.physics_engine = arcade.PhysicsEngineSimple(
        #     self.player, [
        #         scene.get_sprite_list(LAYER_NAME_WALLS),
        #         scene.get_sprite_list(LAYER_NAME_NUMBER)
        #     ]
        # )

        return scene

    def update_score(self):
        temp_score = 0
        for problem in self.problem_list:
            assert (isinstance(problem, VisualMathProblem))
            if problem.is_solved():
                temp_score += 1
        self.score = temp_score

    def is_level_complete(self) -> bool:
        return self.score >= self.max_score

    def draw_score(self):
        if self.max_score > 0:  # Make sure we don't display score on a level without one (the main area)
            percentage = int(self.score / self.max_score * 100)
            arcade.draw_text(
                text=f"Problems Completed: {self.score}/{self.max_score} ({percentage}%)",
                start_x=100,
                start_y=100,
                font_size=25,
                bold=True
            )
