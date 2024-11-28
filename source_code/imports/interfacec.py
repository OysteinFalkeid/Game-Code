import pygame
from typing import Optional, Union, Tuple, Sequence
from pathlib import Path

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.color.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

class Text:
    def __init__(self, x, y, width, height, text, colour: Optional[ColorValue] = 'black'):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_rect_value = max(self._width, self._height)
        self._rectvalue = [self._x, self._y, self._width, self._height]
        self._colour = colour
        self._text_str = text
        self._font =  pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), int(height/2))
        self._text_surface = self._font.render(text, True, self._colour)
        
    def display(self, surface: pygame.Surface):
        surface.blit(self._text_surface, (
            self._x + self._width/2 - len(self._text_str) / 2 * int(self._height/4), 
            self._y + self._height/2 - int(self._height/4), 
            self._width, 
            self._height
        ))
        
    def set_text(self, text):
        self._text_surface = self._font.render(text, True, self._colour)

class Button(Text):
    def __init__(self, x, y, width, height, text, function, surface = None, sprites_group: Optional[pygame.sprite.Sprite] = None):
        super().__init__(x, y, width, height, text)
        self._function = function
        self._surface = surface
        
        self._button_surface = pygame.Surface((self._width, self._height))
        self._sprites_group = sprites_group
        path = Path(__file__).parent / Path('sprites') / Path('New Piskel (1).png')
        self._upper_left = Sprite(path, 
                                  (x,y), 
                                  self._max_rect_value/16, self._max_rect_value/16, 
                                  (0, 0, 32, 32))
        self._lower_left = Sprite(path, 
                                  (x, y +  height - self._max_rect_value/16), 
                                  self._max_rect_value/16, self._max_rect_value/16 + 1, 
                                  (32, 0, 32, 32))
        self._lower_right = Sprite(path, 
                                   (x + width - self._max_rect_value/16 + 1, y + height - self._max_rect_value/16), 
                                   self._max_rect_value/16, self._max_rect_value/16 + 1, 
                                   (64, 0, 32, 32))
        self._upper_right = Sprite(path, 
                                   (x + width - self._max_rect_value/16 + 1, y), 
                                   self._max_rect_value/16, self._max_rect_value/16, 
                                   (0, 32, 32, 32))
        self._upper = Sprite(path, 
                            (x + self._max_rect_value/16, y), 
                            width - self._max_rect_value/16 * 2 +1, self._max_rect_value/16, 
                            (32, 32, 32, 32))
        self._lower = Sprite(path, 
                            (x + self._max_rect_value/16, y + height - self._max_rect_value/16), 
                            width - self._max_rect_value/16 * 2 +1, self._max_rect_value/16 + 1, 
                            (0, 64, 32, 32))
        self._left = Sprite(path, 
                            (x, y + self._max_rect_value/16), 
                            self._max_rect_value/16, height - self._max_rect_value/16 * 2 + 2, 
                            (64, 32, 32, 32))
        self._right = Sprite(path, 
                            (x + width - self._max_rect_value/16 + 1, y + self._max_rect_value/16), 
                            self._max_rect_value/16, height - self._max_rect_value/16 * 2 + 2, 
                            (32, 64, 32, 32))
        self._center = Sprite(path, 
                            (x + self._max_rect_value/16, y + self._max_rect_value/16), 
                            width - self._max_rect_value/16*2 + 2, height - self._max_rect_value/16 * 2 + 2, 
                            (64, 64, 32, 32))
        
        
        self._button_surface.blit(self._upper_left.image, (self._upper_left.rect.left - x, self._upper_left.rect.top - y))
        self._button_surface.blit(self._lower_left.image, (self._lower_left.rect.left- x, self._lower_left.rect.top- y))
        self._button_surface.blit(self._lower_right.image, (self._lower_right.rect.left- x, self._lower_right.rect.top- y))
        self._button_surface.blit(self._upper_right.image, (self._upper_right.rect.left- x, self._upper_right.rect.top- y))
        self._button_surface.blit(self._upper.image, (self._upper.rect.left- x, self._upper.rect.top- y))
        self._button_surface.blit(self._lower.image, (self._lower.rect.left- x, self._lower.rect.top- y))
        self._button_surface.blit(self._left.image, (self._left.rect.left- x, self._left.rect.top- y))
        self._button_surface.blit(self._right.image, (self._right.rect.left- x, self._right.rect.top- y))
        self._button_surface.blit(self._center.image, (self._center.rect.left- x, self._center.rect.top- y))
    
    
    def test_button_press(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._height:
            self._function()
            
    
    def display(self, surface: pygame.Surface):
        #pygame.draw.rect(surface, (170,170,170), self._rectvalue)
        surface.blit(self._button_surface, (self._x, self._y))
        super().display(surface)
    
    @property
    def sprite(self):
        return self._button_surface
        
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_file, coordinate, width: Optional[int] = None, height: Optional[int] = None, sprite_rect = (0, 0, 1, 1)):
        super().__init__()
        self.image = pygame.image.load(image_file)
        # sprite_rect = pygame.Rect(0, 0, 32, 32)
        self.image = self.image.subsurface(sprite_rect)
        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate
    
    def scale(self, width, hight):
        self.image = pygame.transform.scale(self.image, (width, hight))