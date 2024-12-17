import pygame
from typing import Optional, Union, Tuple, Sequence
from pathlib import Path
import math

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.color.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

class Text:
    def __init__(self, x, y, width, hight, text, font_size: int, colour: Optional[ColorValue] = 'black'):
        self._x = x
        self._y = y
        self._width = width
        self._hight = hight
        self._max_rect_value = max(self._width, self._hight)
        self._min_rect_value = min(self._width, self._hight)
        self._rectvalue = [self._x, self._y, self._width, self._hight]
        self._colour = colour
        self._text_str = text
        self._font_size = font_size
        self._font =  pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), font_size)
        self._text_surface = self._font.render(self._text_str, True, self._colour)
        
    def draw(self, surface: pygame.Surface):
        surface.blit(self._text_surface, (
            math.floor(self._x + self._width/2 - len(self._text_str) * self._font_size * (11 / 40)), 
            self._y + self._hight/2 - self._font_size/2, 
            self._width, 
            self._hight,
        ))
        
    def set_text(self, text):
        self._text_str = text
        self._text_surface = self._font.render(self._text_str, True, self._colour)
    
    def scale(self, font_size: int):
        self._font =  pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), font_size)
        self._text_surface = self._font.render(self._text_str, True, self._colour)

class Button(Text):
    def __init__(self, x, y, width, hight, text, font_size: int, function, surface = None, colour: Optional[ColorValue] = 'black'):
        super().__init__(x, y, width, hight, text, font_size, colour)
        self._function = function
        self._surface = surface
        
        
        # define the button on its own surface stored in ram
        self._button_surface = pygame.Surface((self._width, self._hight))
        self._path = Path(__file__).parent / Path('sprites') / Path('Button_texture.png')
        
        # exstracts the button textre and transforms every part to fit the definesd button size
        border_thickness = math.floor(self._min_rect_value/4) # every button in the game has the same relative border thickness
        self._center = Sprite(self._path, 
                            (x, y), 
                            width, hight, 
                            (64, 64, 32, 32))
        self._upper = Sprite(self._path, 
                            (x, y), 
                            width, border_thickness, 
                            (32, 32, 32, 32))
        self._lower = Sprite(self._path, 
                            (x, y + hight - border_thickness), 
                            width, border_thickness, 
                            (0, 64, 32, 32))
        self._left = Sprite(self._path, 
                            (x, y), 
                            border_thickness, hight, 
                            (64, 32, 32, 32))
        self._right = Sprite(self._path, 
                            (x + width - border_thickness, y), 
                            border_thickness, hight, 
                            (32, 64, 32, 32))
        self._upper_left = Sprite(self._path, 
                                  (x,y), 
                                  border_thickness, border_thickness, 
                                  (0, 0, 32, 32))
        self._lower_left = Sprite(self._path, 
                                  (x, y +  hight - border_thickness), 
                                  border_thickness, border_thickness, 
                                  (32, 0, 32, 32))
        self._lower_right = Sprite(self._path, 
                                   (x + width - border_thickness, y + hight - border_thickness), 
                                   border_thickness, border_thickness, 
                                   (64, 0, 32, 32))
        self._upper_right = Sprite(self._path, 
                                   (x + width - border_thickness, y), 
                                   border_thickness, border_thickness, 
                                   (0, 32, 32, 32))

        # blit all the parts of the button to the button surface
        self._button_surface.blit(self._center.image, (self._center.rect.left - x, self._center.rect.top - y))
        self._button_surface.blit(self._upper.image, (self._upper.rect.left- x, self._upper.rect.top- y))
        self._button_surface.blit(self._lower.image, (self._lower.rect.left- x, self._lower.rect.top- y))
        self._button_surface.blit(self._left.image, (self._left.rect.left- x, self._left.rect.top- y))
        self._button_surface.blit(self._right.image, (self._right.rect.left- x, self._right.rect.top- y))
        self._button_surface.blit(self._upper_left.image, (self._upper_left.rect.left - x, self._upper_left.rect.top - y))
        self._button_surface.blit(self._lower_left.image, (self._lower_left.rect.left- x, self._lower_left.rect.top- y))
        self._button_surface.blit(self._lower_right.image, (self._lower_right.rect.left- x, self._lower_right.rect.top- y))
        self._button_surface.blit(self._upper_right.image, (self._upper_right.rect.left- x, self._upper_right.rect.top- y))
    
    def test_button_press(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._hight:
            self._function()
            
    def draw(self, surface: pygame.Surface):
        #pygame.draw.rect(surface, (170,170,170), self._rectvalue)
        surface.blit(self._button_surface, (self._x, self._y))
        super().draw(surface)
    
    def scale(self, x, y, width, hight):
        # exstracts the button textre and transforms every part to fit the definesd button size
        border_thickness = math.floor(self._min_rect_value/4) # every button in the game has the same relative border thickness
        self._center = Sprite(self._path, 
                            (x, y), 
                            width, hight, 
                            (64, 64, 32, 32))
        self._upper = Sprite(self._path, 
                            (x, y), 
                            width, border_thickness, 
                            (32, 32, 32, 32))
        self._lower = Sprite(self._path, 
                            (x, y + hight - border_thickness), 
                            width, border_thickness, 
                            (0, 64, 32, 32))
        self._left = Sprite(self._path, 
                            (x, y), 
                            border_thickness, hight, 
                            (64, 32, 32, 32))
        self._right = Sprite(self._path, 
                            (x + width - border_thickness, y), 
                            border_thickness, hight, 
                            (32, 64, 32, 32))
        self._upper_left = Sprite(self._path, 
                                  (x,y), 
                                  border_thickness, border_thickness, 
                                  (0, 0, 32, 32))
        self._lower_left = Sprite(self._path, 
                                  (x, y +  hight - border_thickness), 
                                  border_thickness, border_thickness, 
                                  (32, 0, 32, 32))
        self._lower_right = Sprite(self._path, 
                                   (x + width - border_thickness, y + hight - border_thickness), 
                                   border_thickness, border_thickness, 
                                   (64, 0, 32, 32))
        self._upper_right = Sprite(self._path, 
                                   (x + width - border_thickness, y), 
                                   border_thickness, border_thickness, 
                                   (0, 32, 32, 32))

        # blit all the parts of the button to the button surface
        self._button_surface.blit(self._center.image, (self._center.rect.left - x, self._center.rect.top - y))
        self._button_surface.blit(self._upper.image, (self._upper.rect.left- x, self._upper.rect.top- y))
        self._button_surface.blit(self._lower.image, (self._lower.rect.left- x, self._lower.rect.top- y))
        self._button_surface.blit(self._left.image, (self._left.rect.left- x, self._left.rect.top- y))
        self._button_surface.blit(self._right.image, (self._right.rect.left- x, self._right.rect.top- y))
        self._button_surface.blit(self._upper_left.image, (self._upper_left.rect.left - x, self._upper_left.rect.top - y))
        self._button_surface.blit(self._lower_left.image, (self._lower_left.rect.left- x, self._lower_left.rect.top- y))
        self._button_surface.blit(self._lower_right.image, (self._lower_right.rect.left- x, self._lower_right.rect.top- y))
        self._button_surface.blit(self._upper_right.image, (self._upper_right.rect.left- x, self._upper_right.rect.top- y))
    
    @property
    def sprite(self):
        return self._button_surface

class Button_load_menue(Button):
    def __init__(self, x, y, width, hight, text, font_size: int, function, surface=None):
        width = width + len(text) * font_size * (11/20)
        super().__init__(x, y, width, hight, text, font_size, function, surface)
        
    def test_button_press(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._hight:
            return self._function
            
            
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_file, coordinate, width: Optional[int] = None, hight: Optional[int] = None, sprite_rect = (0, 0, 1, 1)):
        super().__init__()
        self.image = pygame.image.load(image_file)
        # sprite_rect = pygame.Rect(0, 0, 32, 32)
        self.image = self.image.subsurface(sprite_rect)
        if width and hight:
            self.image = pygame.transform.scale(self.image, (width, hight))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate
    
    def scale(self, width, hight):
        self.image = pygame.transform.scale(self.image, (width, hight))