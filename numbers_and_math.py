import random
import operator
from enum import Enum
import copy
from constant import *


class NumberBlockHitbox(arcade.Sprite):
    def __init__(self, parent_block):
        super().__init__(TRANSPARENT_BOX_PATH,
                         scale=NUMBER_BLOCK_SCALING * 1.1,
                         hit_box_algorithm="None",  # This is important
                         center_x=parent_block.center_x,
                         center_y=parent_block.center_y)
        self.parent_block = parent_block


class BlockGroupPosition(Enum):
    """
    Stores the file suffixes for the images representing relative block positions.
    So like left/right/standalone/middle. I don't know man just look at the values
    """
    LEFT = "leftend"
    RIGHT = "rightend"
    MIDDLE = "middle"
    STANDALONE = "edit"


class BlockType(Enum):
    """
    Determines whether the block is movable, immovable, correct, etc. Basically
    the block's status.
    """
    MOVABLE = "crate_44"
    IMMOVABLE = "crate_42"
    CORRECT = "crate_45"
    INCORRECT = "crate_43"
    OPERATION = "crate_01"


class NumberBlock(arcade.Sprite):
    """
    A sprite that draws itself as a crate with its stored value as a number on top.
    """

    def __init__(self, scene, value):
        super().__init__()
        assert (value is not None and scene is not None)
        self.value = value
        self.scene = scene

        # This determines whether it is movable, immovable, etc.
        self.block_type = BlockType.MOVABLE
        # This determines whether it is a left, right, middle, or standalone block.
        self.block_group_position: BlockGroupPosition = BlockGroupPosition.STANDALONE
        self.configure_texture()
        self.scale = NUMBER_BLOCK_SCALING
        self._hit_box_algorithm = "None"
        # A reference to a TargetLocation that this block might be placed on
        self.target_location = None
        # Auxiliary sprites. One for the hitbox, another for the number/symbol.
        self.hit_box_sprite = NumberBlockHitbox(self)
        self.symbol_sprite = arcade.Sprite(self._get_symbol_path(),
                                           scale=NUMBER_SCALING,
                                           hit_box_algorithm="None")

        # Add myself to a sprite list
        scene.get_sprite_list(LAYER_NAME_NUMBER).append(self)
        # Add my hit box sprite to the other one
        scene.get_sprite_list(LAYER_NAME_NUMBER_HITBOX).append(self.hit_box_sprite)
        # And finally, add my symbol sprite list to that top layer
        scene.get_sprite_list(LAYER_NAME_NUMBER_SYMBOLS).append(self.symbol_sprite)

    def move_to(self, x, y):
        """
        Use this to move a NumberBlock rather than setting center_x and center_y directly.
        Moves the sprite along with its accompanying hit box and symbol sprites.
        This also exists for the purpose of polymorphism - to be synonymous with NumberBlockGroup,
        which has the same function.
        """
        self.center_x = x
        self.center_y = y
        self.hit_box_sprite.center_x = x
        self.hit_box_sprite.center_y = y
        self.symbol_sprite.center_x = x
        self.symbol_sprite.center_y = y

    def auto_move(self):
        collision_list = arcade.check_for_collision_with_list(self,
                                                              self.scene.get_sprite_list(LAYER_NAME_NUMBER_TARGETS))
        if len(collision_list) != 0:  # Player dropped the block on top of a Target Location
            assert (isinstance(collision_list[0], TargetLocation))
            self.target_location = pick_nearest_collision(self, collision_list)
            self.target_location.place_number_block(self)
        else:  # Player dropped the block out in the open
            if self.target_location is not None:
                self.target_location.clear_number_block()

    def set_block_type(self, block_type: BlockType):
        self.block_type = block_type
        self.configure_texture()

    def set_block_group_position(self, pos: BlockGroupPosition):
        self.block_group_position = pos
        self.configure_texture()

    def configure_texture(self):
        path = f"{CRATE_BASE_PATH}{self.block_type.value}{self.block_group_position.value}{IMG_PATH_EXT}"
        # print(path)  # For debugging purposes
        self.texture = arcade.load_texture(path)

    def _get_symbol_path(self):
        filename = ""
        if self.value == "+":
            filename = "add"
        elif self.value == "/":
            filename = "divide2"
        elif self.value == "-":
            filename = "subtract"
        elif self.value == "*":
            filename = "multiply"
        elif self.value == "=":
            filename = "equals"
        else:
            filename = self.value
        return f"{NUM_BASE_PATH}{filename}{IMG_PATH_EXT}"

    def __str__(self):
        return super.__str__(self) + f"\nNumberBlock Val: {self.value} \nSpriteList: {self.sprite_lists}" \
               + f"\n{self._points}\n\n"


class NumberBlockGroup:
    """
    One or more (probably up to 3) Blocks that represent a single value.
    Will be made out of NumberBlocks (which are movable) by default, but
    can also be made as TargetLocations.
    """

    def __init__(self, block_template=NumberBlock, scene=None, x=0, y=0, blocks=None, from_number=None):
        assert (scene is not None)
        self.scene = scene
        self.center_x = x
        self.center_y = y
        self.block_template = block_template
        if from_number is None:
            self._blocks = blocks
            self.value = self._compute_value()
        else:
            assert (blocks is None)
            try:
                self.value = int(from_number)
            except ValueError:
                self.value = from_number
            self._blocks = self._make_blocks_from_number()

    def _compute_value(self):
        value = 0
        multiplier = 1
        for block in reversed(self._blocks):
            value += block.value * multiplier
            multiplier *= 10
        return value

    def _make_blocks_from_number(self):
        blocks = []
        temp_val = self.value

        if isinstance(temp_val, str):
            blocks.append(self.block_template(self.scene, temp_val))
        else:
            assert (temp_val >= 0)
            finished = False
            multiplier = 1
            while not finished:
                single_digit = int(((temp_val % (multiplier * 10)) - (temp_val % multiplier)) / multiplier)
                blocks.insert(0, self.block_template(self.scene, single_digit))
                multiplier *= 10
                if temp_val // multiplier == 0:
                    finished = True

        return blocks

    def place_left(self, number_block):
        self._blocks.insert(0, number_block)
        self._update_value()
        self._update_textures()

    def detach_right(self) -> NumberBlock:
        return self._blocks.pop()

    def place_right(self, number_block):
        self._blocks.append(number_block)
        self._update_value()
        self._update_textures()

    def _update_value(self):
        self.value = self._compute_value()

    def _update_locations(self):
        """
        Sets the locations of each block in the NumberBlockGroup so they draw
        next to each other properly.
        """
        for index, block in enumerate(self._blocks):
            offset = index * TILE_SIZE * TILE_SCALING
            block.move_to(self.center_x + offset, self.center_y)

    def _update_textures(self):
        """
        Updates the block_group_position property of each NumberBlock in the group
        so they appear as a single number rather than separate digits.
        """
        if self.block_template == NumberBlock:
            for index, block in enumerate(self._blocks):
                size = self.get_size()
                if size == 1:
                    block.set_block_group_position(BlockGroupPosition.STANDALONE)
                else:
                    if index == 0:
                        block.set_block_group_position(BlockGroupPosition.LEFT)
                    elif index == size - 1:
                        block.set_block_group_position(BlockGroupPosition.RIGHT)
                    else:
                        block.set_block_group_position(BlockGroupPosition.MIDDLE)

    def set_block_type(self, block_type: BlockType):
        if self.block_template == NumberBlock:
            for block in self._blocks:
                block.set_block_type(block_type)

    def move_to(self, x, y):
        """
        Use this when trying to move the block group rather than editing center_x
        and center_y directly. This ensures the child blocks get moved along properly
        as well.
        """
        self.center_x = x
        self.center_y = y
        self._update_locations()
        self._update_textures()

    def get_size(self):
        return len(self._blocks)

    def is_correct(self):
        assert (self.block_template == TargetLocation)
        for target in self._blocks:
            assert (isinstance(target, TargetLocation))
            if not target.is_correct():
                return False
        return True

    def log(self):
        for block in self._blocks:
            print(str(block))


class TargetLocation(arcade.Sprite):
    """
    A sprite that draws the target locations
    """

    def __init__(self, scene, expected_value):
        super().__init__()

        self.texture = arcade.load_texture(TARGET_BOX)
        self.scale = NUMBER_BLOCK_SCALING
        self.expected_value = expected_value
        self.number_attempt = None
        scene.get_sprite_list(LAYER_NAME_NUMBER_TARGETS).append(self)

    def move_to(self, x, y):
        """
        Use this to move a TargetLocation rather than setting center_x and center_y directly.
        This also exists for the purpose of polymorphism - to be synonymous with NumberBlockGroup,
        which has the same function.
        """
        self.center_x = x
        self.center_y = y

    # Check if the player got the answer right
    def is_correct(self):
        if self.number_attempt is None:
            return False
        if self.number_attempt.value == self.expected_value:
            return True
        else:
            # If we wanted to keep track of failed attempts for a score, this would be where we'd do it
            return False

    def place_number_block(self, block: NumberBlock):
        # Try to snap in the NumberBlock
        if self.number_attempt is None:
            block.move_to(self.center_x, self.center_y)
            self.number_attempt = block

            if self.is_correct():
                self.number_attempt.set_block_type(BlockType.CORRECT)
            else:
                # If we wanted to keep track of failed attempts for a score, this would be where we'd do it
                self.number_attempt.set_block_type(BlockType.INCORRECT)
        else:
            pass

    def clear_number_block(self):
        self.number_attempt = None


class SimpleMathProblem:
    """
    Represents a math problem consisting of two operands - lhs and rhs (left-hand side
    and right-hand side) - an operation to be performed on them, and the result of the
    operation.
    """

    def __init__(self, min_value=1, max_value=10, operator_str=None):
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        finished = False
        while not finished:
            self.setup(operator_str)
            if self.answer >= 0:
                # Could be a decimal, but get_clean_problem() should take care of that
                finished = True

    def setup(self, operator_str):
        self.min_value = 1
        self.max_value = 10
        self.lhs = random.randint(self.min_value, self.max_value)
        self.rhs = random.randint(self.min_value, self.max_value)
        if operator_str is None:
            self.operator = self.get_random_operator()
        else:
            print(operator_str)
            assert (operator_str in self.operators.keys())
            self.operator = operator_str
        self.answer = self.get_answer()

    def get_random_operator(self):
        return random.choice(list(self.operators.keys()))

    def get_answer(self):
        answer = self.operators[self.operator](self.lhs, self.rhs)
        return answer


def get_clean_problem(min=None, max=None, operator_str=None):
    """
    Quick and Dirty method for getting a nice and pretty math problem; i.e., one
    where the answer comes out to an integer, not a decimal.

    ***** I'm pretty sure this is what's causing the occasional crash-on-startup bug *****
    """
    prob = None
    valid = False
    while not valid:
        prob = SimpleMathProblem(min, max, operator_str)
        if isinstance(prob.answer, int):
            valid = True
        elif isinstance(prob.answer, float) and prob.answer.is_integer():
            prob.answer = int(prob.answer)
            valid = True

    return prob


class VisualMathProblem:
    """
    Represents a collection of sprites representing a math problem. Operators, operands, and
    the result are all represented.
    """

    def __init__(self, scene, center_x=0, center_y=0, min=None, max=None, operator_str=None):
        """
        Params:
        :operator_str: a string with a math operator. Either "+", "-", "*", or "/".
        """
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y
        self.sprite_list = self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        self.problem = get_clean_problem(min, max, operator_str)

        # Number Block Groups
        self.lhs = NumberBlockGroup(scene=self.scene, from_number=self.problem.lhs)
        # self.lhs_target = TargetLocation(scene=self.scene, x=100)

        self.operator = NumberBlockGroup(scene=self.scene, from_number=str(self.problem.operator))
        # self.operator_target = TargetLocation(scene=self.scene, x=400)

        self.rhs = NumberBlockGroup(scene=self.scene, from_number=self.problem.rhs)
        # self.rhs_target = TargetLocation(scene=self.scene, x=700)

        self.equals = NumberBlockGroup(scene=self.scene, from_number="=")
        # self.equals_target = TargetLocation(scene=self.scene, x=1000)



        self.answer_target = NumberBlockGroup(block_template=TargetLocation, scene=self.scene,
                                              from_number=self.problem.answer)

        self.answer_blocks = NumberBlockGroup(block_template=NumberBlock, scene=self.scene,
                                              from_number=self.problem.answer)

        self.movable_blocks = self.answer_blocks._blocks

        for i in range(0, 5):
            self.movable_blocks.append(NumberBlock(scene=self.scene, value=random.randint(0, 9)))

        # Configure The Problem
        self.lhs.set_block_type(BlockType.IMMOVABLE)
        self.rhs.set_block_type(BlockType.IMMOVABLE)
        self.operator.set_block_type(BlockType.OPERATION)
        self.equals.set_block_type(BlockType.OPERATION)
        for block in self.movable_blocks:
            block.set_block_type(BlockType.MOVABLE)
        # self.answer_target.set_block_type(BlockType.MOVABLE)

        self.draw_order = [self.lhs, self.operator, self.rhs, self.equals, self.answer_target]

        self.answer_range_height = 0
        self.answer_range_width = 400
        self.answer_range_offset = 120
        self.answer_range_x_offset = 320

    def draw(self):
        x = self.center_x
        y = self.center_y
        space = TILE_SIZE * TILE_SCALING
        for chunk in self.draw_order:
            size = chunk.get_size()
            chunk.move_to(x, y)

            # Move over to the next space
            x += space * size + space

        for block in self.movable_blocks:
            block.move_to(
                random.randint(
                    self.center_x - self.answer_range_width // 2,
                    self.center_x + self.answer_range_width // 2
                ) + self.answer_range_x_offset,
                random.randint(
                    self.center_y,
                    self.center_y + self.answer_range_height
                ) + self.answer_range_offset
            )

    def log(self):
        for block in self.draw_order:
            block.log()

    def is_solved(self) -> bool:
        """
        Function will check if the problem has been solved and will return True/False.
        Basically an alias for self.answer_target.is_correct().
        """
        if self.answer_target.is_correct():
            print("correct")
            return True
        else:
            print("incorrect")
            return False


class VisualMathProblemLocation(arcade.Sprite):
    def __init__(self,
                 filename=None,
                 scale=None,
                 image_x=None,
                 image_y=None,
                 image_width=None,
                 image_height=None,
                 center_x=None,
                 center_y=None,
                 flipped_horizontally=None,
                 flipped_vertically=None,
                 flipped_diagonally=None,
                 hit_box_algorithm=None,
                 hit_box_detail=None,
                 texture=None,
                 angle=None,
                 operator_str=None):
        super().__init__()
        self.vmp = None
        self.operator = operator_str

    def setup(self, scene):
        self.vmp = VisualMathProblem(scene, self.center_x, self.center_y, operator_str=self.operator)
        self.vmp.draw()
