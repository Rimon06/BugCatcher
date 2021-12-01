'''B.U.G Backyard Under Guard
# Game made by Rider of Sun
# TODO: Complete the game
'''

import pygame
# Initialize the pygame
pygame.init()
from constants import *
import Manager
import characters
import media
from media import load_png
from random import randint, choice
from sys import exit
import tiles


# Title and Icon
pygame.display.set_caption("B.U.G. Bruno is Under Guard")
icon = media.load_png("crop.png")
pygame.display.set_icon(icon)

#  --Title Scene--
class TitleScene(Manager.Scene):
    def __init__(self):
        BUTTON_HEIGHT = 275
        super(TitleScene, self).__init__()
        
        self.background = media.load_png("title2.png")
        img1 = media.load_png("cartel-jugar.png")
        box1 = img1.get_rect(topleft = (50,BUTTON_HEIGHT)) 
        
        img2 = media.load_png("cartel-salir.png")
        box2 = img2.get_rect(topleft = (450,BUTTON_HEIGHT))
        
        self.background.blit(img1,box1)
        self.background.blit(img2,box2)
        
        self.icon = CHARACTER_IMG["Cockroach"]
        self.box3 = self.icon.get_rect()
        self.iconpos = [box1.midleft,box2.midleft]
        self.op = 0
        
        self.music = load_music("slide-guitar.wav")
        self.music.play(loops=-1)
        self.music.set_volume(0.5)
        
    def render(self, screen):
        screen.blit(self.background, (0, 0))
        
        screen.blit(self.icon,self.icon.get_rect(midright = self.iconpos[self.op]))
        
    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.director.go_to((ByeScene()))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.op = (self.op - 1) % 2
                if e.key == pygame.K_RIGHT:
                    self.op = (self.op + 1) % 2
                if e.key in [pygame.K_SPACE]:
                    top = load_music("sound-correct.wav")
                    top.play()
                    top.set_volume(0.5)
                    self.music.stop()
                    if self.op % 2 == 0:
                        self.director.go_to(PlayGameScene())
                    else:
                        self.director.go_to(ByeScene())
                

#  --Bye Scene--
class ByeScene(Manager.Scene):
    def render(self, screen):
        pass

    def update(self):
        print("Good Bye!!")
        pygame.quit()
        exit()

    def handle_events(self, events):
        pass

#  --PlayGameScene--
class PlayGameScene(Manager.Scene):
    def __init__(self):
        super(PlayGameScene, self).__init__()
        self.setup_map(GARDEN_MAP)
        
        self.player = characters.Player(WIDTH/2, U_LIM+100)
        
        self.Bugs = pygame.sprite.Group()
        
        self.WORLD = characters.Character.WORLD
        self.WORLD.add(self.player)
        self.WORLD.add(characters.Crop(randint((WIDTH/4),WIDTH*(3/4)),randint(HEIGHT/4,HEIGHT*(3/4))) for _ in range(12))
        self.WORLD.add(characters.Hole((randint(L_LIM,R_LIM),randint(U_LIM,D_LIM)),2) for _ in range(5))
        
        self.score = {k:v for (k,v) in zip(BUG_NAMES,[0,0,0,0,0])}
        self.FLAG = False #for debug
        self.round = 1;
        
        self.music = media.load_music("funk-loop.wav")
        self.music.play(loops=-1)
        
        self.boxbug = media.load_png("cartel-bug.png")
        self.rectbug = self.boxbug.get_rect(topleft = (50,350))
        self.boxcrop = media.load_png("cartel-crop.png")
        self.rectcrop = self.boxcrop.get_rect(topleft = (450,350))
        self.boxtime = media.load_png("cartel.png")
        self.recttime = self.boxtime.get_rect(topleft = (250,1))
        
        self.countdown = GET_TICK()
        self.start = -3
    
    def setup_map(self,layout):
        self.tiles = pygame.sprite.Group()
        for row_i,row in  enumerate(layout):
            for col_i,cell in  enumerate(row):
                x = TILE_SIZE * col_i
                y = TILE_SIZE * row_i
                self.tiles.add(tiles.Tile((x,y),TILE_SIZE,cell))
           
    def render(self, screen):
        self.tiles.draw(screen)
        
        if self.start < 60 and characters.Crop.number > 0:
            self.WORLD.draw(screen)
            self.player.group_catched.draw(screen)
            
            screen.blit(self.boxbug,self.rectbug)
            media.put_string('x'+str(self.score['Cockroach']),screen,self.rectbug.center,35) 
            
            screen.blit(self.boxcrop,self.rectcrop)
            N = characters.Crop.number
            media.put_string('x'+str(N),screen,self.rectcrop.center,35) 
            
            screen.blit(self.boxtime,self.recttime)
            if self.start < 0:
                media.put_string(str(-self.start), screen, screen.get_rect().center, 50)
            elif self.start == 0:
                media.put_string("START!", screen, screen.get_rect().center, 50)
            else:
                media.put_string(str(60-self.start), screen, self.recttime.center, 50)
            return
        else: # when the game ends!
            color = (58,33,21)
            rect = screen.get_rect()
            if self.start >= 60:
                rect.y -= 50
                media.put_string("YOU WIN!", screen, rect.center,50,color)
                rect.y += 15
                media.put_string(":D",screen,rect.center,15,color)
                rect.y -= 15
                rect.y += 50
                media.put_string(f"CROPS SAVED: {characters.Crop.number}",screen,rect.center,50,color)
            else:
                rect.y -= 50 
                media.put_string("WE LOSE OUR CROPS!",screen,rect.center,50,color)
                rect.y += 25
                media.put_string("oh my carrots :,(",screen,rect.center,15,color)
            rect.y += 50
            media.put_string(f"BUGS CATCHED: {self.score['Cockroach']}",screen,rect.center,50,color)
            rect.y += 40
            media.put_string(f"press 'f' to go to menu",screen,rect.center,15,color)
            
    def update(self):
        current_time = GET_TICK()
        
        if (current_time - self.countdown > 1000):
            self.countdown = GET_TICK() 
            if characters.Crop.number > 0:
                self.start += 1
        if self.start > 0 and self.start < 60 and characters.Crop.number > 0:
            self.Bugs.update()
            characters.Hole.ELEMENTS.update()
            
            num_bugs = len(self.Bugs)
            for h in characters.Hole.ELEMENTS:
                num_bugs += len(h.BUGS)

            if randint(1,40) == 1 and num_bugs  < 15:
                new = characters.Cockroach(self.choice())
                self.Bugs.add(new)
                self.WORLD.add(new)
            self.player.update()
        
    def choice(self):
        return choice([(randint(L_LIM,L_LIM+40),randint(U_LIM,D_LIM)),
                       (randint(R_LIM-40,R_LIM),randint(U_LIM,D_LIM)),
                       (randint(L_LIM,R_LIM),randint(U_LIM,U_LIM+30)),
                       (randint(L_LIM,R_LIM),randint(D_LIM-30,D_LIM))])
    
    def endPlayGameScene(self):
        self.WORLD.empty()
        characters.Hole.ELEMENTS.empty()
        characters.Crop.CROP_GROUP.empty()
        characters.Crop.number -= characters.Crop.number
        self.music.stop()
        self.director.go_to(TitleScene())
        
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.start < 60 or characters.Crop.number == 0:
                        new = self.player.attack()
                        for k,v in new.items():
                            self.score[k] += v
                if e.key == pygame.K_f and (self.start > 60 or characters.Crop.number == 0):
                    self.endPlayGameScene()



manager = Manager.SceneDirector(TitleScene())
while True:
    CLOCK.tick(60)

    if pygame.event.get(pygame.QUIT):
        manager.go_to(ByeScene())
    # Director tells Scene Objects to do their stuff
    manager.loop(pygame.event.get(), SCREEN)
    pygame.display.flip()

