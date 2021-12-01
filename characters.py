import pygame
import media
from brain import *
from pygame.math import Vector2
from random import randint
from constants import *

class Character(pygame.sprite.Sprite):
    ''' abstract class for every character that will be blitted in the game
    attributes: x,y,image,rect,
    methods:  __init__, update, __str__, draw '''
    WORLD = pygame.sprite.Group()
    def __init__(self, x,y,name):
        super(Character,self).__init__()
        self.r = Vector2(x,y) # Position Vector
        self.v = 2 # Speed
        self.dest = Vector2(0,0) # Position of the goal
        self.image = CHARACTER_IMG[name]
        self.rect = self.image.get_rect()
        self.type = name
        
    def update(self, *a,**b): 
        pass
    

    def import_character_assets(self,c_path):
        for animation in self.animations.keys():
            full_path = c_path+animation
            self.animations[animation] = import_folder(full_path)

class Player(Character):
    class animate_catch(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = CHARACTER_IMG["cloud"]
            self.rect = self.image.get_rect(center = pos)
            
            self.angle = 0
            self.w = 2.5
            
        def update(self):
            self.angle += self.w
            self.image = pygame.transform.rotate(CHARACTER_IMG["cloud"],self.angle)
            
            if self.angle > 360:
                self.kill()
            
    def __init__(self, x,y):
        super(Player,self).__init__(x,y,"bruno")
        self.v = 2.5
        self.direction = Vector2(0,0)
        self.status = "idle"
        self.group_catched = pygame.sprite.Group()
        
        self.animations = {'idle':[],'walking':[],'catching':[]}
        self.animation_speed = .15
        self.frame_index = 0
        self.import_character_assets('media/Bruno/')
        self.image = self.animations[self.status][int(self.frame_index)]
        self.t = False
        self.facing_right = True

    def move(self):
        
        self.r += self.v*self.direction
        
        if self.r.x < L_LIM:
            self.r.x = L_LIM
        elif self.r.x > R_LIM:
            self.r.x = R_LIM
        if self.r.y < U_LIM:
            self.r.y = U_LIM
        elif self.rect.bottom > D_LIM:
            self.r.y = D_LIM
        
        self.rect.midbottom = self.r
        

    def get_status(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.status = "catching"
        else:
            if self.direction != (0,0):
                self.status = "walking"
            else:
                self.status = "idle"
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
    
    def attack(self):
        captured = {k:v for (k,v) in zip(BUG_NAMES,[0,0,0,0,0])}
        
        self.rect.move_ip(20*self.direction.x,0)
        for b in pygame.sprite.spritecollide(self,Character.WORLD,False):
            if b.type in BUG_NAMES:
                if randint(1,2) == 1:
                    captured[b.type]+=1
                    self.group_catched.add(Player.animate_catch(b.r))
                    b.kill()
                    
        self.rect.move_ip(-20*self.direction.x,0)
        return captured
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if self.direction != (0,0):
            self.direction.normalize_ip()


    def update(self):
        self.get_input()
        self.move()
        self.get_status()
        self.animate()
        self.group_catched.update()
    
    

class Bug(Character):
    ''' Class Bug '''
    def __init__(self, name,pos):
        x,y = pos
        super(Bug,self).__init__(x,y,name)
        self.act_dir = None
        self.brain = StateMachine()
        self.rect.center = (self.r.x,self.r.y)
        self.attention = pygame.sprite.GroupSingle()
        self.ORIG_VIEW_ANGLE = Vector2(0,0)
        
    def set_new_dest(self,dest):
    # dest: Vector2 => set a new dest and change the angle
        if dest == self.dest:
            return
        
        self.dest = dest
         
        if self.r != self.dest:
            self.dir_move = (self.dest - self.r).normalize()
            self.angle = self.dir_move.angle_to(self.ORIG_VIEW_ANGLE)
            self.image = pygame.transform.rotate(CHARACTER_IMG[self.type],self.angle)
        
    def update(self, **args): 
        self.brain.think()
        
        if self.v > 0. and self.r != self.dest:
            self.r += self.v * (self.dest - self.r).normalize()
            self.rect.center = self.r

    
    def distance_to_dest(self):
        return self.dest.distance_to(self.r)

    def nearest_sprites(self,distance):
        def fun(sprite1,sprite2):
            return sprite1 is not sprite2 and (sprite1.r.distance_to(sprite2.r)) < distance
        
        return pygame.sprite.spritecollide(self,self.WORLD,False,collided = fun)
    
    def most_close_to(self,sprite_group,type=None):
        min = None
        for spr in sprite_group:
            if type is None or spr.type == type:
                if min is None or spr.r.distance_to(self.r) < min.r.distance_to(self.r):
                    min = spr
        
        return min
    
    def get_attention(self):
        return self.attention.sprites()


class Cockroach(Bug):   
    def __init__(self,pos = (0,0)):
        super(Cockroach,self).__init__("Cockroach",pos)
        self.brain.add_state(ExploringState(self))
        self.brain.add_state(EatingState(self))
        self.brain.add_state(SeekingState(self))
        self.brain.add_state(HidingState(self))
        self.brain.set_state("exploring")
        self.ORIG_VIEW_ANGLE = Vector2(0,1) # 90
        self.set_new_dest(Vector2(randint(0, WIDTH),randint(0, HEIGHT)))
        
    def eat_crop(self,crop):
        if randint(1, 100) == 1:
            crop.attacked()

class Crop(pygame.sprite.Sprite):
    number = 0
    CROP_GROUP = pygame.sprite.Group()
    def __init__(self, x=0, y=0):
        Crop.number+=1
        super(Crop,self).__init__(self.CROP_GROUP)
        self.r = Vector2(x,y)
        self.image = CHARACTER_IMG["crop"]
        self.rect = self.image.get_rect()
        self.rect.center = self.r
        self.life = 4 # Max HEALTH of all crop
        self.type = "Crop"
    
    def attacked(self):
        if self.isAlive():
            self.life -= 1
        if not self.isAlive():
            Crop.number-=1
            self.kill()
    
    def isAlive(self):
        return self.life > 0
    
class Hole(pygame.sprite.Sprite):
    ELEMENTS = pygame.sprite.Group()
    def __init__(self,pos,limit=3):
        super(Hole,self).__init__(self.ELEMENTS)
        self.image = pygame.transform.scale2x(CHARACTER_IMG["hole"])
        self.rect = self.image.get_rect()
        self.BUGS = pygame.sprite.Group()
        self.type = "Hole"
        
        self.r = Vector2(pos)
        self.rect.center = self.r
        if limit <= 0:
            self.limit = 3
        else:
            self.limit = limit
    
    def goIn(self,bug):
        if not self.full():
            self.BUGS.add(bug)
    
    def full(self):
        return len(self.BUGS) >= self.limit
    
    def goOut(self,bug):
        self.BUGS.remove(bug)

    def update(self):
        self.BUGS.update()
        
    def __contains__(self,item):
        return item in self.BUGS