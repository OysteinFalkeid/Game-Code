import multiprocessing.process
import pygame
import sys
import imports.menues as menues
import imports.interfacec as interfacec
import traceback
import imports.game as game_controller
import multiprocessing
import time
    
# Define a custom sprite class


def main():
    # pygame setup
    pygame.init()
    print('\n\n')
    clock = pygame.time.Clock()
    #defines if the game is running or not. when set to 0 or False the game closes
    running = True
    
    display_info = pygame.display.Info()
    
    #the size of the screen, width and hight can be used insted off caling get_screen_width() ...
    size = width, height = display_info.current_w/2, display_info.current_h/2
    #The colour to set the screen to between every frame.
    background_base_colour = 30, 63, 90
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    PLAY = pygame.event.custom_type()
    TEXT_MODE = pygame.event.custom_type()
    GAME_MODE = pygame.event.custom_type()
    MOVE = multiprocessing.Event()
    
    
    custom_event_dict = {
        'PLAY': PLAY,
        'TEXT_MODE': TEXT_MODE,
        'GAME_MODE': GAME_MODE,
        'MOVE': MOVE,
    }
    game_mode = 'GAME_MODE'
    
    sprites_group = pygame.sprite.Group()
    
    game = game_controller.Game(screen, width, height, custom_event_dict)
    #the game is activated via the main menue. where it is set to try to render the game
    display_game = False
    
    player = Player(0,0,100,100)
    
   
    
    
    #the debugger is an ingame displayer 
    debug = False
    
    fps_displayer = interfacec.Text(0,0,width/16, height/16, 'None', colour='white')

    menue_controller = menues.Menue_controller(screen, size, width, height, custom_event_dict)
    

    try:
        while running:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    menue_controller.on_mouse_press(mouse)
                    game.on_mouse_press(mouse)
                    
                elif event.type == custom_event_dict['PLAY']:
                    menue_controller.set_menue('game')
                    display_game = True
                    game.resume()
                    
                elif event.type == custom_event_dict['TEXT_MODE']:
                    game_mode = 'TEXT_MODE'
                
                elif event.type == custom_event_dict['GAME_MODE']:
                    game_mode = 'GAME_MODE'
                
                
                                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        display_game = False
                        game.pause()
                        menue_controller.set_menue('main')
                    elif game_mode == 'TEXT_MODE':
                        if event.unicode == '':
                             game.send_key_to_file_wiewer(event)
                        else:
                            game.eddit_file(event.unicode)

                        
                elif event.type != pygame.MOUSEMOTION and debug == True:
                    print(pygame.event.event_name(event.type))
            
            if custom_event_dict['MOVE'].is_set():
                print('test')
                player.move('down')
                custom_event_dict['MOVE'].clear()
                    
            sprites_group.update()      
            screen.fill(background_base_colour)
            sprites_group.draw(screen)
            
            
            menue_controller.display()
            if display_game:
                player.display(screen)
                game.render()
            
            if debug:
                fps_displayer.set_text(str(round(clock.get_fps(), 2)))
                fps_displayer.display(screen)
            pygame.display.flip()
            clock.tick(60)  # limits FPS to 60
            
            
            
    except KeyboardInterrupt as e:
        print(f'program intereupted by user with {e}')
    except Exception as e:
        print(f'Game crashed {e}\n\n{traceback.format_exc()}')
    finally:
        print('Exit')
        pygame.quit()

class Player:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    def move(self, direction: str):
        if direction == 'right':
            self._x += 10
        elif direction == 'left':
            self._x -= 10
        elif direction == 'up':
            self._y -= 10
        elif direction == 'down':
            self._y += 10
    
    def display(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), (self._x, self._y, self._width, self._height))   
      



    
if __name__ == '__main__':
    main()
    
