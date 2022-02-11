import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
SCREEN_TITLE = "RUNTIME TERROR"
MAP = ""

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5 

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.75
TILE_SCALING = 0.5

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
        PLAYER_TEXTURES.append(arcade.load_texture("assets\kenney_sokobanpack\PNG\Default size\Player\player_02.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets\kenney_sokobanpack\PNG\Default size\Player\player_05.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets\kenney_sokobanpack\PNG\Default size\Player\player_20.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets\kenney_sokobanpack\PNG\Default size\Player\player_11.png"))

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite("assets\kenney_sokobanpack\PNG\Default size\Player\player_05.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 375
        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)


        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)
        
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
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


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()