"""
Designed to make file mananging easier. This is just the division room setup function.
It might make more sense to make this a class that contains all of the necessary components of this specific room.
"""
from constant import *
from door import Door


def setupDivisionRoom(self):
    map_name = "maps/Grass-Area.tmx"
    room_operator = "/"
    self.is_falling_tile_map = False

    # Custom map options
    layer_options = {

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