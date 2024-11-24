import interfacec


class Menue_controller:
    def __init__(self, surface, size, width, height):
        self._surface = surface
        self._size = size
        self._width = width
        self._height = height
        self._button_quit = interfacec.Button(self._width/2, self._height/2, width/4, height/4)
        pass
    
    def display(self):
        self.main_menue()

    def main_menue(self):
        self._button_quit.display(self._surface)
        
    def on_mouse_press(self, coordinate):
        self._button_quit.test_button_press(coordinate)