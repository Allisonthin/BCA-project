from tarfile import PAX_FIELDS
import arcade

# from eg import GRID_PIXEL_SIZE, LAYER_NAME_FOREGROUND, LAYER_NAME_MOVING_PLATFORMS, SPRITE_PIXEL_SIZE


mspeed = 10
TILE_SCALING = 1

SPRITE_PIXEL_SIZE = 32

GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE* TILE_SCALING

coin_scaling =0.8

LAYER_NAME_PLATFORMS = "plat"
LAYER_NAME_FOREGROUND = "back"
LAYER_NAME_MOVING_PLATFORMS = "moving object"

gravity = 1
jump_speed = 23

class a(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, resizable=True )

        self.scene = None
        self.player = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.score  = 0
    
        self.tile_map = None
        self.level = 1

        self.px = 100
        self.py = 500

        self.end_map = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        

        # self.player_sprite = None

        arcade.set_background_color(arcade.color.AERO_BLUE)
        self.gun_sound = arcade.load_sound("sound/sniper-rifle-5989.mp3")

    def setup(self):

        self.scene = arcade.Scene()
        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)
        

        map_name = f"layer/untitled_1.tmj"

        

        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS:{
                "use_spatial_hash": False
            }
         }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        # self.scene.add_sprite_list_after("players", LAYER_NAME_FOREGROUND)


        # self.scene.add_sprite_list("players")
        # self.scene.add_sprite_list("walls", use_spatial_hash=True)
        # self.scene.add_sprite_list("coins")

        

        self.player = arcade.Sprite("image/soldier.png", 0.1)

        self.player.center_x = self.px
        self.player.center_y = self.py

        self.scene.add_sprite("players", self.player)

        self.end_map = self.tile_map.width * GRID_PIXEL_SIZE
        print(self.end_map)

        # print(self.tile_map.width)

        # for i in range(0,10000,64):

        #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
        #     wall.center_x = i
        #     wall.center_y = 32

        #     self.scene.add_sprite("walls", wall)

        # coordinate =[[512, 96], [256, 96], [768, 96]]

        # for wa in coordinate:

        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)

        #     wall.position = wa
        #     self.scene.add_sprite("walls", wall)

        # coin_coordinate = [[200, 96], [500, 96], [600, 96]]

        # for co in coin_coordinate:
        #     coin = arcade.Sprite(":resources:images/items/coinGold.png",coin_scaling)

        #     coin.position = co
        #     self.scene.add_sprite("coins", coin)


        if self.tile_map.background_color : 
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,platforms=self.scene[LAYER_NAME_PLATFORMS],
            gravity_constant=gravity,
            # ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_MOVING_PLATFORMS]

        )


    

    def on_draw(self):

        self.clear()
        
        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()
        score = f"score :{self.score}"
        arcade.draw_text(score, 10,10,arcade.color.WHITE, 24)
    
    def on_key_press(self, key, modifier):
        if key == arcade.key.F:
            self.player.change_x = mspeed
        elif key == arcade.key.S:
            self.player.change_x = -mspeed
        elif key == arcade.key.E:
            if self.physics_engine.can_jump():
                self.player.change_y = jump_speed
                arcade.play_sound(self.jump_sound)
        

    def on_key_release(self, key, modifier):
        if key == arcade.key.S or key == arcade.key.F:
            self.player.change_x = 0
        elif key == arcade.key.E or key == arcade.key.D:
            self.player.change_y = 0

    def center_camera_to_player(self):

        screen_centered_x = self.player.center_x - (self.camera.viewport_width/3)
        screen_centered_y = self.player.center_y - (self.camera.viewport_height/3)

        if screen_centered_x < 0:
            screen_centered_x = 0
        if screen_centered_y < 0:
            screen_centered_y = 0

        player_centered = screen_centered_x,screen_centered_y

        self.camera.move_to(player_centered)
            

    def update(self,delta_time):
        self.physics_engine.update() 

        # coin_hit_list = arcade.check_for_collision_with_list(self.player,self.scene["coins"])

        # for coin in coin_hit_list:
        #     coin.remove_from_sprite_lists()
        #     arcade.play_sound(self.collect_coin_sound)

        #     self.score += 1

        if self.player.center_y < 0:

            self.player.center_x = self.px
            self.player.center_y = self.py

        # if self.player.center_x >= self.end_map:

        #     self.level += 1

        #     self.setup()

        #     self.player.center_x = self.px
        #     self.player.center_y = self.py

        self.scene.update_animation(delta_time)

        self.scene.update([LAYER_NAME_MOVING_PLATFORMS])

    
        self.center_camera_to_player()

        



def main():

    win = a(1280,720)

    win.setup()

    arcade.run()

if __name__ == "__main__":

    main()