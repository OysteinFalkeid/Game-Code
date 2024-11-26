import pytest
import pygame
from imports.game import *
import imports.interfacec as interfacec

def test_width():
    pygame.init()
    game = Game(None,2)
    assert game._width == 2, f'game instance has a _width of {game._width} but shold be 2'
    pygame.quit()
    
    
    
    
