import pygame
import libtcodpy as libtcod

pygame.init()


# Game size definitions
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864
CELL_WIDTH = 32
CELL_HEIGHT = 32
GAME_FPS = 60

# Game color definitions
COLOR_BLACK = (0, 0, 0) # RGB colors
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# Fonts


# Messages
NUM_MESSAGES = 8

# FOV settings
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10


#MAP TILES
MAP_WIDTH = 36
MAP_HEIGHT = 20
MAP_MAX_NUM_ROOMS = 15

ROOM_MAX_HEIGHT = 10
ROOM_MIN_HEIGHT = 4
ROOM_MAX_WIDTH = 6
ROOM_MIN_WIDTH = 5

#Sprites PLAYER
# S_PLAYER = pygame.image.load( "bunny.png" )

# #Sprites ENEMY
# S_OGRE = pygame.image.load( "ogre.png" )
# S_BARBARIAN = pygame.image.load( "barbarian.png" )
# S_BLACKDRAGON = pygame.image.load( "blackdragon.png" )
# S_DEVIL = pygame.image.load( "devil.png" )
# S_WIZARDRAT = pygame.image.load( "wizardrat.png" )
# S_GREENDRAGON = pygame.image.load( "greendragon.png" )
# S_MEDUSA = pygame.image.load( "medusa.png" )
# S_RYVEN = pygame.image.load( "ryven.png" )

#Sprites ITEM



#Sprites MAP
