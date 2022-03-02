import imp
import arcade
import random
import operator

from numpy import isin

from constant import *


class NumberBlock(arcade.Sprite):
    """
    A sprite that draws itself as a crate with its stored value as a number on top.
    """

    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.texture = arcade.load_texture(CRATE_BLUE_PATH)
        self.scale = TILE_SCALING
        # self.draw()

    def update_animation(self, delta_time: float = 1 / 60):
        # Draw this block's numeric value on top of this sprite.
        arcade.draw_text(
            f"{self.value}",
            start_x=self.center_x,
            start_y=self.center_y,
            color=arcade.color.WHITE,
            font_size=18 * TILE_SCALING,
            width=int(self.width),
            align="center",
            font_name="calibri",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

    def move_to(self, x, y):
        """
        This only exists for the purpose of polymorphism - to be synonymous with NumberBlockGroup,
        which has the same function.
        """
        self.center_x = x
        self.center_y = y


class NumberBlockGroup:
    """
    One or more (probably up to 3) NumberBlocks that represent a single value.
    """

    def __init__(self, x=0, y=0, blocks=None, from_number=None):
        if from_number is None:
            self._blocks = blocks
            self.value = self._compute_value()
        else:
            assert (blocks is None)
            self.value = int(from_number)
            self._blocks = self._make_blocks_from_number()
        self.center_x = x
        self.center_y = y
        self.sprite_list = None

    def _compute_value(self):
        value = 0
        multiplier = 1
        for block in reversed(self._blocks):
            value += block.value * multiplier
            multiplier *= 10
        return value

    def _make_blocks_from_number(self):
        finished = False
        multiplier = 1
        temp_val = self.value
        blocks = []
        while not finished:
            single_digit = int(((temp_val % (multiplier * 10)) - (temp_val % multiplier)) / multiplier)
            blocks.insert(0, NumberBlock(single_digit))
            multiplier *= 10
            if temp_val // multiplier == 0:
                finished = True

        return blocks

    def place_left(self, number_block):
        self._blocks.insert(0, number_block)
        self._update_value()

    def place_right(self, number_block):
        self._blocks.append(number_block)
        self._update_value()

    def _update_value(self):
        self.value = self._compute_value()

    def draw(self, sprite_list=None):
        """
        Just to clarify, this is not overriding a built-in arcade draw() function.
        It just tells each NumberBlock in the list where to place itself and which texture to use.
        """
        # Checks to ensure we already have a sprite_list for this object.
        if sprite_list is None:
            assert(self.sprite_list is not None)
        # Stores a sprite_list into this object the first time it's called.
        else:
            self.sprite_list = sprite_list

        for block in self._blocks:
            self.sprite_list.append(block)

    def _update_locations(self):
        for index, block in enumerate(self._blocks):
            offset =  index * TILE_SIZE * TILE_SCALING * 2
            block.center_x = self.center_x + offset
            block.center_y = self.center_y
            print(f"block {block.value}: ({block.center_x}, {block.center_y}) - offset: {offset}")

    def move_to(self, x, y):
        """
        Use this when trying to move the block group rather than editing center_x
        and center_y directly. This ensures the child blocks get moved along properly
        as well.
        """
        self.center_x = x
        self.center_y = y
        self._update_locations()

    def get_size(self):
        return len(self._blocks)


class SimpleMathProblem:
    """
    Represents a math problem consisting of two operands - lhs and rhs (left-hand side
    and right-hand side) - an operation to be performed on them, and the result of the
    operation.
    """

    def __init__(self, min_value=1, max_value=10):
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        self.min_value = min_value
        self.max_value = max_value
        self.lhs = random.randint(self.min_value, self.max_value)
        self.rhs = random.randint(self.min_value, self.max_value)
        self.operator = self.get_random_operator()
        self.answer = self.get_answer()

    def get_random_operator(self):
        return random.choice(list(self.operators.keys()))

    def get_answer(self):
        answer = self.operators[self.operator](self.lhs, self.rhs)
        return answer


def get_clean_problem():
    """
    Quick and Dirty method for getting a nice and pretty math problem; i.e., one
    where the answer comes out to an integer, not a decimal.
    """
    prob = None
    valid = False
    while not valid:
        prob = SimpleMathProblem()
        if isinstance(prob.answer, int):
            valid = True
        elif isinstance(prob.answer, float) and prob.answer.is_integer():
            valid = True

    return prob


class VisualMathProblem:
    """
    Represents a collection of sprites representing a math problem. Operators, operands, and
    the result are all represented.
    """

    def __init__(self, scene, center_x=0, center_y=0):
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y

        self.problem = get_clean_problem()
        self.lhs = NumberBlockGroup(self.center_x, self.center_y, from_number=self.problem.lhs)
        self.rhs = NumberBlockGroup(self.center_x + (4 * TILE_SIZE), self.center_y, from_number=self.problem.rhs)
        self.answer = NumberBlockGroup(self.center_x + (8 * TILE_SIZE), self.center_y,
                                       from_number=int(self.problem.answer))
        self.equals = NumberBlock("=")
        self.operator = NumberBlock(str(self.problem.operator))

        self.draw_order = [self.lhs, self.operator, self.rhs, self.equals, self.answer]

    def draw(self):
        sprite_list = self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        self.lhs.draw(sprite_list)
        self.rhs.draw(sprite_list)
        self.answer.draw(sprite_list)
        sprite_list.append(self.equals)
        sprite_list.append(self.operator)

        x = self.center_x
        y = self.center_y
        space = TILE_SIZE * TILE_SCALING
        for chunk in self.draw_order:
            size = 1
            if isinstance(chunk, NumberBlockGroup):
                size = chunk.get_size()
            chunk.move_to(x, y)

            # Move over to the next space
            x += space * size + space

            print(f"chunk {chunk.value}: ({chunk.center_x}, {chunk.center_y})")
