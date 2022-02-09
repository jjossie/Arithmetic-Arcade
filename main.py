import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
SCREEN_TITLE = "RUNTIME TERROR"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.75
TILE_SCALING = 1

MAPS = [
    "maps/joel-demo.tmx"
]

LAYER_NAME_WALLS = "walls"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_PLAYER = "player"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Our scene object
        self.scene = None

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

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Load the Tiled Map
        layer_options = {}
        self.tile_map = arcade.load_tilemap(MAPS[self.map_index], TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        # self.scene.add_sprite_list(LAYER_NAME_WALLS, use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/male_person/malePerson_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 375
        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_WALLS)
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our Scene
        self.scene.draw()

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

        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
