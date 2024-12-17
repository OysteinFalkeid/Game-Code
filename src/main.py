import multiprocessing.process
import pygame
import sys
import menues as menues
import interfacec as interfacec
import traceback
import game as game_controller
import multiprocessing
import time
from pathlib import Path
import math


import os
import platform
import ctypes

def maximize_window():
    """
    Maximize the Pygame window based on the operating system.
    """
    hwnd = pygame.display.get_wm_info()["window"]
    system = platform.system()

    if system == 'Windows':
        ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
    elif system == 'Linux':
        os.system(f"wmctrl -i -r {hwnd} -b add,maximized_vert,maximized_horz")
    elif system == 'Darwin':  # macOS
        os.system(f"""
        osascript -e 'tell application "System Events" to set the position of windows of application "Python" to {{0, 0}}'
        osascript -e 'tell application "System Events" to set the size of windows of application "Python" to {{1920, 1080}}'
        """)
    else:
        # Fallback: Simulate maximized window
        info = pygame.display.Info()
        pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
    
# Define a custom sprite class


def main():
    # pygame setup
    pygame.init()
    pygame.mixer.init()
    
    print('\n')
    clock = pygame.time.Clock()
    #defines if the game is running or not. when set to 0 or False the game closes
    running = True
    
    #the size of the screen, width and hight can be used insted off caling get_screen_width() ...
    size = pygame.display.get_desktop_sizes()[0]
    size = width, height = size[0]/1.5, size[1]/1.5
    scale_factor = min(width, height)/480
    #The colour to set the screen to between every frame.
    background_base_colour = 30, 63, 90
    screen = pygame.display.set_mode(size, flags=(pygame.RESIZABLE), depth=8)
    pygame.display.set_caption('Game Code', 'Game Code')
    pygame.display.set_icon(pygame.image.load((Path(__file__).parent / Path('sprites') / Path('icon.png'))))
    
    maximize_window()
    
    PLAY = pygame.event.custom_type()
    TEXT_MODE = pygame.event.custom_type()
    GAME_MODE = pygame.event.custom_type()
    LOAD_MENUE = pygame.event.custom_type()
    
    custom_event_dict = {
        'PLAY': PLAY,
        'TEXT_MODE': TEXT_MODE,
        'GAME_MODE': GAME_MODE,
        'LOAD_MENUE': LOAD_MENUE,
    }
    game_mode = 'GAME_MODE'
    
    game = game_controller.Game(screen, width, height, scale_factor, custom_event_dict)
    #the game is activated via the main menue. where it is set to try to render the game
    display_game = False
    
    #the debugger is an ingame displayer 
    debug = True
    
    fps_displayer = interfacec.Text(
        math.floor(scale_factor*20),math.floor(scale_factor*8),
        0,0,
        'None', 
        math.floor(scale_factor*8),
        colour='white'
    )

    menue_controller = menues.Menue_controller(screen, scale_factor, custom_event_dict)
    
    try:
        while running:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    menue_controller.on_mouse_press(mouse)
                    if display_game:
                        game.on_mouse_press(mouse)
                    
                elif event.type == custom_event_dict['PLAY']:
                    menue_controller.set_menue('game')
                    display_game = True
                    game.resume()
                    
                elif event.type == custom_event_dict['TEXT_MODE']:
                    game_mode = 'TEXT_MODE'
                
                elif event.type == custom_event_dict['GAME_MODE']:
                    game_mode = 'GAME_MODE'
                
                elif event.type == custom_event_dict['LOAD_MENUE']:
                    game_mode = 'LOAD_MENUE'
                    menue_controller.set_menue('load_menue')
                           
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen() 
                    elif event.key == pygame.K_ESCAPE:
                        display_game = False
                        game.pause()
                        menue_controller.set_menue('main')
                    elif menue_controller.textmode:
                        if event.unicode != '':
                            if event.key == pygame.K_BACKSPACE:
                                menue_controller.text = menue_controller.text[:-1]
                            else:
                                menue_controller.text += event.unicode
                    elif game_mode == 'TEXT_MODE':
                        if event.unicode == '':
                             game.send_key_to_file_wiewer(event)
                        else:
                            print(repr(event.unicode))
                            game.eddit_file(event.unicode)
                    else:
                        game.add_keystroke_to_queue(event.unicode)
                
                elif event.type == pygame.VIDEORESIZE:
                     
                    size = width, height = size = event.w, event.h
                    scale_factor = min(width, height)/480
                    fps_displayer.scale(math.floor(scale_factor * 8))
                    menue_controller.scale(scale_factor)
                    game.scale(scale_factor)
                    # menue_controller.set_size(size, width, height)
                    # game.set_size(size, width, height)
            
            game.move_file_wiewer(pygame.mouse.get_rel())
            game.send_mouse_pos_to_file(pygame.mouse.get_pos())
            
            screen.fill(background_base_colour)
            
            menue_controller.draw()
            
            if display_game:
                #player.draw(screen)
                game.draw()
            
            if game_mode == 'LOAD_MENUE':
                save = menue_controller.get_save()
                if save:
                    game.save = save
                    menue_controller.set_menue('main')
            
            if debug:
                fps_displayer.set_text(str(round(clock.get_fps(), 2)))
                fps_displayer.draw(screen)
            pygame.display.flip()
            # currentley the limmiting factor for the annimation speed is the clock function integrated in the Code_prosessor class in game.py
            clock.tick(80)  # limits FPS to 1000
            
            
            
    except KeyboardInterrupt as e:
        print(f'program intereupted by user with {e}')
    except Exception as e:
        print(f'Game crashed {e}\n\n{traceback.format_exc()}')
    finally:
        pygame.quit()
        pygame.mixer.quit()
        game.kill()
        print('Exit')

    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
    
