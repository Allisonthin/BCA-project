import arcade

class a(arcade.Window):
    def __init__(self, width , height):
        super().__init__(width, height)

        self.player = None
        self.player_list = None

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()

        self.player = arcade.AnimatedTimeBasedSprite()

        self.player.textures = []

        pox = 7
        poy = 0
        for i in range(12):

            texture = arcade.load_texture("image/cat-run-cycle-animation-sequence_40831-250-removebg-preview.png", x= pox , y = poy)
            anim = arcade.AnimationKeyframe(i, 60, texture)

            self.player.frames.append(anim)
            if i % 6 ==0:
                pox = 7

            else:

                pox +=131
            if i % 12 in [6]:
                pox += 109 
        # for i in range(2):

        #     self.player.textures.append(arcade.load_texture("image/cat-run-cycle-animation-sequence_40831-250-removebg-preview.png", x= i*10, y= 0 , width = 10, height = 10))
        self.player.center_x = 100
        self.player.center_y = 100
        self.player_list.append(self.player)

    def on_draw(self):

        

        arcade.start_render()
        self.player_list.draw()

    def update(self,delta_time):

        self.player_list.update_animation()



def main():
    win = a(1200,900)

    win.setup()
    arcade.run()

if __name__ == "__main__":

    main()