import pygame
from constants import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size,type):
        super().__init__()
        self.image = pygame.Surface((size,size))
        if type == "T":
            self.image = TILE["D1"] #.fill((115, 230, 0))
        elif type == "F":
            self.image = TILE["G2"]
        else:
            self.image = TILE["G1"] #.fill((115, 230, 0))
        
        self.rect = self.image.get_rect(topleft = pos)