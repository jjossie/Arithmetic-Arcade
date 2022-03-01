import imp
import arcade
# from main import *

from constant import *

# main_page = MyGame()

class Player(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self.player_sprite = None
        self.window = window

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Load Textures
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_02.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_11.png"))

        # Set up the player, specifically placing it at these coordinates.
        self.scale = CHARACTER_SCALING
        self.texture = PLAYER_TEXTURES[0]
        self.center_x = 500
        self.center_y = 375
        # self.player_list.append(self)
        

        def setup(self):
            """Set up the current map/scene/stage/level here. Call this function to restart the game.
        The map file must be loaded first, then the scene object can be initialized from that.
        Then the player sprite can be loaded and added to the scene afterward so that they draw
        in the proper order.
        """

        # Set up the player, specifically placing it at these coordinates.

        self = arcade.Sprite("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png",
                                           CHARACTER_SCALING)
        self.center_x = 500
        self.center_y = 375
        # self.player_list.append(self)
        

        


    
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


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        print("key pressed")

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_speed()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

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

                # This does not allow the player go over
        if self.center_x < (VIEWPORT_MARGIN*6/5):
            if self.center_x <= (VIEWPORT_MARGIN/10):    
                self.center_x = (VIEWPORT_MARGIN/10)
        else:
            self.window.scroll_to_player()
        if self.center_y < (VIEWPORT_MARGIN*1.2):
            if self.center_y <= (VIEWPORT_MARGIN/10):    
                self.center_y = (VIEWPORT_MARGIN/10)
        else:
            self.window.scroll_to_player()
        if self.center_x > (MAP_SIZE-VIEWPORT_MARGIN*0.8):
            if self.center_x >= (MAP_SIZE+20):
                self.center_x = (MAP_SIZE+20)
        else:
            self.window.scroll_to_player()
        if self.center_y > (MAP_SIZE - VIEWPORT_MARGIN*0.8):
            if self.center_y >= (MAP_SIZE + VIEWPORT_MARGIN/5):
                self.center_y = (MAP_SIZE + VIEWPORT_MARGIN/5)    
        else:
            self.window.scroll_to_player()

