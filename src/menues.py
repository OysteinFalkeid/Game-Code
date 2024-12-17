import interfacec as interfacec
import pygame
import os
from pathlib import Path
import glob
import math


class Menue_controller:
    def __init__(self, surface, scale_factor, custom_event_dict):
        self._surface = surface
        
        self._save = ''
        self.textmode = False
        self.text = ''
        
        self._display_menue = 'main'
        
        self._custom_event_dict = custom_event_dict
        self._button_list: list[interfacec.Button] = []
        self._button_load_list: list[interfacec.Button_load_menue] = []
        
        self.scale(scale_factor)
        
    def draw(self):
        if self._display_menue == 'main':
            self.main_menue()
        elif self._display_menue == 'game':
            self.inngame_menue()
        elif self._display_menue == 'load_menue':
            self.load_menue() 

    def scale(self, scale_factor):
        self._scale_factor = scale_factor
        
        self._button_quit = \
            interfacec.Button(
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 20),
                math.floor(self._scale_factor * 80), 
                math.floor(self._scale_factor * 40), 
                "Quit",
                math.floor(self._scale_factor * 16),
                lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
            )
        
        self._button_play = \
            interfacec.Button(
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 70),
                math.floor(self._scale_factor * 80), 
                math.floor(self._scale_factor * 40), 
                "Play",
                math.floor(self._scale_factor * 16),
                lambda: pygame.event.post(pygame.event.Event(self._custom_event_dict['PLAY'])),
            )
        
        self._button_Load = \
            interfacec.Button(
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 120),
                math.floor(self._scale_factor * 160), 
                math.floor(self._scale_factor * 40),
                "Load/new save",
                math.floor(self._scale_factor * 16),
                lambda: pygame.event.post(pygame.event.Event(self._custom_event_dict['LOAD_MENUE'])),
            )
            
        self._button_new_save = \
            interfacec.Button(
                math.floor(self._scale_factor *20), 
                math.floor(self._scale_factor * 70),
                math.floor(self._scale_factor * 90), 
                math.floor(self._scale_factor * 40), 
                "New save",
                math.floor(self._scale_factor * 16),
                lambda: self.new_save(),
            )
        
        self._button_ass_text_field = \
            interfacec.Button(
                math.floor(self._scale_factor * 120), 
                math.floor(self._scale_factor * 70),
                math.floor(self._scale_factor * 300), 
                math.floor(self._scale_factor * 40), 
                self.text,
                math.floor(self._scale_factor * 16),
                lambda: self.load_menue_text(),
            )
        
        self._button_back = \
            interfacec.Button(
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 20),
                math.floor(self._scale_factor * 90), 
                math.floor(self._scale_factor * 40), 
                "Back",
                math.floor(self._scale_factor * 16),
                lambda: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)),
            )
        
        path = Path(__file__).parent / Path('saves')
        button_dict = {}
        for i, save in enumerate(glob.glob(str(path) + "\\*\\" )):
            button_dict[os.path.basename(save[:-1])] = interfacec.Button_load_menue(
                math.floor(self._scale_factor * 20),
                math.floor(self._scale_factor * 50) * i + math.floor(self._scale_factor * 140), 
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 40),
                os.path.basename(save[:-1]),
                math.floor(self._scale_factor * 16),
                os.path.basename(save[:-1]),
            )
        
        self._button_load_list = []
        for button in button_dict:
            self._button_load_list.append(button_dict[button])
           
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
        self._button_ass_text_field.set_text(self.text)
        self._button_list = [self._button_new_save, self._button_ass_text_field, self._button_back]
        
        for button in self._button_list:
            button.draw(self._surface)
        
        for button in self._button_load_list:
            button.draw(self._surface)
    
    def load_menue_text(self):
        self.textmode = True
    
    def new_save(self):
        path = Path(__file__).parent / Path('saves') / Path(self.text)
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        self.textmode = False
        
        self.scale(self._scale_factor)
    
    def get_save(self):
        save = self._save
        self._save = ''
        return save
    
    def on_mouse_press(self, coordinate):
        if self._display_menue == 'load_menue':
            for button in self._button_load_list:
                self._save = button.test_button_press(coordinate)
                if self._save:
                    break
        
        for button in self._button_list:
                button.test_button_press(coordinate)
            
    def set_menue(self, menue):
        self._display_menue = menue