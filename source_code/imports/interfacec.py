import pygame
from typing import Optional, Union, Tuple, Sequence

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.color.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

class Text:
    def __init__(self, x, y, width, height, text, colour: Optional[ColorValue] = 'black'):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rectvalue = [self._x, self._y, self._width, self._height]
        self._colour = colour
        self._font =  pygame.font.Font(None, 32)
        self._text = self._font.render(text, True, self._colour)
        
    def display(self, surface: pygame.Surface):
        surface.blit(self._text, self._rectvalue)
        
    def set_text(self, text):
        self._text = self._font.render(text, True, self._colour)

class Button(Text):
    def __init__(self, x, y, width, height, text, function):
        super().__init__(x, y, width, height, text)
        self._function = function
    
    
    def test_button_press(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._height:
            self._function()
            
    
    def display(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (170,170,170), self._rectvalue)
        super().display(surface)