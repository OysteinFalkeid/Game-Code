import pygame
import sys
import imports.menues as menues
import imports.interfacec as interfacec
import traceback
import imports.game as game_controller
    

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
    
    
    custom_event_dict = {
        'PLAY': PLAY,
        'TEXT_MODE': TEXT_MODE,
        'GAME_MODE': GAME_MODE,
    }
    game_mode = 'GAME_MODE'
    
    game = game_controller.Game(screen, width, height, custom_event_dict)
    #the game is activated via the main menue. where it is set to try to render the game
    display_game = False
    
    
    #the debugger is an ingame displayer 
    debug = True
    
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
                    print('text_mode')
                
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
                    
                    
            screen.fill(background_base_colour)
            
            
            menue_controller.display()
            if display_game:
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

if __name__ == '__main__':
    main()