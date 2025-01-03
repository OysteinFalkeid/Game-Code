import pygame
import menues
import interfacec
import game as game_controller
import traceback
import multiprocessing
import multiprocessing.process
from pathlib import Path
import math


import os
import platform
import ctypes


    

class Main:
    def __init__(self):
        # pygame setup
        pygame.init()
        pygame.mixer.init()
        pygame.key.set_repeat(500, 50)
        
        print('\n')
        self._clock = pygame.time.Clock()
        #defines if the game is running or not. when set to 0 or False the game closes
        self._running = True
        self.mousebuttondown = False

        #the size of the screen, width and hight can be used insted off caling get_screen_width() ...
        self._size = pygame.display.get_desktop_sizes()[0]
        self._size = width, height = self._size[0]/1.5, self._size[1]/1.5
        self._scale_factor = min(width, height)/480
        #The colour to set the screen to between every frame.
        self._background_base_colour = 30, 63, 90
        self._screen = pygame.display.set_mode(self._size, flags=(pygame.RESIZABLE), depth=8)
        pygame.display.set_caption('Game Code', 'Game Code')
        pygame.display.set_icon(pygame.image.load((Path(__file__).parent / Path('sprites') / Path('icon.png'))))

        self.maximize_window()
        
        PLAY = pygame.event.custom_type()
        TEXT_MODE = pygame.event.custom_type()
        GAME_MODE = pygame.event.custom_type()
        LOAD_MENUE = pygame.event.custom_type()
        
        self._custom_event_dict = {
            'PLAY': PLAY,
            'TEXT_MODE': TEXT_MODE,
            'GAME_MODE': GAME_MODE,
            'LOAD_MENUE': LOAD_MENUE,
        }
        
        self._game_mode = 'GAME_MODE'
        
        self._event_hash_map = {
            pygame.QUIT:            self.QUIT,
            pygame.ACTIVEEVENT:     self.SPARE,
            pygame.KEYDOWN:         self.KEYDOWN,
            pygame.KEYUP:           self.SPARE,
            pygame.MOUSEMOTION:     self.SPARE,
            pygame.MOUSEBUTTONUP:   self.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN: self.MOUSEBUTTONDOWN,
            pygame.JOYAXISMOTION:   self.SPARE,
            pygame.JOYBALLMOTION:   self.SPARE,
            pygame.JOYHATMOTION:    self.SPARE,
            pygame.JOYBUTTONUP:     self.SPARE,
            pygame.JOYBUTTONDOWN:   self.SPARE,
            pygame.VIDEORESIZE:     self.VIDEORESIZE,
            pygame.VIDEOEXPOSE:     self.SPARE,
            pygame.USEREVENT:       self.SPARE,
            PLAY:                   self.PLAY,
            TEXT_MODE:              self.TEXT_MODE,
            GAME_MODE:              self.GAME_MODE,
            LOAD_MENUE:             self.LOAD_MENUE,
            pygame.AUDIODEVICEADDED: self.SPARE,
            pygame.AUDIODEVICEREMOVED: self.SPARE,
            pygame.FINGERMOTION: self.SPARE,
            pygame.FINGERDOWN: self.SPARE,
            pygame.FINGERUP: self.SPARE,
            pygame.MOUSEWHEEL: self.SPARE,
            pygame.MULTIGESTURE: self.SPARE,
            pygame.TEXTEDITING: self.SPARE,
            pygame.TEXTINPUT: self.SPARE,
            pygame.DROPFILE: self.SPARE,
            pygame.DROPBEGIN: self.SPARE,
            pygame.DROPCOMPLETE: self.SPARE,
            pygame.DROPTEXT: self.SPARE,
            pygame.MIDIIN: self.SPARE,
            pygame.MIDIOUT: self.SPARE,
            pygame.CONTROLLERDEVICEADDED: self.SPARE,
            pygame.JOYDEVICEADDED: self.SPARE,
            pygame.CONTROLLERDEVICEREMOVED: self.SPARE,
            pygame.JOYDEVICEREMOVED: self.SPARE,
            pygame.CONTROLLERDEVICEREMAPPED: self.SPARE,
            pygame.KEYMAPCHANGED: self.SPARE,
            pygame.CLIPBOARDUPDATE: self.SPARE,
            pygame.RENDER_TARGETS_RESET: self.SPARE,
            pygame.RENDER_DEVICE_RESET: self.SPARE,
            pygame.LOCALECHANGED: self.SPARE,
            pygame.WINDOWSHOWN: self.SPARE,
            pygame.WINDOWHIDDEN: self.SPARE,
            pygame.WINDOWEXPOSED: self.SPARE,
            pygame.WINDOWMOVED: self.SPARE,
            pygame.WINDOWRESIZED: self.SPARE,
            pygame.WINDOWSIZECHANGED: self.SPARE,
            pygame.WINDOWMINIMIZED: self.SPARE,
            pygame.WINDOWMAXIMIZED: self.SPARE,
            pygame.WINDOWRESTORED: self.SPARE,
            pygame.WINDOWENTER: self.SPARE,
            pygame.WINDOWLEAVE: self.SPARE,
            pygame.WINDOWFOCUSGAINED: self.SPARE,
            pygame.WINDOWFOCUSLOST: self.SPARE,
            pygame.WINDOWCLOSE: self.SPARE,
            pygame.WINDOWTAKEFOCUS: self.SPARE,
            pygame.WINDOWHITTEST: self.SPARE,
            pygame.WINDOWICCPROFCHANGED: self.SPARE,
            pygame.WINDOWDISPLAYCHANGED: self.SPARE,
            pygame.APP_TERMINATING: self.SPARE,
            pygame.APP_LOWMEMORY: self.SPARE,
            pygame.APP_WILLENTERBACKGROUND: self.SPARE,
            pygame.APP_DIDENTERBACKGROUND: self.SPARE,
            pygame.APP_WILLENTERFOREGROUND: self.SPARE,
            pygame.APP_DIDENTERFOREGROUND: self.SPARE,
        }
        
        self._game = game_controller.Game(self._screen, width, height, self._scale_factor, self._custom_event_dict)
        #the game is activated via the main menue. where it is set to try to render the game
        self._display_game = False
        
        #the debugger is an ingame displayer 
        self._debug = True
        
        self._fps_displayer = interfacec.Text(
            math.floor(self._scale_factor*20),math.floor(self._scale_factor*8),
            0,0,
            'None', 
            math.floor(self._scale_factor*11),
            colour='white'
        )

        self._menue_controller = menues.Menue_controller(self._screen, self._scale_factor, self._custom_event_dict)
  
    def NOT_IN_EVENT_HASH_MAP(selef, event: pygame.event.Event):
        pass
        # print(f'event not in event_hash_map: {event}')
        
    def QUIT(self, event: pygame.event.Event):
        self._running = False 
    
    def MOUSEBUTTONDOWN(self, event: pygame.event.Event):
        mouse = pygame.mouse.get_pos()
        self._menue_controller.on_mouse_press(mouse)
        if self._display_game:
            self._game.on_mouse_press(mouse)
        
        self._game.send_mouse_pos_to_file(pygame.mouse.get_pos())
        
        self.mousebuttondown = True

    def MOUSEBUTTONUP(self, event: pygame.event.Event):
        mouse = pygame.mouse.get_pos()
        if self._display_game:
            self._game.on_mouse_press(mouse, release=True)
            
        self.mousebuttondown = False
    
    def PLAY(self, event: pygame.event.Event):
        self._menue_controller.set_menue('game')
        self._display_game = True
        self._game.resume()
    
    def TEXT_MODE(self, event: pygame.event.Event):
        self._game_mode = 'TEXT_MODE'
    
    def GAME_MODE(self, event: pygame.event.Event):
        self._game_mode = 'GAME_MODE'
    
    def LOAD_MENUE(self, event: pygame.event.Event):
        self._game_mode = 'LOAD_MENUE'
        self._menue_controller.set_menue('load_menue')
    
    def KEYDOWN(self, event: pygame.event.Event):
        if event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen() 
        elif event.key == pygame.K_ESCAPE:
            self._display_game = False
            self._game.pause()
            self._menue_controller.set_menue('main')
        elif self._menue_controller.textmode:
            if event.unicode != '':
                if event.key == pygame.K_BACKSPACE:
                    self._menue_controller.text = self._menue_controller.text[:-1]
                else:
                    self._menue_controller.text += event.unicode
        elif self._game_mode == 'TEXT_MODE':
            self._game.send_key_to_file_wiewer(event)
        else:
            self._game.add_keystroke_to_queue(event.unicode)
    
    def VIDEORESIZE(self, event: pygame.event.Event):
        self._size = width, height = event.w, event.h
        self._scale_factor = min(width, height)/480
        self._fps_displayer.scale(math.floor(self._scale_factor * 8))
        self._menue_controller.scale(self._scale_factor)
        self._game.scale(self._scale_factor)
        
    def SPARE(self, event: pygame.event.Event):
        pass
        # print(f'event function not defined: {event}')
    
    def main_loop(self):
        try:
            while self._running:
                
                for event in pygame.event.get():
                    self._event_hash_map.get(event.type, self.NOT_IN_EVENT_HASH_MAP)(event)
                        
                self._game.move_file_wiewer(pygame.mouse.get_rel())
                if self.mousebuttondown:
                    self._game.on_mouse_press(pygame.mouse.get_pos(), release=True)
                
                self._screen.fill(self._background_base_colour)
                
                self._menue_controller.draw()
                
                if self._display_game:
                    self._game.draw()
                
                if self._game_mode == 'LOAD_MENUE':
                    save = self._menue_controller.get_save()
                    if save:
                        self._game.save = save
                        self._menue_controller.set_menue('main')
                
                if self._debug:
                    self._fps_displayer.set_text(str(round(self._clock.get_fps(), 2)))
                    self._fps_displayer.draw(self._screen)
                pygame.display.flip()
                # currentley the limmiting factor for the annimation speed is the clock function integrated in the Code_prosessor class in game.py
                self._clock.tick(80)  # limits FPS to 80
                
                
                
        except KeyboardInterrupt as e:
            print(f'program intereupted by user with {e}')
        except Exception as e:
            print(f'Game crashed {e}\n\n{traceback.format_exc()}')
        finally:
            pygame.quit()
            pygame.mixer.quit()
            self._game.kill()
            print('Exit')
            
    def maximize_window(self):
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
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    main = Main()
    main.main_loop()
    
