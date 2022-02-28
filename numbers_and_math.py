import arcade
import random
import operator

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
        print(f"NumberBlock created with value {self.value}")
        self.draw()

    def update_animation(self, delta_time: float = 1 / 60):
        # Draw this block's numeric value on top of this sprite.
        arcade.draw_text(
            f"{self.value}",
            start_x=self.center_x,
            start_y=self.center_y,
            color=arcade.color.WHITE,
            font_size=18,
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

    def __init__(self, blocks):
        self.blocks = blocks
        self.value = self._compute_value()

    def _compute_value(self):
        block_count = len(self.blocks)
        value = 0
        multiplier = 1
        for block in reversed(self.blocks):
            # print(f"i: {i}, multiplier: {multiplier}, block[i]: {self.blocks[i].value}")
            value += block.value * multiplier
            multiplier *= 10
        return value


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
        self.lhs_sprite = NumberBlock(self.problem.lhs)
        self.rhs_sprite = NumberBlock(self.problem.rhs)
        # self.operator_sprite = NumberBlock(self.problem.operator)
        self.answer_sprite = NumberBlock(int(self.problem.answer))

    def draw(self):
        self.scene.add_sprite(LAYER_NAME_NUMBER, self.lhs_sprite)
        self.scene.add_sprite(LAYER_NAME_NUMBER, self.rhs_sprite)
        self.scene.add_sprite(LAYER_NAME_NUMBER, self.answer_sprite)

        # Position the left number block
        self.lhs_sprite.center_x = self.center_x
        self.lhs_sprite.center_y = self.center_y

        # Position the right number block
        self.rhs_sprite.center_x = self.center_x + (4 * TILE_SIZE)
        self.rhs_sprite.center_y = self.center_y

        # Position the answer number block
        self.answer_sprite.center_x = self.center_x + (8 * TILE_SIZE)
        self.answer_sprite.center_y = self.center_y
