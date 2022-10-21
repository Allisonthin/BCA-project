
from turtle import width
import arcade



class mainscreen(arcade.View):
    # def __init__(self):
    #     self.new = None
    #     self.set = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALICE_BLUE)


    def setting(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_text("new game", 500,400, arcade.color.RED, 12, 10)
        arcade.draw_text("resume", 500,370, arcade.color.RED, 12, 10)
        
        arcade.draw_text("setting", 500,340, arcade.color.RED, 12, 10)


    def on_mouse_press(self, x , y , button, modifiers):
        game_view = Gameview()
        # if button == arcade.MOUSE_BUTTON_LEFT and x == 500 :
        self.window.show_view(game_view)

class Gameview(arcade.View):
    def __init__(self):
        super().__init__()

        # arcade.set_background_color(arcade.color.BLUE)

    def setup(self):

        print("setup")

    def on_show_view(self):
        self.setup()


def main():

    window = arcade.Window(1000,800)

    menu = mainscreen()
    window.show_view(menu)
    g= Gameview()
    arcade.run()

if __name__ == "__main__":
    main()