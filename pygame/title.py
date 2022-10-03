from functions import *
from block_game import Blockgame
import pygame, sys
pygame.init()

class Titleclass(Stateclass):
    def __init__(self, screen_size, mouse, stack):
        super().__init__(screen_size, mouse, stack)
        self.buttoncontroller = Buttoncontroller([Buttonclass('Start game'),Buttonclass('How to play'),Buttonclass('Quit')])
        self.buttoncontroller.set_center((self.screen_size[0]/2,self.screen_size[1]/2))

    def game_loop(self):
        if self.mouse.active:
            index = self.buttoncontroller.game_loop(self.mouse)
            if index != None:
                self.menu(index)
            
    def event(self, event):
        #button controller
        if self.mouse.active == False:
                index = self.buttoncontroller.event(event)
                if index != None:
                    self.menu(index)    

    def resize(self, screen_size):
        self.screen_size = screen_size
        self.buttoncontroller.set_center((self.screen_size[0]/2,self.screen_size[1]/2))
            
    def draw(self, window):
        window.fill((50,50,100))
        self.buttoncontroller.draw(window)

    def menu(self, index):
        if index == 0:
            Blockgame(self.screen_size, self.mouse, self.stack).enter_state(self.stack)
        elif index == 1:
            Howclass(self.screen_size, self.mouse, self.stack).enter_state(self.stack)
        elif index == 2:
            pygame.quit()
            sys.exit()

class Howclass(Stateclass):
    def __init__(self, screen_size, mouse, stack):
        super().__init__(screen_size, mouse, stack)
        self.back_button = Buttonclass('Back')
        self.back_button.rect.center = (self.screen_size[0]/2, self.screen_size[1]-50)
        self.how_text0 = Textclass('Press F1 to switch to fullscreen.')
        self.how_text0.rect.center = (self.screen_size[0]/2, 50)
        self.how_text1 = Textclass('Press S to randomize the screen when in game.')
        self.how_text1.rect.center = (self.screen_size[0]/2, 100)
        self.how_text2 = Textclass('Pick up blocks and place them somewear else.')
        self.how_text2.rect.center = (self.screen_size[0]/2, 150)

    def game_loop(self):
        if self.back_button.update(self.mouse):
            self.exit_state(self.stack)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state(self.stack)

    def resize(self, screen_size):
        self.screen_size = screen_size
        self.back_button.rect.center = (self.screen_size[0]/2, self.screen_size[1]-50)
        self.how_text0.rect.center = (self.screen_size[0]/2, 50)
        self.how_text1.rect.center = (self.screen_size[0]/2, 100)
        self.how_text2.rect.center = (self.screen_size[0]/2, 150)

    def draw(self, window):
        window.fill((50,50,100))
        self.back_button.draw(window)
        self.how_text0.draw(window)
        self.how_text1.draw(window)
        self.how_text2.draw(window)

class Worldsettings(Stateclass):
    def __init__(self, screen_size, mouse):
        super().__init__(screen_size, mouse)

    def game_loop(self):
        pass

    def event(self, event):
        pass

    def resize(self, screen_size):
        pass

    def draw(self, window):
        pass