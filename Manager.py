''' * Module: Manager
This module have 2 classes:
 - Scene class is an abstract class, a template for the new classes scenes.
 - SceneDirector class is a helper class, applying the functions of Scene
   and changing the scene.

 So this module have the classes that makes the game to work'''


class Scene(object):
    '''Class Scene is abstract, so needs to heritate.
    It is in all the videogame: pause, menu, levels, etc etc etc
    handle_events  ---> update ---> render
    '''

    def __init__(self):
        '''initiate attributes that will go brrr your game'''
        self.director = None

    def handle_events(self, events):
        '''Handling Users events (and maybe by other manager)'''
        raise NotImplementedError

    def update(self):
        ''' updating all attributes of Scene before updating it'''
        raise NotImplementedError

    def render(self, screen):
        '''for rendering all the stuff in the screen'''
        raise NotImplementedError


class SceneDirector(object):
    '''Director assings a scene to work'''

    def __init__(self, scene):
        self.go_to(scene)

    def go_to(self, scene):
        '''Every director have to change scene'''
        self.scene = scene
        if scene is not None:
            self.scene.director = self

    def loop(self, events, screen):
        '''Light! Camera! Action! This do all actions of an Scene Object.
        This goes inside the main loop of the game'''
        if self.scene is not None:
            self.scene.handle_events(events)
            self.scene.update()
            self.scene.render(screen)

