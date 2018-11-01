# Modules
import libtcodpy as libtcod
import pygame
import math

# Game files
import constants

#  ____ _____ ____  _   _  ____ _____ 
# / ___|_   _|  _ \| | | |/ ___|_   _|
# \___ \ | | | |_) | | | | |     | |  
#  ___) || | |  _ <| |_| | |___  | |  
# |____/ |_| |_| \_\\___/ \____| |_|  

class structure_tile:

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class structure_assets:

    def __init__(self):

        ## SPRITESHEETS ##
        self.character = object_spritesheet("sprites/58qsdgA.png")
        self.reptile = object_spritesheet("sprites/graphics/Characters/Reptile.png")
        self.aquatic = object_spritesheet("sprites/reptilesheet.png")
        self.wall = object_spritesheet("sprites/graphics/Objects/Wall.png")
        self.floor = object_spritesheet("sprites/graphics/Objects/Floor.png")
        self.shield = object_spritesheet("sprites/graphics/Items/Shield.png")
        self.medwep = object_spritesheet("sprites/graphics/Items/MedWep.png")
        self.scroll = object_spritesheet("sprites/graphics/Items/Scroll.png")
        self.flesh = object_spritesheet("sprites/graphics/Items/Flesh.png")

        ## ANIMATIONS ##
        self.A_PLAYER = self.character.get_animation(0, 6, 32, 32, 3, (32, 32))
        self.A_SNAKE_01 = self.reptile.get_animation(5, 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_02 = self.reptile.get_animation(11, 5, 16, 16, 2, (32, 32))


        ## SPRITES ##
        self.S_WALL = self.wall.get_image(11, 7, 16, 16, (32, 32))[0]
        self.S_WALLEXPLORED = self.wall.get_image(11, 13, 16, 16, (32, 32))[0]

        self.S_FLOOR = self.floor.get_image(9, 8, 16, 16, (32, 32))[0]
        self.S_FLOOREXPLORED = self.floor.get_image(
            9, 11, 16, 16, (32, 32))[0]

        ## ITEMS ##
        self.S_SWORD = self.medwep.get_image(1, 1, 16, 16, (32, 32))
        self.S_SHIELD = self.shield.get_image(1, 1, 16, 16, (32, 32))
        self.S_SCROLL_01 = self.scroll.get_image(5, 1, 16, 16, (32, 32))
        self.S_SCROLL_02 = self.scroll.get_image(3, 2, 16, 16, (32, 32))
        self.S_SCROLL_03 = self.scroll.get_image(4, 6, 16, 16, (32, 32))
        self.S_FLESH_01 = self.flesh.get_image(2, 4, 16, 16, (32, 32))

        # # Sprite sheets
        # self.characterspritesheet = object_spritesheet("sprites/58qsdgA.png")
        # self.enemyspritesheet = object_spritesheet("sprites/reptilesheet.png")
        # # Animations
        # self.A_PLAYER = self.characterspritesheet.get_animation(0, 6, 32, 32, 3, (32, 32))
        # self.A_OGRE = self.enemyspritesheet.get_animation(4, 5, 16, 16, 4, (32, 32))
        # Map tiles
        # self.S_WALL = pygame.image.load("sprites/wall.png")
        # self.S_WALLEXPLORED = pygame.image.load("sprites/wallool.png")
        # self.S_FLOOR = pygame.image.load("sprites/grass.png")
        # self.S_FLOOREXPLORED = pygame.image.load("sprites/grassool.png")
        ## Fonts
        self.FONT_DEBUG_MESSAGE = pygame.font.Font("fonts/joystix_monospace.ttf", 12)
        self.FONT_MESSAGE_TEXT = pygame.font.Font("fonts/joystix_monospace.ttf", 12)
        self.FONT_CURSOR_TEXT = pygame.font.Font("fonts/joystix_monospace.ttf", constants.CELL_HEIGHT)


#   ___  ____      _ _____ ____ _____ ____  
#  / _ \| __ )    | | ____/ ___|_   _/ ___| 
# | | | |  _ \ _  | |  _|| |     | | \___ \ 
# | |_| | |_) | |_| | |__| |___  | |  ___) |
#  \___/|____/ \___/|_____\____| |_| |____/ 
                                         

class object_actor:


    def __init__(self, x, y, name_object, animation, animation_speed = .7, creature = None, ai = None, container = None, item = None, equipment = None):
        self.x = x   #MAP address , not a pixel address
        self.y = y   #MAP address
        self.name_object = name_object
        self.animation = animation
        self.animation_speed = animation_speed / 1.0 # in seconds

        # Animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0

        self.creature = creature
        if self.creature:
            self.creature.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            self.item = component_item()
            self.item.owner = self


    @property
    def display_name(self):

        if self.creature:
            return (self.creature.name_instance + " the " + self.name_object)

        if self.item:
            if self.equipment and self.equipment.equipped:
                return (self.name_object + " (e)")
            else:
                return self.name_object



    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAIN.blit(self.animation[0], ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT ))
            elif len(self.animation) > 1:
                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()
                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0
                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0
                    else:
                        self.sprite_image += 1
                SURFACE_MAIN.blit(self.animation[self.sprite_image],
                                 ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT ))


    def distance_to(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, other):

        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

class object_game:

    def __init__(self):
        self.current_objects = []
        self.message_history = []
         
class object_spritesheet:
    """ this class is gonna be used to grab images out of a sprite sheet"""
    def __init__(self, file_name):
        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()
        
    def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, num_sprites = 1, scale = None):

        image_list = []

        for i in range(num_sprites):
            # create blank image
            image = pygame.Surface([width, height]).convert()
            # copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0, 0), ( column * width + (width * i), row * height, width, height))
            # set transparency key to black
            image.set_colorkey(constants.COLOR_BLACK)
            # Scale is a tuple
            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))
            image_list.append(image)
        return image_list

    def get_image(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT, scale=None):

        image_list = []

        # create blank image
        image = pygame.Surface([width, height]).convert()
        # copy image from sheet onto blank
        image.blit(self.sprite_sheet, (0, 0),
                    (column * width, row * height, width, height))
        # set transparency key to black
        image.set_colorkey(constants.COLOR_BLACK)
        # Scale is a tuple
        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))
        image_list.append(image)
        return image_list

class obj_Room:

    ''' This is a rectangle that lives on the map '''

    def __init__(self, coords, size):

        self.x1, self.y1 = coords
        self.w, self.h = size

        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return (center_x, center_y)

    def intersect(self, other):

        # return True if other obj intersects with this one
        objects_intersect = (self.x1 <= other.x2 and self.x2 >= other.x1 and
                             self.y1 <= other.y2 and self.y2 >= other.y1)

        return objects_intersect


#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____  
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___| 
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \ 
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/ 
                                                             
class component_creature:
    """ Creatures have health , can damage other objects
        by attacking them. They can be killed """
    def __init__(self, name_instance, base_atk = 2, base_def = 0, hp = 10, death_function = None):
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):
      
        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = check_map_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target)

        if not tile_is_wall:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):

        damage_delt = self.power - target.creature.defense

        game_message(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_delt) +  " damage!", constants.COLOR_WHITE)
        target.creature.take_damage(damage_delt)


    def take_damage(self, damage):
        self.hp -= damage
        game_message(self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):
        self.hp += value
        if self.hp >= self.maxhp:
            self.hp = self.maxhp

    @property
    def power(self):

        total_power = self.base_atk

        if self.owner.container:
            object_bonuses = [obj.equipment.attack_bonus
                              for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_power += bonus

        return total_power

    @property
    def defense(self):

        total_defense = self.base_def

        if self.owner.container:
            object_bonuses = [obj.equipment.defense_bonus
                              for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_defense += bonus

        return total_defense

class ai_Confuse:

    '''Objects with this ai aimlessly wonder around

    '''

    def __init__(self, old_ai, num_turns):

        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):

        if self.num_turns > 0:
            self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                     libtcod.random_get_int(0, -1, 1))

            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai

            game_message(self.owner.display_name + " has broken free!",
                         constants.COLOR_RED)

class ai_Chase:
    ''' A basic monster ai which chases and tries to harm player.

    '''
    def take_turn(self):

        monster = self.owner

        if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

            # move towards the player if far away
            if monster.distance_to(PLAYER) >= 2:
                self.owner.move_towards(PLAYER)

            # if close enough, attack player
            elif PLAYER.creature.hp > 0:
                monster.creature.attack(PLAYER)

class component_container:
    
    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume

    # Get names of everything in inventory

    # Get volume within inventory
    @property
    def volume(self):
        return 0.0

    @property
    def equipped_items(self):

        list_of_equipped_items = [obj for obj in self.inventory
                                  if obj.equipment and obj.equipment.equipped]

        return list_of_equipped_items


    # Get weight of everything in inventory

class component_item:

    def __init__(self, weight = 0.0, volume = 0.0, use_function = None, value = None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function

        # Pick up item
    def pick_up(self, actor):
        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Your inventory is full!", constants.COLOR_WHITE)
            else:
                game_message("Picking up ", constants.COLOR_WHITE)
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.container = actor.container

        # Drop item
    def drop(self, new_x, new_y):
        GAME.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game_message("Item dropped!", constants.COLOR_WHITE)

        # Use the item
    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function:
            result = self.use_function(self.container.owner, self.value)
            if result is not None:
                print("use_function failed")
            else:
                self.container.inventory.remove(self.owner)

class component_equipment:

    def __init__(self, attack_bonus=None, defense_bonus=None, slot=None):

        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):

        #check for equipment in slot
        all_equipped_items = self.owner.item.container.equipped_items

        for item in all_equipped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                game_message("equipment slot is occupied", constants.COLOR_RED)
                return

        self.equipped = True

        game_message("item equipped", constants.COLOR_WHITE)

    def unequip(self):
        #toggle self.equipped
        self.equipped = False

        game_message("item unequipped", constants.COLOR_WHITE)

#  ____             _   _
# |  _ \  ___  __ _| |_| |__
# | | | |/ _ \/ _` | __| '_ \
# | |_| |  __/ (_| | |_| | | |
# |____/ \___|\__,_|\__|_| |_|


def death_snake(monster):
    '''Default death function for creatures.

    '''

    # print message alerting player that creature has died
    game_message(monster.creature.name_instance +
                 " is dead!",
                 constants.COLOR_GREY)

    # remove ai and creature components
    monster.animation = ASSETS.S_FLESH_01
    monster.creature = None
    monster.ai = None


#  __  __    _    ____  
# |  \/  |  / \  |  _ \ 
# | |\/| | / _ \ | |_) |
# | |  | |/ ___ \|  __/ 
# |_|  |_/_/   \_\_|    
                      

def create_map():
    new_map = [[ structure_tile(True) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH) ]

    # Generate new room
    list_of_rooms = []

    for i in range(constants.MAP_MAX_NUM_ROOMS):

        w = libtcod.random_get_int(0, constants.ROOM_MIN_WIDTH,
                                   constants.ROOM_MAX_WIDTH)
        h = libtcod.random_get_int(0, constants.ROOM_MIN_HEIGHT,
                                   constants.ROOM_MAX_HEIGHT)

        x = libtcod.random_get_int(0, 2, constants.MAP_WIDTH - w - 2)
        y = libtcod.random_get_int(0, 2, constants.MAP_HEIGHT - h - 2)

        #create the room
        new_room = obj_Room((x, y), (w, h))

        failed = False

        # check for interference
        for other_room in list_of_rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # place room
            map_create_room(new_map, new_room)
            current_center = new_room.center

            if len(list_of_rooms) == 0:
                gen_player(current_center)
                #print(current_center)
            else:
                previous_center = list_of_rooms[-1].center
                #print(previous_center)
                # dig tunnels
                map_create_tunnels(current_center, previous_center, new_map)

            list_of_rooms.append(new_room)


    # new_map[10][10].block_path = True  # Walls gonna block path
    # new_map[8][15].block_path= True

    # for x in range(constants.MAP_WIDTH): # Places walls around the map
    #     new_map[x][0].block_path = True
    #     new_map[x][constants.MAP_HEIGHT-1].block_path = True

    # for y in range(constants.MAP_HEIGHT):
    #     new_map[0][y].block_path = True
    #     new_map[constants.MAP_WIDTH-1][y].block_path = True

    make_map_fov(new_map)

    return (new_map, list_of_rooms)

def map_place_objects(room_list):

    for room in room_list:
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
        if (x, y) is not (PLAYER.x, PLAYER.y):
            gen_enemy((x, y))

        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
        if (x, y) is not (PLAYER.x, PLAYER.y):
            gen_item((x, y))

def map_create_room(new_map, new_room):
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            new_map[x][y].block_path = False

def map_create_tunnels(coords1, coords2, new_map):

    coin_flip = (libtcod.random_get_int(0, 0, 1))

    x1, y1 = coords1
    x2, y2 = coords2

    x_step, y_step = 1, 1

    if x1 > x2:
        x_step = -1

    if y1 > y2:
        y_step = -1


    if coin_flip == 0:

        for x in range(x1, (x2 + x_step), x_step):
            new_map[x][y1].block_path = False

        for y in range(y1, (y2 + y_step), y_step):
            new_map[x2][y].block_path = False

    else:

        for y in range(y1, (y2 + y_step), y_step):
            new_map[x1][y].block_path = False

        for x in range(x1, (x2 + x_step), x_step):
            new_map[x][y2].block_path = False

    return new_map

def check_map_creatures(x, y, exclude_object = None):

    target = None

    if exclude_object: # check object to find creature in location that is not excluded

        for object in GAME.current_objects:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and 
                object.creature):
                target = object

            if target:
                return target
    
    else: # check objectlist to find any creature at that location

        for object in GAME.current_objects:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and 
                object.creature):
                target = object

            if target:
                return target

def make_map_fov(incoming_map):
    
    global FOV_MAP

    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, 
                                                      not incoming_map[x][y].block_path)

def calculate_map_fov():

    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, 
                                constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)

def map_objects_at_coords(coords_x, coords_y):
    # Checks if there is an object in the specific map location
    object_options = [obj for obj in GAME.current_objects if obj.x == coords_x and obj.y == coords_y]
    return object_options

def create_map_line(coords_1, coords_2):
    # Converts two x, y, coordinates into a list of tiles.
    # coords_1 : (x1, y1)
    # coords_2 : (x2, y2)
    x1, y1 = coords_1
    x2, y2 = coords_2
    libtcod.line_init(x1, y1, x2, y2)
    calc_x, calc_y = libtcod.line_step()
    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    while (not calc_x is None):

        coord_list.append((calc_x, calc_y))

        calc_x, calc_y = libtcod.line_step()

    return coord_list

def check_map_for_wall(x, y):

    incoming_map[x][y].block_path

def map_find_radius(coords, radius):

    center_x, center_y = coords

    tile_list = []

    start_x = (center_x - radius)
    end_x = (center_x + radius + 1)

    start_y = (center_y - radius)
    end_y = (center_y + radius + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x, y))

    return tile_list


#  ____  ____      ___        __
# |  _ \|  _ \    / \ \      / /
# | | | | |_) |  / _ \ \ /\ / / 
# | |_| |  _ <  / ___ \ V  V /  
# |____/|_| \_\/_/   \_\_/\_/   


def draw_game():
    """ This function clears(updates) the 'map' , draws the map and the character """
    # Character needs to be drawn in top of the map! The order is important! LAYERS
    SURFACE_MAIN.fill(constants.COLOR_BLACK)

    # Draws the map
    draw_map(GAME.current_map)

    # Draws the objects (player , nemeies , items , etc)
    for objs in GAME.current_objects:
        objs.draw()

    draw_debug()
    draw_messages()

def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)    
            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(ASSETS.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                else:
                    SURFACE_MAIN.blit(ASSETS.S_FLOOR, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))    

            elif map_to_draw[x][y].explored:

                if map_to_draw[x][y].block_path == True:
                    SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                else:
                    SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))    

def draw_debug():

    draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_RED)

def draw_messages():

    to_draw = GAME.message_history[-(constants.NUM_MESSAGES):]
    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)
    start_y = constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height) - 10

    i = 0

    for message, color in to_draw:
        draw_text(SURFACE_MAIN, message, (10, start_y + (i * text_height)), color )
        i += 1

def draw_text(display_surface, text_to_display, coords, text_color, background_color = None, center = False):
    """ This function takes in some texts and displays it on the referenced surface """
    text_surface, text_rect = helper_text_objects(text_to_display, text_color, background_color)

    # adjust the location of the surface based on the coordinates
    if not center:
        text_rect.topleft = coords
    else:
        text_rect.center = coords


    display_surface.blit(text_surface, text_rect)

def draw_tile_rect(coords, tile_color = None, tile_alpha = None, mark = None):
    x, y = coords
    # Default colors
    if tile_color:
        local_color = tile_color
    else:
        local_color = constants.COLOR_WHITE

    # default alpha
    if tile_alpha:
        local_alpha = tile_alpha
    else:
        local_alpha = 200

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT
    new_surface = pygame. Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(local_color)
    new_surface.set_alpha(local_alpha)
    if mark:
        draw_text(new_surface, mark,
                  coords=(constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2),
                  text_color=constants.COLOR_BLACK, center=True)

    SURFACE_MAIN.blit(new_surface, (new_x, new_y))


#  _   _  _____  _      ____   _____  ____    _____  _   _  _   _   ____  _____  ___  ___   _   _  ____  
# | | | || ____|| |    |  _ \ | ____||  _ \  |  ___|| | | || \ | | / ___||_   _||_ _|/ _ \ | \ | |/ ___| 
# | |_| ||  _|  | |    | |_) ||  _|  | |_) | | |_   | | | ||  \| || |      | |   | || | | ||  \| |\___ \ 
# |  _  || |___ | |___ |  __/ | |___ |  _ <  |  _|  | |_| || |\  || |___   | |   | || |_| || |\  | ___) |
# |_| |_||_____||_____||_|    |_____||_| \_\ |_|     \___/ |_| \_| \____|  |_|  |___|\___/ |_| \_||____/ 
                                                                                                       

def helper_text_objects(incoming_text, incoming_color, incoming_background):
    if incoming_background:
        text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_background)
    else:
        text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return text_surface, text_surface.get_rect()

def helper_text_height(font):

    font_object = font.render("a", False, (0, 0, 0))
    font_rect = font_object.get_rect()
    return font_rect.height

def helper_text_width(font):

    font_object = font.render("a", False, (0, 0, 0))
    font_rect = font_object.get_rect()
    return font_rect.width


#  __  __             _      
# |  \/  | __ _  __ _(_) ___ 
# | |\/| |/ _` |/ _` | |/ __|
# | |  | | (_| | (_| | | (__ 
# |_|  |_|\__,_|\__, |_|\___|
#               |___/       

def cast_heal(target, value):
    if target.creature.hp == target.creature.maxhp:
        game_message(target.creature.name_instance + " the " + target.name_object + " is already at maximum hp!", constants.COLOR_GREY)
        return "canceled"
    else:
        target.creature.heal(value)
        game_message(target.creature.name_instance + " the " + target.name_object + " healed for " + str(value) + " health!", constants.COLOR_GREY)
        game_message(target.creature.hp)
    return None

def cast_lightning(caster, T_damage_maxrange):

    damage, m_range = T_damage_maxrange

    player_location = (PLAYER.x, PLAYER.y)

    # Prompt the player for a tile
    point_selected = menu_tile_select(coords_origin = player_location, max_range = 5, penetrate_walls = False)
    # Converts that tile into a list of tiles between A -> B
    if point_selected:
        list_of_tiles = create_map_line(player_location, point_selected)
        # Cycle through list, damage everything found
        for i, (x, y) in enumerate(list_of_tiles):

            target = check_map_creatures(x, y)

            if target:
                target.creature.take_damage(damage)

def cast_fireball(caster, T_damage_radius_range):

    # defs
    damage, local_radius, max_r  = T_damage_radius_range

    player_location = (caster.x, caster.y)

    # get target tile
    point_selected = menu_tile_select(coords_origin=player_location,
                                      max_range=max_r,
                                      penetrate_walls=False,
                                      pierce_creature=False,
                                      radius=local_radius)

    if point_selected:
        # get sequence of tiles
        tiles_to_damage = map_find_radius(point_selected, local_radius)

        creature_hit = False

        # damage all creatures in tiles
        for (x, y) in tiles_to_damage:
            creature_to_damage = check_map_creatures(x, y)

            if creature_to_damage:
                creature_to_damage.creature.take_damage(damage)

                if creature_to_damage is not PLAYER:
                    creature_hit = True

        if creature_hit:
            game_message("The monster howls out in pain as it BURNS...", constants.COLOR_RED)

def cast_confusion(caster, effect_length):

    # select tile
    point_selected = menu_tile_select()

    # get target
    if point_selected:
        tile_x, tile_y = point_selected
        target = check_map_creatures(tile_x, tile_y)

        # temporarily confuse the target
        if target:
            oldai = target.ai

            target.ai = ai_Confuse(old_ai=oldai, num_turns=effect_length)
            target.ai.owner = target

            game_message("The creature's eyes glaze over",
                         constants.COLOR_GREEN)


#  __  __                      
# |  \/  | ___ _ __  _   _ ___ 
# | |\/| |/ _ \ '_ \| | | / __|
# | |  | |  __/ | | | |_| \__ \
# |_|  |_|\___|_| |_|\__,_|___/


def menu_pause():

    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    menu_text = "PAUSED"
    menu_font = ASSETS.FONT_DEBUG_MESSAGE

    text_height = helper_text_height(menu_font)
    text_width = len(menu_text) * helper_text_width(menu_font)

    menu_close = False
    while not menu_close:
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_close = True

        draw_text(SURFACE_MAIN, "PAUSED", (constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2), constants.COLOR_RED)

        CLOCK.tick(constants.GAME_FPS)

        pygame.display.flip()

def menu_inventory():

    menu_close = False

    # Calculate window dimensions
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    # Menu characteristics
    menu_width = 200
    menu_height = 200
    menu_x = (window_width / 1.2) - menu_width / 2
    menu_y = (window_height / 1.3) - menu_height / 2

    
    menu_text_font = ASSETS.FONT_DEBUG_MESSAGE
    menu_text_height = helper_text_height(menu_text_font)

    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:
        # Clear the menu
        local_inventory_surface.fill(constants.COLOR_GREY)
        # Register changes
        print_list = [obj.display_name for obj in PLAYER.container.inventory]
        # Get list of input events
        events_list = pygame.event.get()
        # Mouse events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x_relative = mouse_x - menu_x
        mouse_y_relative = mouse_y - menu_y

        mouse_in_window = (mouse_x_relative > 0 and 
                            mouse_y_relative > 0 and
                            mouse_x_relative < menu_width and 
                            mouse_y_relative < menu_height)

        mouse_line_selection = mouse_y_relative / menu_text_height

        # Cycle through events
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if mouse_in_window and int(mouse_line_selection) <= len(print_list) - 1:
                        PLAYER.container.inventory[int(mouse_line_selection)].item.drop(PLAYER.x, PLAYER.y)
                if event.button == 1:
                    if mouse_in_window and int(mouse_line_selection) <= len(print_list) - 1:
                        PLAYER.container.inventory[int(mouse_line_selection)].item.use()
                        menu_close = True


        # Draw the list
        for line, (name) in enumerate(print_list):
            if line == int(mouse_line_selection) and mouse_in_window:
                draw_text(local_inventory_surface, name, (0, 0 + (line*menu_text_height)), constants.COLOR_BLACK, constants.COLOR_WHITE)
            else:
                draw_text(local_inventory_surface, name, (0, 0 + (line*menu_text_height)), constants.COLOR_BLACK)

        # Render game
        draw_game()

        # Draw menu
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))
        
        CLOCK.tick(constants.GAME_FPS)

        pygame.display.update()

def menu_tile_select(coords_origin = None, max_range = None, radius = None, 
                    penetrate_walls = True, pierce_creature = True):

    # Lets the player select a tile , pauses the game , produces an onscreen rectangle , when the player
    # presses the LMB will return the map adress ( used for magic spells )
    menu_close = False
    while not menu_close:
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Get button clicks
        events_list = pygame.event.get()
        # Mouse map selection 
        map_coord_x = mouse_x // constants.CELL_WIDTH
        map_coord_y = mouse_y // constants.CELL_HEIGHT

        valid_list_of_tiles = []

        if coords_origin:
            full_list_of_tiles = create_map_line(coords_origin, (map_coord_x, map_coord_y))

            for i, (x, y) in enumerate(full_list_of_tiles):

                valid_list_of_tiles.append((x, y))

                if max_range and i == max_range - 1:
                    break

                if not penetrate_walls and GAME.current_map[x][y].block_path:
                    break

                if not pierce_creature and check_map_creatures(x, y):
                    break


        else:
            valid_list_of_tiles = [(map_coord_x, map_coord_y)]

        # Return map coords when pressing mouse
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l or event.key == pygame.K_k or event.key == pygame.K_j:
                    menu_close = True                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return (valid_list_of_tiles[-1])
        # Draw game
        draw_game()

        # Draw rectangle at mouse position
        for (tile_x, tile_y) in valid_list_of_tiles:
            if (tile_x, tile_y) == valid_list_of_tiles[-1]:
                draw_tile_rect(coords=(tile_x, tile_y), mark='X')
            else:
                draw_tile_rect(coords=(tile_x, tile_y))

        if radius:
            area_effect = map_find_radius(valid_list_of_tiles[-1], radius)
            for (tile_x, tile_y) in area_effect:
                draw_tile_rect(coords = (tile_x, tile_y), tile_color = constants.COLOR_RED, tile_alpha = 150)
        pygame.display.flip()
        CLOCK.tick(constants.GAME_FPS)

#   ____                           _
#  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___
# | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
# | |_| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
#  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/

## PLAYER

def gen_player(coords):

    global PLAYER

    x, y = coords
    # create the player
    container_com = component_container()
    creature_com = component_creature("Momo", base_atk=4)
    PLAYER = object_actor(x, y, "Bunny",
                       ASSETS.A_PLAYER,
                       animation_speed=1,
                       creature=creature_com,
                       container=container_com)
    
    GAME.current_objects.append(PLAYER)

def gen_item(coords):

    global GAME

    random_num = libtcod.random_get_int(0, 1, 5)
    if random_num == 1:
        new_item = gen_scroll_lightning(coords)
    elif random_num == 2:
        new_item = gen_scroll_fireball(coords)
    elif random_num == 3:
        new_item = gen_scroll_confusion(coords)
    elif random_num == 4:
        new_item = gen_weapon_sword(coords)
    elif random_num == 5:
        new_item = gen_armor_shield(coords)
    GAME.current_objects.append(new_item)

def gen_scroll_lightning(coords):
    x, y = coords
    damage = libtcod.random_get_int(0, 5, 7)
    m_range = libtcod.random_get_int(0, 7, 8)
    item_com = component_item(use_function=cast_lightning,
                        value=(damage, m_range))
    return_object = object_actor(x, y, "lightning scroll",
                              animation=ASSETS.S_SCROLL_01,
                              item=item_com)
    return return_object

def gen_scroll_fireball(coords):
    x, y = coords
    damage = libtcod.random_get_int(0, 2, 4)
    radius = 1
    m_range = libtcod.random_get_int(0, 9, 12)
    item_com = component_item(use_function=cast_fireball,
                        value=(damage, radius, m_range))
    return_object = object_actor(x, y, "fireball scroll",
                              animation=ASSETS.S_SCROLL_02,
                              item=item_com)
    return return_object

def gen_scroll_confusion(coords):
    x, y = coords
    effect_length = libtcod.random_get_int(0, 5, 10)
    item_com = component_item(use_function=cast_confusion,
                        value=effect_length) 
    return_object = object_actor(x, y, "confusion scroll",
                              animation=ASSETS.S_SCROLL_03,
                              item=item_com)
    return return_object

def gen_weapon_sword(coords):
    x, y = coords
    bonus = libtcod.random_get_int(0, 1, 2)
    equipment_com = component_equipment(attack_bonus=bonus)
    return_object = object_actor(x, y, "sword", animation=ASSETS.S_SWORD,
                              equipment=equipment_com)
    return return_object

def gen_armor_shield(coords):
    x, y = coords
    bonus = libtcod.random_get_int(0, 1, 2)
    equipment_com = component_equipment(defense_bonus=bonus)
    return_object = object_actor(x, y, "shield", animation=ASSETS.S_SHIELD,
                              equipment=equipment_com)
    return return_object

## ENEMIES
def gen_enemy(coords):

    random_num = libtcod.random_get_int(0, 1, 100)
    if random_num <= 15:
        new_enemy = gen_snake_cobra(coords)
    else:
        new_enemy = gen_snake_anaconda(coords)
    GAME.current_objects.append(new_enemy)

def gen_snake_anaconda(coords):

    x, y = coords
    base_attack = libtcod.random_get_int(0, 1, 2)
    max_health = libtcod.random_get_int(0, 5, 10)
    creature_name = "Pdskane"
    creature_com = component_creature(creature_name,
                                base_atk=base_attack,
                                hp=max_health,
                                death_function=death_snake)
    ai_com = ai_Chase()
    snake = object_actor(x, y, "anaconda",
                      ASSETS.A_SNAKE_01,
                      animation_speed=1,
                      creature=creature_com,
                      ai=ai_com)
    return snake

def gen_snake_cobra(coords):

    x, y = coords
    base_attack = libtcod.random_get_int(0, 3, 6)
    max_health = libtcod.random_get_int(0, 15, 20)
    creature_name = "Snake Chief"
    # create lobster 1
    creature_com = component_creature(creature_name,
                                base_atk=base_attack,
                                death_function=death_snake,
                                hp=max_health)
    ai_com = ai_Chase()
    snake = object_actor(x, y, "cobra",
                      ASSETS.A_SNAKE_02,
                      animation_speed=1,
                      creature=creature_com,
                      ai=ai_com)
    return snake


#   ____    _    __  __ _____   __  __    _    ___ _   _ 
#  / ___|  / \  |  \/  | ____| |  \/  |  / \  |_ _| \ | |
# | |  _  / _ \ | |\/| |  _|   | |\/| | / _ \  | ||  \| |
# | |_| |/ ___ \| |  | | |___  | |  | |/ ___ \ | || |\  |
#  \____/_/   \_\_|  |_|_____| |_|  |_/_/   \_\___|_| \_|


def game_handle_keys():

    global FOV_CALCULATE

    event_list = pygame.event.get()
    for event in event_list:

        if event.type == pygame.QUIT:
            return "Quit"

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player_moved"
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player_moved"
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player_moved"
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player_moved"
            
            if event.key == pygame.K_g:
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)

            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

            if event.key == pygame.K_p:
                menu_pause()

            if event.key == pygame.K_i:
                menu_inventory()

            if event.key == pygame.K_l:
                cast_lightning()

            if event.key == pygame.K_k:
                cast_fireball()

            if event.key == pygame.K_j:
                cast_confusion()

            

    return "no-action"

def game_initalization():
    """ Here we define the game screen and initalize pygame """

    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, ASSETS

    pygame.init()

    pygame.key.set_repeat(200, 70) # Generates multiple KEYDOWN event

    SURFACE_MAIN = pygame.display.set_mode( (constants.MAP_WIDTH*constants.CELL_WIDTH, 
                                             constants.MAP_HEIGHT*constants.CELL_HEIGHT) ) # Pygame uses tuples for values
    GAME = object_game()

    CLOCK = pygame.time.Clock()
     
    FOV_CALCULATE = True 

    ASSETS = structure_assets()

    GAME.current_map, GAME.current_rooms = create_map()
    map_place_objects(GAME.current_rooms)

    libtcod.namegen_parse("sprites/data/jice_celtic.cfg")

    # create scrolls
    gen_item((2, 2))
    gen_item((2, 3))
    gen_item((2, 4))

    # create 2 enemies
    gen_enemy((15, 15))
    gen_enemy((15, 16))

    # PLAYER = gen_player((1, 1))

    # GAME.current_objects.append(PLAYER)

def game_message(game_msg, msg_color):
    
    GAME.message_history.append((game_msg, msg_color))

def main():
    """ This function contains the main game loop"""

    game_quit = False

    player_action = "no-action"

    while not game_quit:
        # Player action definitiom
        player_action = "no-action"
        # Handle key input
        player_action = game_handle_keys()
        calculate_map_fov()
        # Draws the game


        if player_action == "Quit":
            game_quit = True

        elif player_action != "no-action":
            for objs in GAME.current_objects:
                if objs.ai:
                    objs.ai.take_turn()

        draw_game()
        # The built-in update function in pygame , like sys.clear and reprint
        pygame.display.flip()

        CLOCK.tick(constants.GAME_FPS)

    # Quit the game        
    pygame.quit()
    exit()



if __name__ == '__main__':
    game_initalization()
    main()

    
