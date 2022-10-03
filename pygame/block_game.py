from functions import *
import pygame, random

class Block:
    def __init__(self, size, x, y, color, xy_offset=(0,0)):
        self.size = size
        self.rect = pygame.Rect((x*size)+xy_offset[0], (y*size)+xy_offset[1], size, size)
        self.color = color
        self.list_indexes = (x,y)

    def __repr__(self):
        return 'Block class'

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
    
    def draw_highlight(self, window):
        pygame.draw.rect(window, (255,255,255), self.rect, 3)

    def update_pos(self, xy_offset):
        self.rect.topleft = ((self.list_indexes[0]*self.size)+xy_offset[0], (self.list_indexes[1]*self.size)+xy_offset[1])

    def get_neighbours(self, list) -> tuple:
        #top
        if self.list_indexes[1]-1 > -1:
            top = list[self.list_indexes[1]-1][self.list_indexes[0]]
        else:
            top = None
        #bottom
        if self.list_indexes[1]+1 < len(list):
            bottom = list[self.list_indexes[1]+1][self.list_indexes[0]]
        else:
            bottom = None
        #left
        if self.list_indexes[0]-1 > -1:
            left = list[self.list_indexes[1]][self.list_indexes[0]-1]
        else:
            left = None
        #right
        if self.list_indexes[0]+1 < len(list[0]):
            right = list[self.list_indexes[1]][self.list_indexes[0]+1]
        else:
            right = None
        return {'top':top, 'bottom':bottom, 'left':left, 'right':right}

    def fill(self, target_color, selected, list, num=0):
        selected.append(self)
        neighbours = self.get_neighbours(list)
        for neighbour in neighbours.values():
            if neighbour != None and neighbour.color == target_color and neighbour not in selected:
                neighbour.fill(target_color, selected, list, num+1)
        return selected

class Blockgame(Stateclass):
    world = []
    block_size = 30
    rect = pygame.Rect(0, 0, block_size, block_size)
    world_colors = ((200,0,0),(0,200,0),(0,0,200))

    color = None
    higlighted_block = None

    def __init__(self, screen_size, mouse, stack):
        super().__init__(screen_size, mouse, stack)
        self.make_world()
        
    def game_loop(self):
        self.higlighted_block = None

        self.rect.center = self.mouse.pos
        for row in self.world:
            for block in row:
                if block.rect.collidepoint(self.mouse.pos):
                    self.higlighted_block = block
                        
                    if pygame.mouse.get_pressed()[0] and self.mouse.press == False:
                        if self.color == None:#pick up if hand is empty
                            self.color = block.color
                            block.color = (0,0,0)
                        else:#has an color on hand
                            if block.color == (0,0,0):#if player places an color on an empty space
                                block.color = self.color
                                self.color = None
                            else:#swap colors
                                self.color, block.color = block.color, self.color
                    elif pygame.mouse.get_pressed()[2] and self.mouse.press == False:
                        selected_blocks = []
                        target_color = block.color
                        block.fill(target_color, selected_blocks, self.world)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.make_world()
            if event.key == pygame.K_ESCAPE:
                Pauseclass(self.screen_size, self.mouse, self.stack).enter_state(self.stack)

    def resize(self, screen_size):
        self.screen_size = screen_size
        self.update_world()

        #updates border around blocks
        border_x = int((self.screen_size[0]%self.block_size)/2)
        border_y = int((self.screen_size[1]%self.block_size)/2)
        for row in self.world:
            for block in row:
                block.update_pos((border_x, border_y))

    def draw(self, window):
        window.fill((0,0,0))
        #draws blocks
        for row in self.world:
                for block in row:
                    block.draw(window)

        if self.higlighted_block != None:
            self.higlighted_block.draw_highlight(window)
        if self.color != None:
            pygame.draw.rect(window, self.color, self.rect)

    def make_world(self):
        #makes the world from scratch
        #everything gets deleted
        border_x = int((self.screen_size[0]%self.block_size)/2)
        border_y = int((self.screen_size[1]%self.block_size)/2)
        self.world.clear()
        for y in range(int(self.screen_size[1]/self.block_size)):
            self.world.append([Block(self.block_size, x, y, random.choice(self.world_colors), (border_x, border_y)) for x in range(int(self.screen_size[0]/self.block_size))])

    def update_world(self):
        #adds blocks if the screen gets larger or removes them if it gets smaller
        height = int(self.screen_size[1]/self.block_size)
        width = int(self.screen_size[0]/self.block_size)
        #height
        if height < len(self.world): #remove height
            amount = len(self.world) - height
            for i in range(amount):
                index = len(self.world) - 1
                self.world.remove(self.world[index])
        elif height > len(self.world): #add height 
            amount = height - len(self.world)
            for i in range(amount):
                y = len(self.world)
                self.world.append([Block(self.block_size, x, y, random.choice(self.world_colors)) for x in range(len(self.world[0]))])
        #width
        if width < len(self.world[0]): #remove width
            amount = len(self.world[0]) - width
            for index in range(len(self.world)):
                for i in range(amount):
                    self.world[index].remove(self.world[index][len(self.world[index])-1])
        elif width > len(self.world[0]): #add width
            amount = width - len(self.world[0])
            for index in range(len(self.world)):
                for i in range(amount):
                    y = index
                    x = len(self.world[index])
                    self.world[index].append(Block(self.block_size, x, y, random.choice(self.world_colors)))

class Pauseclass(Stateclass):
    def __init__(self, screen_size, mouse, stack):
        super().__init__(screen_size, mouse, stack)
        self.shadow = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        self.shadow.set_alpha(100)
        self.buttoncontroller = Buttoncontroller([Buttonclass('Continue'), Buttonclass('To title')])
        self.buttoncontroller.set_center((self.screen_size[0]/2, self.screen_size[1]/2))

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state(self.stack)
            

    def resize(self, screen_size):
        self.screen_size = screen_size
        self.prev_state.resize(self.screen_size)
        self.shadow = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        self.shadow.set_alpha(100)
        self.buttoncontroller.set_center((self.screen_size[0]/2, self.screen_size[1]/2))

    def draw(self, window):
        self.prev_state.draw(window)
        pygame.draw.rect(self.shadow, (0,0,50), pygame.Rect(0, 0, self.screen_size[0], self.screen_size[1]))
        window.blit(self.shadow, (0,0))
        self.buttoncontroller.draw(window)

    def menu(self, index):
        if index == 0:
            self.exit_state(self.stack)
        if index == 1:
            self.go_to_first(self.stack)