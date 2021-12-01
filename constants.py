# Constant.py
import pygame
from media import *

CLOCK = pygame.time.Clock()
GET_TICK = pygame.time.get_ticks

SCREEN_SIZE = (WIDTH, HEIGHT) = (600, 400)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

LIMIT = (R_LIM,L_LIM,U_LIM,D_LIM) = (WIDTH-80,80,50,HEIGHT-50)

TILE_SIZE = 32

TILE = {'G1': pygame.transform.scale(load_png("tile-grass1.png"),(TILE_SIZE,TILE_SIZE)),
        'D1': pygame.transform.scale(load_png("tile-dirt-cc.png"),(TILE_SIZE,TILE_SIZE)),
        'G2': pygame.transform.scale(load_png("tile-grass2.png"),(TILE_SIZE,TILE_SIZE)),
        'C1': load_png("tile-crop-2.png")}

                

CHARACTER_IMG = {'Bee': load_png('bee.png'),
             'Cockroach': load_png('Cockroach1.png'),
             'bruno': load_png('bruno.png'),
             'crop': pygame.transform.scale(load_png("tile-crop-2.png"),(20,20)),
             'hole': load_png("hole.png"),
             'cloud':  pygame.transform.scale(load_png("cloud.png"),(TILE_SIZE,TILE_SIZE))}
             
BUG_NAMES = ["Cockroach","Bee","Ant","Spider","Ladybug"]
LITTLE_THINGS = ["Crop","Hole"]

# T -> Tierra Dirt
# B -> BeeHive
# H -> Hormiguero
# F -> Flower
# G -> Grass

GARDEN_MAP = [
'T  F        F   F T',
'T      F         FT',
'TF TT       TT    T',
'T  TT     F     F T',
'T  TT  T TTT F    T',
'T      TTT T      T',
'T  F    TTTT     FT',
'T      TTTT    T  T',
'T  F   T TTT   T  T',
'T             TT  T',
'T   T    F   F    T',
'TF F          F   T',
'TTTTTTTTTTTTTTTTTTT']

ONLY_GARDEN = [
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ',
'                   ']