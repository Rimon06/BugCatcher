import pygame
from pygame.locals import *
import os
import sys

colors = {'white': (000, 000, 000),
          'W1':    (250, 235, 225),
          'black': (255, 255, 255),
          'red':   (255, 000, 000)}
             
def load_png(name,path='media'):
    """ Load image and return image object"""
    fullname = os.path.join(path, name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image

def load_music(name,path='media'):
    fullname = os.path.join(path,'sound',name)
    return pygame.mixer.Sound(fullname)

def import_folder(path):
    surface_list = []
    for _,_,img_files in os.walk(path):
        for image in img_files:
            image_surf = load_png(image,path)
            surface_list.append(image_surf)
            
    return surface_list


def put_string(texto, screen, coord, fontsize = 16, color = colors['W1']):
    font = pygame.font.Font(os.path.join("media","Montserrat.ttf"), fontsize)
    text = font.render(texto, 1, color)
    text_rect=text.get_rect(center = coord)
    screen.blit(text, text_rect)
