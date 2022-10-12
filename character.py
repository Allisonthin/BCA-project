import arcade
# from ball import Ball
player_scaling = 0.1

class Player():

    def __init__(self,width, height):

        # screen size
        # self.width = width
        # self.height = height

        self.player_list = None
        self.player1 = None

        # self.player1.center_x = 300
        # self.player1.center_y = 300

        self.mspeed_h = 0
        self.mspeed_v = 0

        self.ball_x = None
        self.ball_y = 0

        
       # print("player init")

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.player1 = arcade.Sprite("image/soldier.png", player_scaling)

        self.player1.center_x = 300
        self.player1.center_y = 300
        self.player_list.append(self.player1)

        

        #print("char setup")
    def on_draw(self):

        arcade.start_render()
        

        self.player_list.draw()
        
        print("char on draw")

    def update(self,delta_time):

        
        self.player_list.update()

        self.player1.center_x += self.mspeed_h
        self.player1.center_y += self.mspeed_v

        print(self.ball_x," in character")
        self.ball_x = self.player1.center_x
        self.ball_y = self.player1.center_y

        print(self.ball_x," in character")


        
    def on_key_press(self, key, modifier):

       # print("on key char")

        if key == arcade.key.S:
            #self.player1.center_x = -self.mspeed

            self.mspeed_h = -10

        
        elif key == arcade.key.F:
            # self.player1.center_x = self.mspeed
            self.mspeed_h = 10
     
        elif key == arcade.key.E:
      
            # self.player1.center_y = self.mspeed

            self.mspeed_v = 10
        elif key == arcade.key.D:
            # self.player1.center_y = -self.mspeed
            self.mspeed_v = -10
      

    def on_key_release(self, key, modifier):
        if key == arcade.key.S or key == arcade.key.F:
            self.mspeed_h = 0
        elif key == arcade.key.E or key == arcade.key.D:
            self.mspeed_v = 0