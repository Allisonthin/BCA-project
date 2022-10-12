import arcade
import threading
from ball import Ball
from character import Player
# from text import Text

class MyWindow(arcade.Window):
    def __init__(self,width, height, title):
        super().__init__(width, height,title)
        
        #print("blue")

        arcade.set_background_color(arcade.color.AMAZON)

        
 
        

        
        self.player = Player(width, height)
        self.ball1 = Ball(width,height)

        # t1 = threading.Thread(target=self.player, name='t1')
        # t2 = threading.Thread(target=self.ball1, name='t2') 

        # t1.start()  
        # t2.start()      
        #self.txt = Text()
       # print("1")
        
    
    def setup(self):

        
        self.player.setup()

        self.ball1.setup()
       # print("setup")

    def on_draw(self):

        arcade.start_render()
        self.clear()
        
        
        
        self.player.player_list.draw()
        self.ball1.bullet_list.draw()

        


        

    def update(self, delta_time):

        
        self.player.update(1)
        self.ball1.update(1)
        
    

    def on_key_press(self, key, modifier):

        self.player.on_key_press(key, modifier)
    
    def on_key_release(self, key, modifier):
        self.player.on_key_release(key, modifier)

    def on_mouse_press(self,x,y,button, modifier):
        # if button == arcade.MOUSE_BUTTON_LEFT:
        self.ball1.on_mouse_press(x,y,button, modifier)
       

        # for b in self.ball_list:

        #     b.on_draw()
        
    
    

    #def on_mouse_press(self, x, y, button , modifier):

        
        
        # if button == arcade.MOUSE_BUTTON_LEFT:
        #     self.bal.x = self.play1.a_x
        #     self.bal.y = self.play1.a_y

        #     #initializing bullet
        #     self.bal.ch_x = self.bspeed
        #     self.bal.ch_y == 0


        #     arcade.play_sound(self.gun_sound)
        #     self.text1.update()


        #     #print("left button")

  

def main():

    windo = MyWindow(1000,600,"mywind")

    windo.setup()
    arcade.run()

if __name__ == "__main__":
    main()