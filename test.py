import unittest
import arcade
from numbers_and_math import NumberBlockGroup, NumberBlock


# noinspection PyPep8Naming
class TestNumberBlockGroup(unittest.TestCase):

    def setUp(self):
        self.window = arcade.Window(200, 200, "test", resizable=True)
        arcade.set_window(self.window)

    def test_single_block(self):
        block_one = NumberBlock(9)
        group_one = NumberBlockGroup([block_one])
        self.assertEqual(group_one.value, 9)

    def test_two_digit(self):
        block_one = NumberBlock(1)
        block_two = NumberBlock(5)
        group = NumberBlockGroup([block_one, block_two])
        self.assertEqual(group.value, 15)

    def test_three_digit(self):
        block_one = NumberBlock(1)
        block_two = NumberBlock(5)
        block_three = NumberBlock(9)
        group = NumberBlockGroup([block_one, block_two, block_three])
        self.assertEqual(group.value, 159)

    def test_place_left(self):
        block_one = NumberBlock(1)
        block_two = NumberBlock(5)
        group = NumberBlockGroup([block_one, block_two])
        group.place_left(NumberBlock(3))
        self.assertEqual(len(group._blocks), 3)
        self.assertEqual(group.value, 315)

    def test_place_right(self):
        block_one = NumberBlock(1)
        block_two = NumberBlock(5)
        group = NumberBlockGroup([block_one, block_two])
        group.place_right(NumberBlock(3))
        self.assertEqual(len(group._blocks), 3)
        self.assertEqual(group.value, 153)

if __name__ == '__main__':
    unittest.main()
