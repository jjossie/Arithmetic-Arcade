import imp
import arcade

from constant import *


class Player(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Load Textures
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_08.png"))  # Up
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))  # Down
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))  # Left
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_17.png"))  # Right

        # Set up the player, specifically placing it at these coordinates.
        self.center_x = 500
        self.center_y = 375
        self.scale = CHARACTER_SCALING
        self.texture = PLAYER_TEXTURES[0]

    def setup(self):
        """
        Set up this player sprite. Not currently being used for anything since everything is
        initialized in __init__, but this is here in case we need it.
        """

    def update_player_speed(self):

        # Calculate speed base on keys pressed
        self.change_x = 0
        self.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.change_x = PLAYER_MOVEMENT_SPEED

        # This does not allow the player go over
        if self.center_x < (VIEWPORT_MARGIN * 6 / 5):
            if self.center_x <= (VIEWPORT_MARGIN / 10):
                self.center_x = (VIEWPORT_MARGIN / 10)
        else:
            self.window.scroll_to_player()
        if self.center_y < (VIEWPORT_MARGIN * 1.2):
            if self.center_y <= (VIEWPORT_MARGIN / 10):
                self.center_y = (VIEWPORT_MARGIN / 10)
        else:
            self.window.scroll_to_player()
        if self.center_x > (MAP_SIZE - VIEWPORT_MARGIN * 0.8):
            if self.center_x >= (MAP_SIZE + 20):
                self.center_x = (MAP_SIZE + 20)
        else:
            self.window.scroll_to_player()
        if self.center_y > (MAP_SIZE - VIEWPORT_MARGIN * 0.8):
            if self.center_y >= (MAP_SIZE + VIEWPORT_MARGIN / 5):
                self.center_y = (MAP_SIZE + VIEWPORT_MARGIN / 5)
        else:
            self.window.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called by the arcade.Window object whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called by the arcade.Window object when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def texture_update(self):
        """Textures changed by directions"""

        if self.up_pressed:
            self.texture = PLAYER_TEXTURES[0]
        if self.down_pressed:
            self.texture = PLAYER_TEXTURES[1]
        if self.left_pressed:
            self.texture = PLAYER_TEXTURES[2]
        if self.right_pressed:
            self.texture = PLAYER_TEXTURES[3]
