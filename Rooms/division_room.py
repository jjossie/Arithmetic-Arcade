"""
Designed to make file mananging easier. This is just the division room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from numbers_and_math import VisualMathProblemLocation
from door import Door


def setupDivisionRoom(self):
    map_name = "maps/Grass-Area.tmx"
    room_operator = "/"
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
    self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

    # Initialize Scene from the tilemap
    self.scene = arcade.Scene.from_tilemap(self.tile_map)

    # Create the Sprite lists
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
    self.scene.add_sprite_list(LAYER_NAME_PLAYER)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
    self.scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)
    self.scene.add_sprite_list(LAYER_NAME_DOORS)

    # Sprites to add to lists above
    self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)

    home_door = Door("home")
    home_door.setCoordinates(500, 500)
    home_door.setTargetPlayerCoordinates(600, 330)
    self.scene.add_sprite(LAYER_NAME_DOORS, home_door)


    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEngineSimple(
        self.player, [
            self.scene.get_sprite_list(LAYER_NAME_WALLS),
            self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        ]
    )


    # Set up the math problems
    for prob in self.scene.get_sprite_list(LAYER_NAME_MATH_PROBLEM_ORIGIN):
        assert (isinstance(prob, VisualMathProblemLocation))
        prob.setup(self.scene)
        self.problem_list.append(prob.vmp)
