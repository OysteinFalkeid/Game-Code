import imports.interfacec as interfacec
import pygame


class Menue_controller:
    def __init__(self, surface, size, width, height, custom_event_dict):
        self._surface = surface
        self._size = size
        self._width = width
        self._height = height
        
        self._display_menue = 'main'
        
        self._custom_event_dict = custom_event_dict
        self._button_list: list[interfacec.Button] = []
        
        self._button_quit = \
            interfacec.Button(
                self._width/4, 
                self._height/2, 
                width/4, 
                height/8, 
                "Quit",
                lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
            )
        
        self._button_play = \
            interfacec.Button(
                self._width/4, 
                self._height/4, 
                width/4, 
                height/8,
                "Play",
                lambda: pygame.event.post(pygame.event.Event(self._custom_event_dict['PLAY'])),
            )
        
    
    def draw(self):
        if self._display_menue == 'main':
            self.main_menue()
        if self._display_menue == 'game':
            self.inngame_menue()

    def main_menue(self):
        self._button_list = [
        self._button_quit,
        self._button_play,
        ]
        
        for button in self._button_list:
            button.draw(self._surface)
        
    def inngame_menue(self):
        self._button_list = []
    
    def on_mouse_press(self, coordinate):
        for button in self._button_list:
            button.test_button_press(coordinate)
            
    def set_menue(self, menue):
        self._display_menue = menue