import arcade

from constant import PAGE_TEXTURE, PLAYER_TEXTURES, SCREEN_HEIGHT, SCREEN_WIDTH

class Page(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window
        
        self.end = False
        self.center_x = SCREEN_WIDTH/2
        self.center_y = SCREEN_HEIGHT/2
        

        PAGE_TEXTURE.append(
            arcade.load_texture("assets\start.png")
        )
        PAGE_TEXTURE.append(
            arcade.load_texture("assets\end.png")
        )
        PAGE_TEXTURE.append(
            arcade.load_texture("assets/transparent.png")
        )
        self.texture = PAGE_TEXTURE[0]
        print("NOOOOOOOOOOOOOOOOOOOOOO")

    def update(self):
        #self.texture_update()
        pass
    

    def on_key_press(self, key, modifiers):
        """Called by the arcade.Window object whenever a key is pressed."""

        if key == arcade.key.SPACE :
            self.texture = PAGE_TEXTURE[2]

    # def texture_update(self):
    #     if self.end == True:
    #         self.texture = PAGE_TEXTURE[1]
    #     
        