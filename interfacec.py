import pygame

class Button:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rectvalue = [self._x, self._y, self._width, self._height]
        self._font =  pygame.font.Font('freesansbold.ttf', 32)
        self._text = self._font.render('Quit', True, 'black')
    
    
    def test_button_press(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._height:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def display(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (170,170,170), self._rectvalue)
        surface.blit(self._text, self._rectvalue)