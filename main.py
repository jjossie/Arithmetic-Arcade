import arcade
from FallingTileStuff.falling_tile import FallingTile
from numbers_and_math import VisualMathProblem, NumberBlock, VisualMathProblemLocation
from pyglet.math import Vec2
from math import sqrt
from constant import *
from numbers_and_math import VisualMathProblem
from pyglet.math import Vec2
import constant
from player import Player
from page import Page


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Our scene object
        self.exit_list = None
        self.problem = None
        self.scene = None
        self.player = Player(self)
        self.page = Page(self)

        # Some game status/logic
        self.is_falling_tile_map = False
        self.score = None
        self.max_score = None
        self.problem_list = []

        # Load Textures
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_02.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_11.png"))

        # Our physics engine
        self.physics_engine = None
        # Game Logic
        self.map_index = 0  # Index representing which map within global MAPS we're loading for this level.
        self.tile_map = None  # This will hold the actual TileMap object loaded from the .tmx file

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the current map/scene/stage/level here. Call this function to restart the game.
        The map file must be loaded first, then the scene object can be initialized from that.
        Then the player sprite can be loaded and added to the scene afterward so that they draw
        in the proper order.
        """
        self.is_falling_tile_map = False
        # Load the Tiled Map
        layer_options = {
            LAYER_NAME_MATH_PROBLEM_ORIGIN: {
                "custom_class": VisualMathProblemLocation
            },
            LAYER_NAME_WALLS: {
                "hit_box_algorithm": "None",
                "use_spatial_hash": True
            },
            # This will only be needed when we're doing a falling tile room.
            # LAYER_NAME_FALLING_TILE: {
            #     "custom_class": FallingTile,
            #     "custom_class_args": {
            #     }
            # }
        }
        self.tile_map = arcade.load_tilemap(MAPS[self.map_index], TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        self.exit_list = arcade.SpriteList()

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

        # Game Logic
        self.score = 0
        if self.problem_list is not None:
            self.max_score = len(self.problem_list)
        else:
            self.max_score = 0


    def setupFallingTileRoom(self):
        """
            Set up the FallingTileRoom map/scene/stage/level here.
        """
        map_name = "maps/falling-tile-demo.tmx"
        self.is_falling_tile_map = True

        # Custom map options
        layer_options = {
            LAYER_NAME_FALLING_TILE: {
                "custom_class": FallingTile,
                "custom_class_args": {
                }
            }
        }

        # Load tile_map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # repeat line 91 and line 88
        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)
        self.scene.add_sprite_list(LAYER_NAME_PAGE)

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        self.scene.add_sprite(LAYER_NAME_PAGE, self.page)
        # self.scene.add_sprite("Player", self.player_sprite)
        self.exit_list = arcade.SpriteList()
        # self.scene.add_sprite("castle", self.castle_sprite)

        self.exit_list = arcade.SpriteList()

        for tile in self.scene.get_sprite_list(LAYER_NAME_FALLING_TILE):
            tile.setup(self.scene)

        problems = [
            VisualMathProblem(self.scene, 235, 1055, 1, 10, operator_str="-"),

        ]
        for problem in problems:
            problem.draw()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, [
                self.scene.get_sprite_list(LAYER_NAME_WALLS),
                self.scene.get_sprite_list(LAYER_NAME_NUMBER)
            ]
        )

    def player_hit_door(self):
        collisions = arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list(LAYER_NAME_EXIT))
        if len(collisions) > 0:
            self.map_index += 1
            self.setup()
            print("We hit a door to advance to next level")

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Use the main camera for the scene
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Draw Math Layer
        self.scene.get_sprite_list(LAYER_NAME_NUMBER).update_animation()

        # Use the GUI Camera for the score and stuff
        self.gui_camera.use()
        self.draw_score()
        self.caption()

    def on_update(self, delta_time):

        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        self.player_hit_door()

        # Update the player object
        self.player.update()
        self.page.update()

        # Call update on the fallable tiles in the scene if necessary
        if self.is_falling_tile_map:
            for tile in self.scene.get_sprite_list(LAYER_NAME_FALLING_TILE).sprite_list:
                print("falling tile being updated")
                tile.update()


    def update_score(self):
        temp_score = 0
        for problem in self.problem_list:
            assert(isinstance(problem, VisualMathProblem))
            if problem.is_solved():
                temp_score += 1
        self.score = temp_score
        
    def is_level_complete(self) -> bool:
        return self.score >= self.max_score

    def draw_score(self):
        if self.max_score > 0: # Make sure we don't display score on a level without one (the main area)
            percentage = int(self.score / self.max_score * 100)
            arcade.draw_text(
                text=f"Problems Completed: {self.score}/{self.max_score} ({percentage}%)",
                start_x = 100,
                start_y = 100,
                font_size=25,
                bold=True
            )

    def on_key_press(self, symbol: int, modifiers: int):
        self.player.on_key_press(symbol, modifiers)
        self.page.on_key_press(symbol, modifiers)
        

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.on_key_release(symbol, modifiers)

    def caption(self):
        """This Function is to display the caption when it touches the boxes"""

        cap = "Press Space to lift it up"

        arcade.draw_text(
            cap,
            # self.view_left + SCREEN_WIDTH * 0.3,
            # self.view_bottom + SCREEN_HEIGHT * 0.8,
            start_x=SCREEN_HEIGHT / 2,
            start_y=SCREEN_HEIGHT / 2,
            color=arcade.csscolor.WHITE,
            font_size=30
        )
 
    def scroll_to_player(self):

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

        # Scroll to the proper location
        position = Vec2(self.view_left, self.view_bottom)
        self.camera.move_to(position, CAMERA_SPEED)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    # Christian's version
    # window.setupFallingTileRoom()
    arcade.run()


if __name__ == "__main__":
    main()
