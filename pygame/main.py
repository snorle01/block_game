from title import *
import pygame, sys
pygame.init()

screen_size = (1000,1300)
game_window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
fullscreen = False
state_stack = []

#scene
mouse = Mouseclass()
state_stack.append(Titleclass(screen_size, mouse, state_stack))

#/////////
#game loop
#/////////
while True:
    #event handling
    for event in pygame.event.get():
        state_stack[-1].event(event)

        #quit
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        #normal screen rezising
        if event.type == pygame.VIDEORESIZE and not fullscreen:
            screen_size = (event.w, event.h)
            game_window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
            state_stack[-1].resize(screen_size)
        #mouse movement
        if event.type == pygame.MOUSEMOTION:
            mouse.active = True

        #keyboard events
        if event.type == pygame.KEYDOWN:
            #set to fullscreen
            if event.key == pygame.K_F1: 
                fullscreen = not fullscreen
                if fullscreen:
                    game_window = pygame.display.set_mode((game_window.get_width(), game_window.get_height()), pygame.FULLSCREEN)
                    screen_size = (game_window.get_width(), game_window.get_height())
                    state_stack[-1].resize(screen_size)
                else:
                    screen_size = (1000,1300)
                    game_window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
                    state_stack[-1].resize(screen_size)
            #deactivate mouse
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                mouse.active = False

    #gameloop
    state_stack[-1].game_loop()

    #update mouse
    mouse.update()

    #draw
    state_stack[-1].draw(game_window)
    pygame.display.update()

    clock.tick(60)