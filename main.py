import arcade
from pyglet.math import Vec2


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
SCREEN_TITLE = "RUNTIME TERROR"
MAP = ""
MAP_SIZE = 1550

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

CAMERA_SPEED = 0.1
VIEWPORT_MARGIN = 200

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.75
TILE_SCALING = 1

MAPS = [
    # "maps/joel-demo.tmx",
    "maps/Main-Spawn.tmx"
]

PLAYER_IMAGE_PATH = ":resources:images/animated_characters/male_person/malePerson_idle.png"

LAYER_NAME_WALLS = "walls"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_PLAYER = "player"

PLAYER_TEXTURES = []


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Our scene object
        self.scene = None

        # Load Textures
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_02.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_11.png"))

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Our physics engine
        self.physics_engine = None

        # Game Logic
        self.map_index = 0  # Index representing which map within global MAPS we're loading for this level.
        self.tile_map = None  # This will hold the actual TileMap object loaded from the .tmx file

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the current map/scene/stage/level here. Call this function to restart the game.
        The map file must be loaded first, then the scene object can be initialized from that.
        Then the player sprite can be loaded and added to the scene afterward so that they draw
        in the proper order.
        """

        # Load the Tiled Map
        layer_options = {}
        self.tile_map = arcade.load_tilemap(MAPS[self.map_index], TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)

        # Set up the player, specifically placing it at these coordinates.

        self.player_sprite = arcade.Sprite("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 375
        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)


        # # Create the ground
        # # This shows using a loop to place multiple sprites horizontally
        # for x in range(0, 1250, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png", TILE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.scene.add_sprite("Walls", wall)
            
        # self.player_sprite = arcade.Sprite(PLAYER_IMAGE_PATH, CHARACTER_SCALING)
        # self.player_sprite.center_x = 500
        # self.player_sprite.center_y = 375
        # self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_WALLS),
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our Scene
        self.scene.draw()

        self.camera.use()

    def update_player_speed(self):

        # Calculate speed base on keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        
        if self.up_pressed and not self.down_pressed:

            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

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

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        self.texture_update()

    def texture_update(self):
        """Textures changed by directions"""

        if self.up_pressed:
            self.player_sprite.texture = PLAYER_TEXTURES[0]
        if self.down_pressed:
            self.player_sprite.texture = PLAYER_TEXTURES[1]
        if self.left_pressed:
            self.player_sprite.texture = PLAYER_TEXTURES[2]
        if self.right_pressed:
            self.player_sprite.texture = PLAYER_TEXTURES[3]

        if self.player_sprite.center_x < (VIEWPORT_MARGIN*6/5):
            if self.player_sprite.center_x <= (VIEWPORT_MARGIN/10):    
                self.player_sprite.center_x = (VIEWPORT_MARGIN/10)
        elif self.player_sprite.center_y < (VIEWPORT_MARGIN*1.2):
            if self.player_sprite.center_y <= (VIEWPORT_MARGIN/10):    
                self.player_sprite.center_y = (VIEWPORT_MARGIN/10)
        elif self.player_sprite.center_x > (MAP_SIZE-VIEWPORT_MARGIN*0.8):
            if self.player_sprite.center_x >= (MAP_SIZE+20):
                self.player_sprite.center_x = (MAP_SIZE+20)
        elif self.player_sprite.center_y > (MAP_SIZE - VIEWPORT_MARGIN*0.8):
            if self.player_sprite.center_y >= (MAP_SIZE + VIEWPORT_MARGIN/5):
                self.player_sprite.center_y = (MAP_SIZE + VIEWPORT_MARGIN/5)    
        else:
            self.scroll_to_player()
            

        
        

    def scroll_to_player(self):

         # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera.move_to(position, CAMERA_SPEED)



        # position = Vec2(self.player_sprite.center_x - self.width / 2,
        #                 self.player_sprite.center_y - self.height / 2)
        # self.camera.move_to(position, CAMERA_SPEED)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
