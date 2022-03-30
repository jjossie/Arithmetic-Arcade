"""
Parent class for all levels
"""
from constant import *
from door import Door
from numbers_and_math import VisualMathProblemLocation, VisualMathProblem


class Level:

    def __init__(self):

        # Score logic
        self.is_falling_tile_map = None
        self.score = None
        self.max_score = None
        self.problem_list = []

    def make_scene(self, map_name, room_operator, layer_options):

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

        return scene

    def update_score(self):
        print("Updating score at the Level levelW")
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
