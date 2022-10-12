import arcade 
from character import Player


player_scaling = 0.1

class Ball(Player):
    def __init__(self,width, height):
        super().__init__(width,height)
        self.width = width
        self.height = height

        self.bullet_list = None
        self.bullet = None

        self.bullet_speed = 0

        self.pos_x = 0
        self.pos_y = 0

        

        self.gun_sound = arcade.load_sound("sound/sniper-rifle-5989.mp3")

        # character object
        # self.player = Player(width, height)

        

    def setup(self):

        self.bullet_list = arcade.SpriteList()

        
    
        # print("inside the pos ")
        # print(self.pos_x, self.pos_y," inside the vall")

    def on_draw(self):

        arcade.start_render()

        
        self.bullet_list.draw()
        # print("on_drw ball")
    def on_mouse_press(self,x, y, buttom, modifier):

        print("1")
        if buttom == arcade.MOUSE_BUTTON_LEFT:

            self.bullet = arcade.Sprite("image/Laser_Bullet.webp ", player_scaling)

            arcade.play_sound(self.gun_sound)
            print("2")
            
            self.bullet.center_x = self.pos_x
            self.bullet.bottom = self.pos_y
            
            

            # print(self.bullet.center_x, self.bullet.center_y)

            self.bullet_list.append(self.bullet)

    def update(self,delta_time):

        self.pos_x = self.ball_x
        self.pos_y = self.ball_y
        print(type(self.ball_x)," for center x")
        print(ball_x," om vall")
        print(type(self.pos_x), " for position x")

        self.bullet_speed = 10
       # print(self.bullet_speed)

        
        for bul in self.bullet_list:
            #print("inside the update for loop")
            bul.center_x += self.bullet_speed

        self.bullet_list.update()

        for bull in self.bullet_list:

            if bull.left > self.width -100:
                bull.remove_from_sprite_lists()
                #print("inside the update if")
        self.bullet_list.update()
        #print("update")