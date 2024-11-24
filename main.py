import pygame
import sys
import menues
import traceback


def main():
    # pygame setup
    pygame.init()
    print('\n\n')
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    #defines if the game is running or not. when set to 0 or FAlse the game closes
    running = True
    
    #the size of the screen, width and hight can be used insted off caling get_screen_width() ...
    size = width, height = 500, 300
    #The colour to set the screen to between every frame.
    background_base_colour = 0, 0, 0
    screen = pygame.display.set_mode(size)
    
    menue_controller = menues.Menue_controller(screen, size, width, height)
    

    try:
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    menue_controller.on_mouse_press(mouse)
                    
            screen.fill(background_base_colour)
            
            
            menue_controller.display()
            
            pygame.display.flip()
            clock.tick(60)  # limits FPS to 60
            
    except KeyboardInterrupt as e:
        print(f'program intereupted by user with {e}')
    except Exception as e:
        print(f'Game crashed {e}\n\n{traceback.format_exc()}')
    finally:
        print('Exit')
        pygame.quit()

if __name__ == '__main__':
    main()