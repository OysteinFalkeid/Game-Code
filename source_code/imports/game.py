import pygame
import imports.interfacec as interfacec
from pathlib import Path
import traceback
from typing import Optional, Union

class Game:
    def __init__(self, surface, width = 0, height = 0, custom_event_dict: dict[str, pygame.event.Event] = {}):
        self._width = width
        self._height = height
        self._surface = surface
        self._file_dict: dict[Path, File_wiewer] = {}
        
        
        self._button_new_file = \
            interfacec.Button(
                self._width/32, 
                self._height/32, 
                width/4, 
                height/8, 
                "New file",
                lambda: self._append_file(), 
            )
        
        self._button_list: list[interfacec.Button] = [self._button_new_file]
        
        self._custom_event_dict = custom_event_dict
    
    def render(self):
        for button in self._button_list:
            button.display(self._surface)
            
        for file in self._file_dict.values():
            file.display(self._surface)
    
    def _append_file(self):
        file_name = f'code_file_{len(self._file_dict)}'
        path = Path(__file__).parent.parent \
            / Path('save') / Path('save_1') \
            / Path(file_name + '.py')
            
        self._file_dict[file_name] = File_wiewer(file_name, path, self._custom_event_dict)
    
    def eddit_file(self, keystroke: str):
        for file in self._file_dict.values():
            if file.selected:
                file.text_edditer(keystroke)
                break
    
    def send_key_to_file_wiewer(self, event):
        for file in self._file_dict.values():
            if file.selected:
                file.handle_key(event)
    
    def on_mouse_press(self, coordinate):
        for button in self._button_list:
            button.test_button_press(coordinate)
            
        for file in self._file_dict.values():
            file.test_file_select(coordinate)
    
    def pause(self):
        self._button_list = []
        
    def resume(self):
        self._button_list = [self._button_new_file]
        
        
class File_wiewer:
    def __init__(self, name, path, custom_event_dict):
        self._path = path
        self._name = name
        
        self._x = 100
        self._y = 100
        self._width = 1000
        self._height = 800
        self._rectvalue = (0, 0, self._width, self._height)
        self._coordinate = (self._x, self._y)
        
        self._button_play = \
            interfacec.Button(
                0, 0, 80, 40, 
                "play",
                lambda: self.run_code(), 
            )
        self._button_save = \
            interfacec.Button(
                80, 0, 80, 40, 
                "save",
                lambda: self.save(), 
            )
        
        self.selected = False
        if not Path.is_file(self._path):
            with open(self._path, 'x'):
                pass
        with open(self._path, 'r') as file:
            self._text_list = list(file.read())
            
        self._text_surface = pygame.Surface((self._width, self._height))
        self._text_lines: list[str] = []
        self._custom_event_dict = custom_event_dict
        self._font= pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), 20)
        
        self._cursor = self._font.render('|', True, 'white')
        self._cursor_index = 0
        self._cursor_line = 0
        self._text_list_index = 0
        
        
        
    def display(self, surface: pygame.Surface):
        self._text_lines = []
        text_line = ''
        for text in self._text_list:
            if text == '\n':
                self._text_lines.append(text_line)
                text_line = ''
            else:
                text_line += text
        self._text_lines.append(text_line)
        text_line = ''
        pygame.draw.rect(self._text_surface, (170,170,170), self._rectvalue)
        text_list: list[pygame.font.Font.render] = [self._font.render(text, True, 'white') for text in self._text_lines]
        
        for i, text in enumerate(text_list):
            self._text_surface.blit(text, (40, i*18 + 40))
            
        self._button_play.display(self._text_surface)
        self._button_save.display(self._text_surface)
        self._display_cursor()
        surface.blit(self._text_surface, self._coordinate)
                
    def test_file_select(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._height:
            self.selected = True
            pygame.event.post(pygame.event.Event(self._custom_event_dict['TEXT_MODE']))
            print('selected')
        else:
            if self.selected:
                self.selected = False
                pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
        
        self._button_play.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
        self._button_save.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
        
    def run_code(self):
        self.save()
        
        try:
            with open(self._path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip('\n')
                    exec(line)
        except Exception as e:
            print(f'{e}\n\n{traceback.format_exc()}')
    
    def save(self):
        with open(self._path, 'w') as file:
            file.write(''.join(self._text_list))
    
    def text_edditer(self, keystroke: str):
        if keystroke == '':
            pass
        elif keystroke == '\x08':
            if self._text_list_index:
                self._text_list.pop(self._text_list_index -1)
                self._text_list_index -= 1
                self._cursor_index -= 1 
        elif keystroke == '\r':
            self._text_list.insert(self._text_list_index, '\n')
            self._text_list_index += 1
            self._cursor_index += 1 
        else:
            self._text_list.insert(self._text_list_index, keystroke)
            self._text_list_index += 1
            self._cursor_index += 1 
            print(self._text_list)
    
    def handle_key(self, event):
        if event.key == pygame.K_UP:
            if self._cursor_line:
                self._cursor_line -= 1
                if self._cursor_index < len(self._text_lines[self._cursor_line]):
                    self._text_list_index -= len(self._text_lines[self._cursor_line]) + 1
                else:
                    self._text_list_index -= self._cursor_index + 1
                if len(self._text_lines[self._cursor_line]) <= self._cursor_index:
                    self._cursor_index = len(self._text_lines[self._cursor_line])
                
        elif event.key == pygame.K_RIGHT:
            if len(self._text_lines[self._cursor_line]) <= self._cursor_index:
                self._cursor_index = len(self._text_lines[self._cursor_line])
            else:
                self._cursor_index += 1 
                self._text_list_index += 1
                
        elif event.key == pygame.K_DOWN:
            self._text_list_index += len(self._text_lines[self._cursor_line]) + 1
            self._cursor_line += 1
            if len(self._text_lines[self._cursor_line]) <= self._cursor_index:
                self._text_list_index -= self._cursor_index - len(self._text_lines[self._cursor_line])
                self._cursor_index = len(self._text_lines[self._cursor_line])
            
        elif event.key == pygame.K_LEFT:
            if self._cursor_index > 0:
                self._cursor_index -= 1
                if self._text_list_index > 0:
                    self._text_list_index -= 1
        print(self._text_list_index)
            
    def _display_cursor(self):
        
        self._text_surface.blit(self._cursor, (self._cursor_index * 11 + 35, self._cursor_line*18 + 40))
            
            
            
            
            
            
            
            
            
            
            
            
            