import imp
from enum import Enum
import arcade

from constant import *
from numbers_and_math import NumberBlock, BlockType, NumberBlockHitbox


class PlayerOrientation(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Player(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self._block_position_offset = None
        self.window = window

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False
        self.shift_pressed = False

        self.orientation: PlayerOrientation = PlayerOrientation.DOWN
        self.block = None

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

    def update(self):
        """
        Frame-by-frame logic for the player object. Called by window.on_update().
        """
        self.update_player_speed()
        self.texture_update()
        self.check_for_block_collisions()
        self._move_block()
        if not self.space_pressed:
            self.release_block()

    def update_player_speed(self):
        """
        Calculates speed and moves the player based on which keys are pressed.
        """

        # Calculate speed base on keys pressed
        self.change_x = 0
        self.change_y = 0

        speed = PLAYER_MOVEMENT_SPEED * PLAYER_RUN_MULTIPLIER\
            if self.shift_pressed else PLAYER_MOVEMENT_SPEED

        if self.up_pressed and not self.down_pressed:
            self.change_y = speed
        elif self.down_pressed and not self.up_pressed:
            self.change_y = -speed
        if self.left_pressed and not self.right_pressed:
            self.change_x = -speed
        elif self.right_pressed and not self.left_pressed:
            self.change_x = speed

        # This does not allow the player go over
        # if self.center_x < (VIEWPORT_MARGIN * 6 / 5):
        #     if self.center_x <= (VIEWPORT_MARGIN / 10):
        #         self.center_x = (VIEWPORT_MARGIN / 10)
        # else:
        #     self.window.scroll_to_player()
        # if self.center_y < (VIEWPORT_MARGIN * 1.2):
        #     if self.center_y <= (VIEWPORT_MARGIN / 10):
        #         self.center_y = (VIEWPORT_MARGIN / 10)
        # else:
        #     self.window.scroll_to_player()
        # if self.center_x > (MAP_SIZE - VIEWPORT_MARGIN * 0.8):
        #     if self.center_x >= (MAP_SIZE + 20):
        #         self.center_x = (MAP_SIZE + 20)
        # else:
        #     self.window.scroll_to_player()
        # if self.center_y > (MAP_SIZE - VIEWPORT_MARGIN * 0.8):
        #     if self.center_y >= (MAP_SIZE + VIEWPORT_MARGIN / 5):
        #         self.center_y = (MAP_SIZE + VIEWPORT_MARGIN / 5)
        # else:
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
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = True

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
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = False

    def texture_update(self):
        """Change the player's texture based on Orientation."""

        if self.up_pressed:
            self.orientation = PlayerOrientation.UP
        if self.down_pressed:
            self.orientation = PlayerOrientation.DOWN
        if self.left_pressed:
            self.orientation = PlayerOrientation.LEFT
        if self.right_pressed:
            self.orientation = PlayerOrientation.RIGHT
        self.texture = PLAYER_TEXTURES[self.orientation.value]

    def grab_block(self, block: NumberBlock):
        """
        Grab a given NumberBlock if it is movable. This will set the
        relative block offset at the moment the player grabbed it.
        """
        if block.block_type == BlockType.MOVABLE \
                or block.block_type == BlockType.INCORRECT:
            self.block = block
            self._block_position_offset = self._get_block_position_offset()

    def release_block(self):
        """
        Let go of whatever block the player is holding by setting self.block to None.
        Called every time the space bar is released.
        """
        self.block = None

    def check_for_block_collisions(self):
        """
        This is the function that checks if this (the player object) is colliding
        with the hitboxes of any NumberBlocks. It also handles displaying the caption.
        """
        if self.block is None:
            blocks = arcade.check_for_collision_with_list(self, self.window.scene.get_sprite_list(LAYER_NAME_NUMBER_HITBOX))
            if len(blocks) != 0:
                assert(isinstance(blocks[0], NumberBlockHitbox))
                block = blocks[0].parent_block
                # Make sure this block is actually a NumberBlock
                assert(isinstance(block, NumberBlock))
                if self.space_pressed:
                    self.grab_block(block)
                else:
                    self.window.caption()

    def _move_block(self):
        """
        Move the held block along with the player based on an offset relative
        to the player's position.
        This is called by self.update() every frame to ensure the block
        the player is grabbing gets moved along with the player.
        """
        if self.block is not None:
            self.block.move_to(
                self.center_x + self._block_position_offset[0],
                self.center_y + self._block_position_offset[1]
            )

    def _get_block_position_offset(self):
        """
        Determine the position offset for the block relative to the player for
        a given instant in time.
        """
        assert(self.block is not None)
        offset_x = self.block.center_x - self.center_x
        offset_y = self.block.center_y - self.center_y
        offset = 1
        if self.orientation == PlayerOrientation.UP:
            offset_y += offset
        elif self.orientation == PlayerOrientation.DOWN:
            offset_y -= offset
        elif self.orientation == PlayerOrientation.LEFT:
            offset_x -= offset
        else:
            # Assume facing right
            offset_x += offset
        return offset_x, offset_y
