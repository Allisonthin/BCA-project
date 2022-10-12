import arcade

class a(arcade.Window):
    def __init__(self,width, height):
        super().__init__(width, height, fullscreen= True, resizable= True)

def main():

    win = a(600,300)
    arcade.run()

main()