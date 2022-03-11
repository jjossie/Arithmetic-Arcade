import arcade
import random
import operator

from constant import *


class NumberBlock(arcade.Sprite):
    """
    A sprite that draws itself as a crate with its stored value as a number on top.
    """

    def __init__(self, scene, value):
        super().__init__()
        assert (value is not None and scene is not None)
        self.value = value
        self.texture = arcade.load_texture(CRATE_BLUE_PATH)
        self.scale = TILE_SCALING
        self._hit_box_algorithm = "None"
        self.hit_box_sprite = arcade.Sprite("assets/teansparent.png", scale=TILE_SCALING * 1.1,
                                            center_x=self.center_x,
                                            center_y=self.center_y)

        # Add myself to a sprite list
        scene.get_sprite_list(LAYER_NAME_NUMBER).append(self)
        # Add my hit box sprite to the other one
        scene.get_sprite_list(LAYER_NAME_NUMBER_HITBOX).append(self.hit_box_sprite)

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
        self.hit_box_sprite.center_x = x
        self.hit_box_sprite.center_y = y

    def __str__(self):
        return super.__str__(self) + f"\nNumberBlock Val: {self.value} \nSpriteList: {self.sprite_lists}" \
               + f"\n{self._points}\n\n"


class NumberBlockGroup:
    """
    One or more (probably up to 3) NumberBlocks that represent a single value.
    """

    def __init__(self, scene=None, x=0, y=0, blocks=None, from_number=None):
        assert (scene is not None)
        self.scene = scene
        self.center_x = x
        self.center_y = y
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
            blocks.append(NumberBlock(self.scene, temp_val))
        else:
            finished = False
            multiplier = 1
            while not finished:
                single_digit = int(((temp_val % (multiplier * 10)) - (temp_val % multiplier)) / multiplier)
                blocks.insert(0, NumberBlock(self.scene, single_digit))
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

    def _update_locations(self):
        for index, block in enumerate(self._blocks):
            offset = index * TILE_SIZE * TILE_SCALING * 2
            block.move_to(self.center_x + offset, self.center_y)

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

    def log(self):
        for block in self._blocks:
            print(str(block))


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


def get_clean_problem(min=None, max=None):
    """
    Quick and Dirty method for getting a nice and pretty math problem; i.e., one
    where the answer comes out to an integer, not a decimal.
    """
    prob = None
    valid = False
    while not valid:
        prob = SimpleMathProblem(min, max)
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

    def __init__(self, scene, center_x=0, center_y=0, min=None, max=None):
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y

        self.sprite_list = self.scene.get_sprite_list(LAYER_NAME_NUMBER)
        self.problem = get_clean_problem(min, max)
        self.lhs = NumberBlockGroup(scene=self.scene, from_number=self.problem.lhs)
        self.operator = NumberBlockGroup(scene=self.scene, from_number=str(self.problem.operator))
        self.rhs = NumberBlockGroup(scene=self.scene, from_number=self.problem.rhs)
        self.equals = NumberBlockGroup(scene=self.scene, from_number="=")
        self.answer = NumberBlockGroup(scene=self.scene, from_number=self.problem.answer)

        self.draw_order = [self.lhs, self.operator, self.rhs, self.equals, self.answer]

    def draw(self):
        x = self.center_x
        y = self.center_y
        space = TILE_SIZE * TILE_SCALING * 2
        for chunk in self.draw_order:
            size = chunk.get_size()
            chunk.move_to(x, y)

            # Move over to the next space
            x += space * size + space

    def log(self):
        for block in self.draw_order:
            block.log()
