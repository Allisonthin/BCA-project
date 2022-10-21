
import arcade
import os








#screen size
width = 1080
height =800
title ="platformer"

#constants used to scale 
TILE_SCALING = 1
CHARACTER_SCALING = 0.2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 64
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# shooting constants
SPRITE_SCALING_LASER = 0.4
SHOOT_SPEED = 15
BULLET_SPEED = 35
BULLET_DAMAGE = 25

#layers
LAYER_NAME_PLATFORMS = "platform"
# LAYER_NAME_MOVING_PLATFORMS = "moving object"
LAYER_NAME_BACKGROUND="bgcolor"

LAYER_NAME_PLAYER = "player"
# LAYER_NAME_ENEMY =""
LAYER_NAME_BULLETS = "bullets"

#character direction
right_face = 0
left_face = 1

#character movement speed
movement_speed = 12
jump_speed = 30
gravity = 1

player_start_x = 100 
player_start_y = 500 

#loading texture
def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally= True),]




class Entity(arcade.Sprite):
    def __init__(self, folder_name, file_name):
        super().__init__()

        #default face direction
        self.player_face_direction = right_face

        #used for flipping between images
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.character_face_direction = right_face

        

        #path of the image sequence
        main_path = f"{folder_name}/{file_name}/" 

        #load texture for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}idle.png ")
        self.jump_texture_pair = load_texture_pair(f"{main_path}jump0.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}jmp1.png")

        # load texture for walking
        self.walking_textures = []
        for i in range(1,4):
            texture = load_texture_pair(f"{main_path}run {i}.png")
            self.walking_textures.append(texture)

        # load texture for climbing
        # self.climbing_texture = []
        # texture = arcade.load_texture(f"{main_path}_climb1.png")
        # self.climbing_texture.append(texture)
        # texture = arcade.load_texture(f"{main_path}_climb2.png")
        # self.climbing_texture.append(texture)

        #set the initial texture
        self.texture = self.idle_texture_pair[0]

        #setting hit box algorithm
        self.hit_box = self.texture.hit_box_points


class Enemy(Entity):
    def __init__(self,folder_name, file_name):
        super().__init__(folder_name, file_name)


class Animal(Enemy):
    def __init__(self):
        super().__init__("","")


class Player(Entity):
    def __init__(self):
        super().__init__("image","character")

        #track our current state
        self.jumping  = False

    def update_animation(self, delta_time: float = 1/60):

        # check if we need to flipped left or right face of the character
        if self.change_x < 0 and self.player_face_direction == right_face:
            self.player_face_direction = left_face

        elif self.change_x > 0 and self.player_face_direction == left_face:
            self.player_face_direction = right_face


        #climbing animation
        # if self.is_on_ladder:
        #     self.climbing = True

        # if not self.is_on_ladder and self.climbing:
        #     self.climbing = False

        # if self.climbing and abs(self.change_y) > 1:
        #     self.cur_texture += 1
        #     if self.cur_texture > 7:
        #         self.cur_texture = 0

        # if self.climbing:
        #     self.texture = self.climbing_texture[self.cur_texture//4]
        #     return

        # jumping animation
        if self.change_y > 0:
            self.texture= self.jump_texture_pair[self.player_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.jump_texture_pair[self.player_face_direction]
            return

        #walking animation
        self.cur_texture += 1
        if self.cur_texture > 1:
            self.cur_texture = 1
        self.texture = self.walking_textures[self.cur_texture][self.player_face_direction]
        






class MYGAME(arcade.Window):

    def __init__(self):

        super().__init__(width, height, title)

        #set path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #track the current state of the player 
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_reset = False
        self.shoot_press = False

        #our tilemap object
        self.tile_map = None

        # our scene object
        self.scene = None

        # separate variable that holds the player sprite
        self.player_sprite = None

        # our Physics engine
        self.physics_engine = None

        # a player camera
        self.camera = None

        #set background
        # arcade.set_background_color(arcade.color.AERO_BLUE)

        # GUI  camera
        self.gui_camera = None

        self.end_map = 0

        # keep track of the score
        self.score = 0

        #shooting mechanism
        self.can_shoot = False
        self.shoot_timer = 0

        # bullet texture
        # self.bullet_texture_pair = none

        # load sounds




    def setup(self):

        # setting up the cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        
        # map path
        map_name = "layer/map/Map.tmx"

        #layer specifying options for the tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS:{
                "use_spatial_hash": True,
            },
            # LAYER_NAME_MOVING_PLATFORMS:{
            #     "use_spatial_hash": False,
            # },
        }

        # load in tilemap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        

        #initialize new scene with our tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.can_shoot = True
        self.shoot_timer = 0
        # setting up the player, specifically placing it at these coordinate
        self.player_sprite = Player()
        self.player_sprite.center_x = player_start_x
        self.player_sprite.center_y = player_start_y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # calculating the  right edge of the map in pixels
        self.end_map = self.tile_map.width * GRID_PIXEL_SIZE


        # enemy position and state
        # enemy_layer = self.tile_map.object_lists[LAYER_NAME_ENEMY]

        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        #set the background color 
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # create the physics  engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            # platforms = self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=gravity,
            walls= self.scene[LAYER_NAME_PLATFORMS]
        )


    def on_draw(self):

        # clearing the screen to the background color
        self.clear()

        # Activating our camera 
        self.camera.use()
        # draw our scene
        self.scene.draw()

        # Activating the GUI camera before drawing GUI components
        self.gui_camera.use()

        
    def process_keychange(self):

        # process up/down
        if self.up_pressed and not self.down_pressed:
            # if self.physics_engine.is_on_ladder():
            #     self.player_sprite.change_y = movement_speed
            if self.physics_engine.can_jump(y_distance=10) and not self.jump_reset:
                self.player_sprite.change_y = jump_speed
                self.jump_reset = True

        # elif self.down_pressed and not self.up_pressed:
        #     if self.physics_engine.is_on_ladder():
        #         self.player_sprite.change_y = -movement_speed

        # process up/down on a ladder or no movement
        # if self.physics_engine.is_on_ladder():
        #     if not self.up_pressed and not self.down_pressed:
        #         self.player_sprite.change_y =0
        #     elif self.up_pressed and self.down_pressed:
        #         self.player_sprite.change_y =0

        # process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = movement_speed
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -movement_speed
        else:
            self.player_sprite.change_x = 0

    def on_mouse_press(self,x,y, key, modifiers):

        if key == arcade.MOUSE_BUTTON_LEFT:

            self.shoot_press = True

    def on_mouse_release(self, x ,y , key, modifiers):
        if key == arcade.MOUSE_BUTTON_LEFT:
            self.shoot_press = False

    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.E:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.S:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.F:
            self.right_pressed = True

        self.process_keychange()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.E:
            self.up_pressed = False
            self.jump_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.D:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.S:
            self.left_pressed= False
        elif key == arcade.key.RIGHT or key == arcade.key.F:
            self.right_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_x < 0:
            screen_x = 0
        if screen_y < 0:
            screen_y = 0
        player_centered = screen_x , screen_y
        self.camera.move_to(player_centered, 0.2)


    def on_update(self, delta_time):

        # movement and game logic
        self.physics_engine.update()

        #update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False

        else:
            self.player_sprite.can_jump = True

            

        if self.can_shoot:
            if self.shoot_press:
                bullet = arcade.Sprite("image/[removal.ai]_tmp-63511f616034b.png",SPRITE_SCALING_LASER,)
                bullet_texture = load_texture_pair()
                
                if self.player_sprite.player_face_direction == right_face:
                    bullet.change_x = BULLET_SPEED
                elif self.player_sprite.player_face_direction== left_face:
                    bullet.change_x = -BULLET_SPEED

                

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
            
        else:
            self.shoot_timer +=1
            if self.shoot_timer == 5:
                self.can_shoot = True
                self.shoot_timer = 0

            
        # if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
        #     self.player_sprite.is_on_ladder = True
        #     self.process_keychange()

        # else:
        #     self.player_sprite.is_on_ladder = False
        #     self.process_keychange()

        #update Animations
        self.scene.update_animation(
            delta_time,
             [
                LAYER_NAME_PLAYER,
                LAYER_NAME_BACKGROUND,
                ],
        )

        # # update walls, used with moving  platforms
        self.scene.update([LAYER_NAME_BULLETS])

        # position the camera
        self.center_camera_to_player()

def main():
    """Main Function"""
    wind = MYGAME()
    wind.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        


