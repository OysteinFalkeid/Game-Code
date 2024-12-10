import interfacec as interfacec
import pygame
import os
from pathlib import Path
import glob


class Menue_controller:
    def __init__(self, surface, size, width, height, custom_event_dict):
        self._surface = surface
        self._size = size
        self._width = width
        self._height = height
        
        self._save = ''
        
        self._display_menue = 'main'
        
        self._custom_event_dict = custom_event_dict
        self._button_list: list[interfacec.Button] = []
        
        self._button_quit = \
            interfacec.Button(
                100, 
                100, 
                width/4, 
                height/8, 
                "Quit",
                lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
            )
        
        self._button_play = \
            interfacec.Button(
                100, 
                200, 
                width/4, 
                height/8,
                "Play",
                lambda: pygame.event.post(pygame.event.Event(self._custom_event_dict['PLAY'])),
            )
        
        self._button_Load = \
            interfacec.Button(
                100, 
                300, 
                width/4, 
                height/8,
                "Load",
                lambda: pygame.event.post(pygame.event.Event(self._custom_event_dict['LOAD_MENUE'])),
            )
        
    
    def draw(self):
        if self._display_menue == 'main':
            self.main_menue()
        elif self._display_menue == 'game':
            self.inngame_menue()
        elif self._display_menue == 'load_menue':
            self.load_menue() 

    def main_menue(self):
        self._button_list = [
        self._button_quit,
        self._button_play,
        self._button_Load,
        ]
        
        for button in self._button_list:
            button.draw(self._surface)
        
    def inngame_menue(self):
        self._button_list = []
    
    def load_menue(self):
        path = Path(__file__).parent / Path('save')
        button_dict = {}
        for i, save in enumerate(glob.glob(str(path) + "\\*\\" )):
            button_dict[os.path.basename(save[:-1])] = interfacec.Button_load_menue(
                100, 
                100 * i, 
                self._width/4, 
                self._height/8,
                os.path.basename(save[:-1]),
                os.path.basename(save[:-1]),
            )
        
        self._button_list = []
        for button in button_dict:
            self._button_list.append(button_dict[button])
        
        for button in self._button_list:
            button.draw(self._surface)
    
    def get_save(self):
        save = self._save
        self._save = ''
        return save
    
    def on_mouse_press(self, coordinate):
        if self._display_menue == 'load_menue':
            for button in self._button_list:
                self._save = button.test_button_press(coordinate)
                if self._save:
                    break
        else:
            for button in self._button_list:
                button.test_button_press(coordinate)
            
    def set_menue(self, menue):
        self._display_menue = menue