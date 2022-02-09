import arcade

CRATE_BLUE_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_09.png"
CRATE_BROWN_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_07.png"


class NumberBlock(arcade.Sprite):
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
