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
        self.textmode = False
        self.text = ''
        
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
        path = Path(__file__).parent / Path('saves')
        button_dict = {}
        for i, save in enumerate(glob.glob(str(path) + "\\*\\" )):
            button_dict[os.path.basename(save[:-1])] = interfacec.Button_load_menue(
                100, 
                100 * i + 200, 
                200, 
                74,
                os.path.basename(save[:-1]),
                os.path.basename(save[:-1]),
            )
        
        button_new_save = interfacec.Button(
                10, 
                10, 
                200, 
                75,
                "new save",
                lambda: self.new_save(),
            )
        
        button_ass_text_field = interfacec.Button(
                220, 
                10, 
                200, 
                75,
                self.text,
                lambda: self.load_menue_text(),
            )
        
        self._button_list = [button_new_save, button_ass_text_field]
        for button in button_dict:
            self._button_list.append(button_dict[button])
        
        for button in self._button_list:
            button.draw(self._surface)
    
    def load_menue_text(self):
        self.textmode = True
    
    def new_save(self):
        path = Path(__file__).parent / Path('savea') / Path(self.text)
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        self.textmode = False
    
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