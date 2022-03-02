import arcade
import random
import operator

TILE_SCALING = 1

LAYER_NAME_NUMBER = "Numbers"

CRATE_BLUE_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_09.png"
CRATE_BROWN_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_07.png"
TILE_SIZE = 32


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
        self.x = x
        self.y = y

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

    def draw(self, sprite_list):
        for index, block in enumerate(self._blocks):
            sprite_list.append(block)
            block.center_x = self.x + (TILE_SIZE * (index + 1) * 2) * TILE_SCALING
            block.center_y = self.y


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

    def draw(self):
        sprite_list = self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        self.lhs.draw(sprite_list)
        self.rhs.draw(sprite_list)
        self.answer.draw(sprite_list)
        sprite_list.append(self.equals)
        sprite_list.append(self.operator)

        # Position the left number block
        self.lhs.center_x = self.center_x
        self.lhs.center_y = self.center_y

        # Position the operator
        self.operator.center_x = self.center_x + (12 * TILE_SIZE)
        self.operator.center_y = self.center_y

        # Position the right number block
        self.rhs.center_x = self.center_x + (4 * TILE_SIZE)
        self.rhs.center_y = self.center_y

        # Position the equals sign
        self.equals.center_x = self.center_x + (16 * TILE_SIZE)
        self.equals.center_y = self.center_y

        # Position the answer number block
        self.answer.center_x = self.center_x + (8 * TILE_SIZE)
        self.answer.center_y = self.center_y
