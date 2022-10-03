import pygame

class Stateclass: # mother class of all scenes
    def __init__(self, screen_size, mouse, stack):
        self.screen_size = screen_size
        self.mouse = mouse
        self.stack = stack
        self.prev_state = None

    def enter_state(self, stack):
        if len(stack) > 1:
            self.prev_state = stack[-1]
        stack.append(self)

    def exit_state(self, stack):
        stack.pop()
        stack[-1].resize(self.screen_size)

    def go_to_first(self, stack):
        while len(stack) > 1:
            stack.pop()
        stack[-1].resize(self.screen_size)

class Mouseclass: # class for the mouse
    pos = (0,0)
    press = False
    active = True

    def update(self):
        pygame.mouse.set_visible = self.active
        if self.active:
            self.pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                self.press = True
            elif not pygame.mouse.get_pressed()[0] or not pygame.mouse.get_pressed()[2]:
                self.press = False

class Textclass: # makes text on the screen
    def __init__(self, text, AA=True, color=(255,255,255), size=50):
        self.font = pygame.font.SysFont(None, size)
        self.text = text
        self.AA = AA
        self.color = color
        self.rect = self.font.render(self.text, self.AA, self.color).get_rect()

    def draw(self, window):
        window.blit(self.font.render(self.text, self.AA, self.color), self.rect)

    def get_height(self):
        self.font.render(self.text, self.AA, self.color).get_height()

    def get_width(self):
        self.font.render(self.text, self.AA, self.color).get_width()

class Buttonclass: # makes a button 
    def __init__(self, text, AA=True, colors=((255,255,255),(200,200,255)), size=60):
        self.font = pygame.font.SysFont(None, size)
        self.text = text
        self.AA = AA
        self.colors = colors
        self.color_index = 0
        self.rect = self.font.render(self.text, self.AA, self.colors[self.color_index]).get_rect()

    def draw(self, window):
        window.blit(self.font.render(self.text, self.AA, self.colors[self.color_index]), self.rect)

    def update(self, mouse):
        if self.rect.collidepoint(mouse.pos):
            self.color_index = 1
            if pygame.mouse.get_pressed()[0] and mouse.press == False:
                return True
            else:
                return False
        else:
            self.color_index = 0
            return False

    def get_height(self):
        return self.font.render(self.text, self.AA, self.colors[self.color_index]).get_height()

    def get_width(self):
        return self.font.render(self.text, self.AA, self.colors[self.color_index]).get_width()

class Buttoncontroller:
    def __init__(self, buttons):
        self.buttons = buttons
        self.current_index = 0
        #finds the largest width and height
        self.width = 0
        self.height = 0
        for button in self.buttons:
            if button.get_width() > self.width:
                self.width = button.get_width()
            if button.get_height() > self.height:
                self.height = button.get_height()
        
        self.rect = pygame.Rect(0, 0, self.width, self.height*len(self.buttons))
        self.set_buttons()

    #sets the button rects to the button controller
    def set_buttons(self):
        for index in range(len(self.buttons)): #old code self.width/2+self.rect.center[0], self.height*index+self.height/2+self.rect.center[1]
            self.buttons[index].rect.center = self.width/2+self.rect.x, self.height*index+self.height/2+self.rect.y

    #sets the center point of the button controller
    def set_center(self, x_and_y):
        self.rect.center = x_and_y
        self.set_buttons()

    #///////////////
    #button controll
    #///////////////

    #draws all buttons
    def draw(self, window):
        for button in self.buttons:
            button.draw(window)

    def game_loop(self, mouse):
        for button in self.buttons:
            if button.update(mouse):
                return self.buttons.index(button)
        
    def event(self, event):
        for button in self.buttons:
            button.color_index = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move(-1)
            elif event.key == pygame.K_DOWN:
                self.move(1)
            if event.key == pygame.K_RETURN:
                return self.current_index
        self.buttons[self.current_index].color_index = 1

    def move(self, number):
        self.current_index += number
        if self.current_index < 0:
            self.current_index = len(self.buttons)-1
        elif self.current_index > len(self.buttons)-1:
            self.current_index = 0