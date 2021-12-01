# Brain.py
from random import randint
import pygame
from pygame.math import Vector2
from constants import *

class State():
    ''' State Object:
        Abstract class. Refers to them so it will be easy to make states to NPC
    '''
    def __init__(self,name):
        self.name = name
        
        
    def do_actions(self):
        ''' do the actions for this state '''
        print("do_actions not implemented in "+self.name)
        pass
    
    def check_conditions(self):
        print("check_conditions not implemented in "+self.name)
        pass
    
    def entry_actions(self):
        print("entry_actions not implemented in "+self.name)
        pass
    
    def exit_actions(self):
        print("exit_actions not implemented in "+self.name)
        pass
        
class StateMachine():
    '''The brain and the manager for every State'''
    def __init__(self):
        self.states = {}  # Stores the states
        self.active_state = None  # The currently active state
        
    def add_state(self,state):
        #Add a state to the internal dictionary
        self.states[state.name] = state
    
    def think(self):
    # Only continue if there is an active state
        if self.active_state is None:
            return
        
        # Perform the actions of the active state, and check conditions
        self.active_state.do_actions()
        
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
    
    def set_state(self, new_state_name):
        # Change states and perform any exit / entry actions
        if self.active_state is not None:
            self.active_state.exit_actions()
        print(new_state_name)
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()
 
## Bugs crop-eater states
class ExploringState(State):
    def __init__(self,bug):
        State.__init__(self,"exploring")
        # Set the bug that this State will manipulate
        self.bug = bug
    
    def random_destination(self):
        self.bug.set_new_dest(Vector2(randint(L_LIM,R_LIM,),
                                      randint(U_LIM,D_LIM)))
    
    def entry_actions(self):
        # Start with random speed and heading
        self.bug.v = 3 + randint(-1, 1)
        self.random_destination()

    def do_actions(self):
        # Change direction, 1 in 20 calls
        if randint(1, 20) == 1:
            self.random_destination()
      
    def attention_to_near_hole(self):
        bug = self.bug
        for c in bug.WORLD:
            if c.type == 'Hole':
                near_hole = bug.most_close_to(c.ELEMENTS)
                if near_hole.full():
                    print("I cant be in that hole")
                    return None
                bug.attention.add(near_hole)
                print("I will go to that hole")
                return "seeking"

    def check_conditions(self): # !!
    # if crop founded at a ratio of 22 pixels
    # then assing the nearest crop to the bug's attention
        bug = self.bug
        l = bug.nearest_sprites(distance = 22)
        #1
        for rl in l:
            near = bug.most_close_to(l,"bruno")
            if rl.type == "Crop":
                bug.attention.add(rl)
                if near is not None:
                    print("nono... better to run")
                    continue
                print("yummy! a delicious crop!")
                return "seeking"
            if rl.type == "Hole":
                if near is not None or randint(1,500) == 1:
                    print("uh!? a HOLE!")
                    return self.attention_to_near_hole()
    def exit_actions(self):
        pass
        
class SeekingState(State):
    def __init__(self,bug):
        State.__init__(self,"seeking")
        self.bug = bug
        
    def entry_actions(self):
        self.bug.v += 1 
        x = self.bug.dest
        for c in self.bug.get_attention():
            x = c.r
            if c.type == "Hole" and c.full():
                self.bug.attention.empty()
        self.bug.set_new_dest(x)
            
    def do_actions(self):
        for c in self.bug.get_attention():
            if c.type == "Hole" and c.full():
                print("OH! I cant go inside :(")
                self.bug.attention.empty()

    def check_conditions(self):
        if len(self.bug.attention) == 0:
            return "exploring"
        for b in self.bug.get_attention():
            if (self.bug.distance_to_dest() < 10.0):
                if b.type == "Hole":
                    print("Im in the hole")
                    return "hiding"
                else:
                    print("im gonna eat this")
                    return "eating"
            
    def exit_actions(self):
        self.bug.v -= 1
        
class EatingState(State):
    def __init__(self,bug):
        State.__init__(self,"eating")
        self.bug = bug

    def entry_actions(self):
        self.v = 0
        self.isBrunoHere = False
        for c in self.bug.get_attention():
            self.bug.set_new_dest(c.r)
            
    
    def do_actions(self):
        bug = self.bug
        for c in bug.get_attention():
            bug.eat_crop(c)
            n = bug.most_close_to(bug.nearest_sprites(35),"bruno")
            if n is not None: # el problema de que gire mucho está aqui !!!
                self.isBrunoHere = True
                print("Oh no, its Bruno. RUN!")
                
    
    def search_hole(self):
        bug = self.bug
        near_hole = bug.most_close_to(bug.WORLD,"Hole")
        holes = near_hole.ELEMENTS.sprites()
        while(near_hole is None or near_hole.full()):
            if near_hole is not None:
                holes.remove(near_hole)
            near_hole = bug.most_close_to(holes)
        
        return near_hole
    
    def check_conditions(self):
        bug = self.bug
        if not bug.attention:
            print("Nothing to eat!")
            return "exploring"
        if self.isBrunoHere:
            near_hole = self.search_hole()
            if near_hole is not None:
                print("Now! go to that hole!")
                bug.attention.add(near_hole)
                return "seeking"
    def exit_actions(self):
        pass        
        
class HidingState(State):
    ''' STATE WHEN AN BUG IS HIDDEN INSIDE SOMETHING'''
    def __init__(self,bug):
        State.__init__(self,"hiding")
        self.bug = bug
        
    def entry_actions(self):
        self.v = 0
        self.prev_group = self.bug.groups()
        self.bug.kill()
        
        for b in self.bug.get_attention():
            self.hole = b
        self.hole.goIn(self.bug)
        print(self.bug.type, len(self.prev_group), len(self.hole.BUGS))

    def do_actions(self):
        bug = self.bug
        n = filter((lambda spr: spr.type != "Hole"),bug.nearest_sprites(80))
        near = bug.most_close_to(n)
        if randint(1,200) == 1 and near is not None and near.type != "bruno":
            self.hole.goOut(bug)
        
    def check_conditions(self):
        if self.bug not in self.hole:
            return "exploring"

    def exit_actions(self):
        self.bug.r = Vector2(self.hole.r)
        self.bug.add(self.prev_group)
        
        
##