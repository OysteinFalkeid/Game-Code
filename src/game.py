#import multiprocessing.process
import multiprocessing
import multiprocessing.context
import multiprocessing.queues
import pygame
import interfacec as interfacec
from pathlib import Path
import traceback
from typing import Optional, Union
import time
import multiprocessing
import functools
import random
import math
import re


class Game:
    def __init__(self, surface: pygame.Surface, width , height , scale_factor, custom_event_dict: dict[str, pygame.event.Event] = {}):
        self._width = width
        self._height = height
        self._surface = surface
        self._font =  pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), int(height/2))
        self._colour = 'white'
        self._print_list = []
        self._file_dict: dict[str, File_wiewer] = {}
        
        self.scale(scale_factor)
        
        self._custom_event_dict = custom_event_dict
        
        self._multiprocessing_draw_queue = multiprocessing.Queue(128)
        self._multiprocessing_draw_dict = {}
        self._custom_event_queue= multiprocessing.Queue(128)
        
        self.save: str = "save_1"
        
    def draw(self):
        while not self._multiprocessing_draw_queue.empty():
            self._multiprocessing_draw_queue_handler(self._multiprocessing_draw_queue.get())
            
        for values in self._multiprocessing_draw_dict.values():
            image = self.load_image(values[0])
            image = pygame.transform.scale(image, (values[3], values[4]))
            surface = pygame.transform.rotate(image, values[5])
            new_rect = surface.get_rect(center = image.get_rect(center = (values[1], values[2])).center)
            self._surface.blit(surface, new_rect)
        
        while not self._custom_event_queue.empty():
            file, comand, values = self._custom_event_queue.get()
            if comand == 'end':
                self._file_dict[file].join(self._multiprocessing_draw_dict[file])
            elif comand == 'print':
                self._font =  pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), 24)
                string: str = values[0]
                string_list = string.replace('\t', '    ').split('\n')
                text_surface_list = [self._font.render(string, True, 'black') for string in string_list]
                start_time = time.time()
                self._print_list.append((text_surface_list, (values[1], values[2]), values[3], start_time))
            elif comand == 'sound':
                sound = self.load_sound(values[0]) # path
                pygame.mixer.music.set_volume(values[1]) # volume
                sound.play()
            elif comand == 'on_hit':
                if values in self._file_dict:
                    if self._multiprocessing_draw_dict[values][1] + self._multiprocessing_draw_dict[file][3] > self._multiprocessing_draw_dict[file][1] > self._multiprocessing_draw_dict[values][1] - self._multiprocessing_draw_dict[file][3]:
                        if self._multiprocessing_draw_dict[values][2] + self._multiprocessing_draw_dict[file][4] > self._multiprocessing_draw_dict[file][2] > self._multiprocessing_draw_dict[values][2] - self._multiprocessing_draw_dict[file][4]:
                            self._file_dict[file].send_event_value(('on_hit', None))
                else:
                    print(f'file {values} not found')
                    
        
        for i, prints in enumerate(self._print_list):
            if prints[2] < time.time() - prints[3]:
                self._print_list.pop(i)
            else:
                height = len(prints[0])
                width = max([text_surface.get_width() for text_surface in prints[0]])
                pygame.draw.rect(self._surface, 'white', (prints[1][0], prints[1][1], width + 8, height * 24))
                for i, string in enumerate(prints[0]):
                    self._surface.blit(string, (prints[1][0]+ 4, prints[1][1] + i*24))
             
        for button in self._button_list:
            button.draw(self._surface)
            
        for file in self._file_dict.values():
            file.draw(self._surface)
    
    def scale(self, scale_factor):
        self._scale_factor = scale_factor
        
        self._button_new_file = \
            interfacec.Button(
                math.floor(self._scale_factor * 20), 
                math.floor(self._scale_factor * 20),
                math.floor(self._scale_factor * 100), 
                math.floor(self._scale_factor * 40),  
                "New file",
                math.floor(self._scale_factor * 16),
                lambda: self._append_file(), 
            )
        
        self._button_list: list[interfacec.Button] = [self._button_new_file]
        
        for file in self._file_dict:
            self._file_dict[file].scale(self._scale_factor)  
            
    def _multiprocessing_draw_queue_handler(self, values: tuple):
        self._multiprocessing_draw_dict[values[0]] = (values[1], values[2], values[3], values[4], values[5], values[6])
      
    def _append_file(self):
        file_name = f'code_file_{len(self._file_dict)}'
        path = Path(__file__).parent \
            / Path('saves') / Path(self.save) \
            / Path(file_name + '.py')
            
        self._file_dict[file_name] = File_wiewer(
            file_name, 
            path, 
            self._scale_factor,
            self._custom_event_dict, 
            self._multiprocessing_draw_queue, 
            self._custom_event_queue
        )
            
    def add_keystroke_to_queue(self, keystroke):
        for file in self._file_dict.values():
            file.add_keystroke_to_queue(keystroke)
    
    def send_key_to_file_wiewer(self, event):
        for file in self._file_dict.values():
            if file.selected:
                file.text_edditer(event)
    
    def send_mouse_pos_to_file(self, coordinates):
        # print(coordinates)
        for file in self._file_dict.values():
            file.send_event_value(('mouse_coords', coordinates))
    
    def on_mouse_press(self, coordinate):
        for button in self._button_list:
            button.test_button_press(coordinate)
            
        for key in reversed(self._file_dict):
            # print(key)
            if self._file_dict[key].test_file_select(coordinate):
                self._file_dict[key] = self._file_dict.pop(key)
                break
        
    def move_file_wiewer(self, rel_coordinate):
        for file in self._file_dict.values():
            if file.movable:
                file.move_text_edditer(rel_coordinate)
    
    @functools.lru_cache(maxsize=128)
    def load_image(self, path):
        return pygame.image.load(path)
    
    @functools.lru_cache(maxsize=128)
    def load_sound(self, path):
        return pygame.mixer.Sound(path)
    
    def pause(self):
        self._button_list = []
        
    def resume(self):
        self._button_list = [self._button_new_file]
     
    def kill(self):
        for file in self._file_dict.values():
            file.kill()   
        
class File_wiewer:
    def __init__(self, name, path, scale_factor, custom_event_dict, multiprocessing_draw_queue, custom_event_queue):
        self._path = path
        self._name = name
        self._scale_factor = scale_factor
        
        self._x = math.floor(self._scale_factor * 100)
        self._y = math.floor(self._scale_factor * 100)
        self._width = math.floor(self._scale_factor * 100)
        self._height = math.floor(self._scale_factor * 100)
        self._rectvalue = [0, 0, self._width, self._height]
        self._coordinate = (self._x, self._y)
        
        self._custom_event_dict = custom_event_dict
        self._multiprocessing_draw_queue = multiprocessing_draw_queue
        self._custom_event_queue = custom_event_queue
        self._keypress_queue = multiprocessing.Queue(4)
        self._event_queue = multiprocessing.Queue(60)
        self._code_prosessor = \
            Code_prosessor(
                self._name, 
                self._path, 
                self._custom_event_queue, 
                self._multiprocessing_draw_queue,
                self._keypress_queue,
                self._event_queue,
            )
        
        
        self.selected = False
        self.movable = False
        if not Path.is_file(self._path):
            with open(self._path, 'x'):
                pass
        with open(self._path, 'r') as file:
            self._text_list = list(file.read())
        self._text_list_old = None
            
        self._text_lines: list[str] = []
        
        # RegEx for finding and colouring words in the draw function
        keywords = [
            # class spesific
            'move_to', 'move', 'wait', 'print', 'turn', 'random', 'keypress', 'on_hit',
            # for loops
            'for _','for',  'in', 'range', 
            # other
            'while', 
            # if teststs
            'elif', 'if', 'else', 
            # defines
            'True', 'False', 'None'
        ]
        self._function_regex = re.compile(r'\b(?:' + '|'.join(keywords) + r')\b')
        
        self._number_regex = re.compile(r'\b\d+\b')
        
        keywords = [
            '(', ')', '{', '}', '[', ']', 
            ',', ':', ';', '.',
            '+', '-', '*', '/', '%', '+=', '-=', '*=', '/=', '%=',
            '=', '<', '>', '!', '==', '<=', '>=', '!=', '&'
        ]
        
        self._operator_regex = re.compile(r'(?:' +'|'.join(map(re.escape, keywords)) + r')')
        
        self._coment_regex = re.compile(r'#.*')
        
        self.scale(self._scale_factor)
        self._cursor_index = 0
        self._cursor_line = 0
        self._text_list_index = 0
        self._draw_cursor_counter = 0
        
    def draw(self, surface: pygame.Surface):
        
        if self._text_list != self._text_list_old:
            
            self._font= pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), math.floor(self._scale_factor * 20))
            self._cursor = self._font.render('|', True, 'white')
        
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
            
            #setting a adaptive bounding bow for the text edditor.
            # every character is 11 pixels wide at a font size of 20
            # there is a 40 pixel gap for numbering and border
            # and there is a 10 pixel gap for border and breething room
            self._width = max(max([len(line) for line in self._text_lines]), 20)* 11 + 40 + 10
            # the same applies for hight altho a 20 pixel spasing is suficient.
            self._rectvalue[2] = self._width
            self._height = len(self._text_lines) * 20 + 40 + 10
            self._rectvalue[3] = self._height
            # self._text_surface = pygame.transform.scale(self._text_surface, (self._width+4, self._height+4))
            
            self._text_surface = pygame.Surface((math.floor(self._scale_factor * (self._width + 4)), math.floor(self._scale_factor * (self._height + 4))))
            
        pygame.draw.rect(
            self._text_surface, 
            (0,0,0), 
            (
                math.floor(self._scale_factor * self._x), 
                math.floor(self._scale_factor * self._y), 
                math.floor(self._scale_factor * (self._width)), 
                math.floor(self._scale_factor * (self._height)),
            )
        )
        pygame.draw.rect(
            self._text_surface, 
            (170,170,170), 
            (
                math.floor(self._scale_factor * 2), 
                math.floor(self._scale_factor * 2), 
                math.floor(self._scale_factor * self._width), 
                math.floor(self._scale_factor * self._height),
            )
        )
        pygame.draw.rect(
            self._text_surface, 
            (15, 48, 75), 
            (
                0, 
                0, 
                math.floor(self._scale_factor * (self._width + 4)), 
                math.floor(self._scale_factor * 32)
            )
        )
        
        self._text_surface.blit(self._font.render(self._name, True, 'white'), (230, 7))
        
        # ---------------------------------------------------
        
        if self._text_list != self._text_list_old:
        
            text_list: list[pygame.font.Font.render] = []
        
            colour_text_list = []
            match_index_list: list[tuple] = []
            self._colour_text_lines_list  = []
            for line in self._text_lines:
                #functions
                match_object_list = re.finditer(self._function_regex, line.split('#')[0])
                match_index_list = []
                for match_object in match_object_list:
                    match_index_list.append(match_object.span())
                
                for span in match_index_list:
                    colour_text_list.append((
                            self._font.render(line[span[0]:span[1]], True, (15, 48, 75)),
                            span[0], span[1]
                        )
                    )
                
                #numbers
                match_object_list = re.finditer(self._number_regex, line.split('#')[0])
                match_index_list = []
                for match_object in match_object_list:
                    match_index_list.append(match_object.span())
                
                for span in match_index_list:
                    colour_text_list.append((
                            self._font.render(line[span[0]:span[1]], True, (255, 255, 204)),
                            span[0], span[1]
                            )
                        )

                #Opperators
                match_object_list = re.finditer(self._operator_regex, line.split('#')[0])
                match_index_list = []
                for match_object in match_object_list:
                    match_index_list.append(match_object.span())
                
                for span in match_index_list:
                    colour_text_list.append((
                            self._font.render(line[span[0]:span[1]], True, (255, 255, 255)),
                            span[0], span[1]
                            )
                        )
                
                #coments
                match_object_list = re.finditer(self._coment_regex, line)
                match_index_list = []
                for match_object in match_object_list:
                    match_index_list.append(match_object.span())
                
                for span in match_index_list:
                    colour_text_list.append((
                            self._font.render(line[span[0]:span[1]], True, (0, 153, 51)),
                            span[0], span[1]
                            )
                        )
                    
                self._colour_text_lines_list.append(colour_text_list)
                colour_text_list = []
            
            self._text_lines_list: list[pygame.font.Font.render] = [self._font.render(text, True, (0, 0, 0)) for i, text in enumerate(self._text_lines)]
            
            self._line_numbers = [self._font.render(str(i), True, (217, 217, 217)) for i in range(len(self._text_lines))]
            
            self._text_list_old = self._text_list.copy()
        
        # ---------------------------------------------------------------
        
        for i, text in enumerate(self._text_lines_list):
            self._text_surface.blit(
                text, 
                (
                    math.floor(self._scale_factor * 42), 
                    i * self._font.size(' ')[1] + math.floor(self._scale_factor * 40)
                )
            )
        
        for i, text_list in enumerate(self._colour_text_lines_list):
            for text in text_list:
                self._text_surface.blit(
                    text[0], 
                    (
                        math.floor(self._scale_factor * 42) + text[1] *  self._font.size(' ')[0], 
                        i * self._font.size(' ')[1] + math.floor(self._scale_factor * 40)
                    )
                    )
        
        for i, number in enumerate(self._line_numbers):
            self._text_surface.blit(
                number, 
                (
                    math.floor(self._scale_factor * 3), 
                    i * self._font.size(' ')[1] + math.floor(self._scale_factor * 40)
                )
            )
            
        self._button_play.draw(self._text_surface)
        self._button_save.draw(self._text_surface)
        self._button_stop.draw(self._text_surface)
        self._draw_cursor()
        surface.blit(self._text_surface, self._coordinate)
        # raise KeyboardInterrupt
    
    def scale(self, scale_factor):
        self._scale_factor = scale_factor
        
        self._x = math.floor(self._scale_factor * 100)
        self._y = math.floor(self._scale_factor * 100)
        self._coordinate = (self._x, self._y)
        
        self._text_list_old = None
        
        self._button_play = \
            interfacec.Button(
                0,
                0,
                math.floor(self._scale_factor * 35),
                math.floor(self._scale_factor * 32),
                "play",
                math.floor(self._scale_factor * 9),
                lambda: self.run_code(), 
            )
        
        self._button_save = \
            interfacec.Button(
                math.floor(self._scale_factor * 35),
                0,
                math.floor(self._scale_factor * 35),
                math.floor(self._scale_factor * 32),
                "save",
                math.floor(self._scale_factor * 9),
                lambda: self.save(), 
            )
        
        self._button_stop = \
            interfacec.Button(
                math.floor(self._scale_factor * 35) * 2,
                0,
                math.floor(self._scale_factor * 35),
                math.floor(self._scale_factor * 32),
                'stop',
                math.floor(self._scale_factor * 9),
                lambda: self.stop(),
            )
               
    def test_file_select(self, coordinate):
        if self._x < coordinate[0] < self._x + math.floor(self._scale_factor * (self._width + 4)) and self._y < coordinate[1] < self._y + math.floor(self._scale_factor * (self._height + 4)):
            self.selected = True
            pygame.event.post(pygame.event.Event(self._custom_event_dict['TEXT_MODE']))
            self._button_play.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
            self._button_save.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
            self._button_stop.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
            
            if self._y < coordinate[1] < self._y + math.floor(self._scale_factor * 32): # top bar for mooving the window
                self.movable = True
            else:
                self.movable = False
               
                relative_x = coordinate[0] - self._x
                relative_y = coordinate[1] - self._y
                
                self._cursor_line = (relative_y-math.floor(self._scale_factor * 40))//self._font.size(' ')[1]
                if self._cursor_line > len(self._text_lines):
                    self._cursor_line = len(self._text_lines)
                
                self._cursor_index = (relative_x-math.floor(self._scale_factor * 35))//self._font.size(' ')[0]
                if self._cursor_index > len(self._text_lines[self._cursor_line]):
                    self._cursor_index = len(self._text_lines[self._cursor_line])
                
                index = 0 
                for i, line in enumerate(self._text_lines):
                        if i+1 > self._cursor_line:
                            break
                        index += len(line) + 1
                self._text_list_index = index + self._cursor_index
                
            return True
        else:
            if self.selected:
                self.selected = False
                pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
                self.movable = False
            return False
        
    def run_code(self):
        self.selected = False
        pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
        self.movable = False
        self.save()
        self.kill()
        self._code_prosessor.start()
        
    def save(self):
        self.selected = False
        pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
        self.movable = False
        with open(self._path, 'w') as file:
            file.write(''.join(self._text_list))
    
    def stop(self):
        self.selected = False
        pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
        self.movable = False
        self.kill()
    
    def send_event_value(self, event):
        if not self._event_queue.full():
            self._event_queue.put(event)
    
    def add_keystroke_to_queue(self, keystroke:str):
        if self._code_prosessor.is_alive():
            if not self._keypress_queue.full():
                self._keypress_queue.put(keystroke)
            else:
                self._keypress_queue.get()
                self._keypress_queue.put(keystroke)
        
    def move_text_edditer(self, rel_coordinate):
        if pygame.mouse.get_pressed(3)[0]:
            self._x, self._y = self._coordinate = rel_coordinate[0] + self._coordinate[0], rel_coordinate[1] + self._coordinate[1]
            
    def text_edditer(self, event: pygame.event.Event):
        print(event.key)
        # Gets keystroces as unicode character and inserts these in the string representation of the file
        # both the index of the string and the position of the cursor is changed
        
        #some keyes do not have a asci representation and to remove buggs this if statement i pased
        if event.key == pygame.K_BACKSPACE:
            # if the cursor is not at index 0 the function can delete items without causing out of 
            # bound error
            if self._text_list_index:
                #to destinguish between newline character and text we simpely test if the backspase 
                # is at the index 0 of a line
                #this is possible because the newline character is at the end of the previus line
                if self._cursor_index > 0:
                    self._text_list.pop(self._text_list_index -1)
                    self._text_list_index -= 1
                    self._cursor_index -= 1
                else: 
                    self._text_list.pop(self._text_list_index -1)
                    self._text_list_index -= 1
                    self._cursor_line -= 1
                    #the self._text_lines list has not been updated meaning we can use the lengt to 
                    # determine the corect position of the cursor after deleting a newline character
                    self._cursor_index = len(self._text_lines[self._cursor_line])
                    
        elif event.key == pygame.K_DELETE:
            if self._text_list_index < len(self._text_list):
                self._text_list.pop(self._text_list_index)   
                 
        elif event.key == 13: # enter
            self._text_list.insert(self._text_list_index, '\n')
            self._text_list_index += 1
            # the cursor has to be moved down one line and back to index 0
            self._cursor_index = 0
            self._cursor_line += 1
            
        elif event.key == pygame.K_TAB: # tab
            for _ in range(4):
                self._text_list.insert(self._text_list_index, ' ')
                self._text_list_index += 1
                self._cursor_index += 1
                
        elif event.key == pygame.K_UP:
            if self._cursor_line:
                self._cursor_line -= 1
                if self._cursor_index < len(self._text_lines[self._cursor_line]):
                    self._text_list_index -= len(self._text_lines[self._cursor_line]) + 1
                else:
                    self._text_list_index -= self._cursor_index + 1
                if len(self._text_lines[self._cursor_line]) <= self._cursor_index:
                    self._cursor_index = len(self._text_lines[self._cursor_line])
                
        elif event.key == pygame.K_RIGHT:
            if len(self._text_lines[self._cursor_line]) < self._cursor_index:
                self._cursor_index = len(self._text_lines[self._cursor_line])
            elif len(self._text_lines[self._cursor_line]) == self._cursor_index:
                if self._text_list_index < len(self._text_list):
                    self._cursor_index = 0
                    self._cursor_line += 1
                    self._text_list_index += 1
            else:
                self._cursor_index += 1 
                self._text_list_index += 1
                
        elif event.key == pygame.K_DOWN:
            if self._cursor_line < len(self._text_lines) -1:
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
            else:
                if self._cursor_line != 0:
                    self._cursor_line -= 1
                    self._cursor_index = len(self._text_lines[self._cursor_line])
                    self._text_list_index -= 1
        
        elif event.key == pygame.K_HOME:
            self._text_list_index -= self._cursor_index
            self._cursor_index = 0
            self._text_list_index = 0
            
        elif event.key == pygame.K_END:
            print('end')
            self._text_list_index += len(self._text_lines[self._cursor_line]) - self._cursor_index
            self._cursor_index = len(self._text_lines[self._cursor_line])
        else:
            self._text_list.insert(self._text_list_index, event.unicode)
            self._text_list_index += 1
            self._cursor_index += 1 
    
        
    def _draw_cursor(self):
        if self._draw_cursor_counter < 40:
            self._text_surface.blit(
                self._cursor, 
                (
                    self._cursor_index *  self._font.size(' ')[0] + math.floor(self._scale_factor * 35), 
                    self._cursor_line * self._font.size(' ')[1] + math.floor(self._scale_factor * 40)
                )
            )
            self._draw_cursor_counter += 1
        else:
            self._draw_cursor_counter += 1
            
        if self._draw_cursor_counter > 80:
            self._draw_cursor_counter = 0
            
    def kill(self):
        print('kill')
        try:
            self._code_prosessor.terminate()
            self._code_prosessor.join()
        except:
            pass
        finally:
            self._code_prosessor = \
            Code_prosessor(
                    self._name, 
                    self._path, 
                    self._custom_event_queue, 
                    self._multiprocessing_draw_queue,
                    self._keypress_queue,
                    self._event_queue,
                )
        
    def join(self, values):
        self._code_prosessor.join()
        self._code_prosessor = \
            Code_prosessor(
                self._name, 
                self._path, 
                self._custom_event_queue, 
                self._multiprocessing_draw_queue, 
                self._keypress_queue,
                self._event_queue,
                values[1], 
                values[2],
                values[3], 
                values[4], 
                values[5]
            )
            
class Code_prosessor(multiprocessing.Process):
    def __init__(
            self, 
            name, 
            path, 
            custom_event_queue: multiprocessing.Queue, 
            multiprocessing_draw_queue: multiprocessing.Queue, 
            keypress_queue: multiprocessing.Queue,
            event_queue: multiprocessing.Queue,
            x: float = 500, 
            y: float = 300, 
            width: float = 100, 
            height: float = 100, 
            angle: float = 0,
            sprite: str = 'icon.png'
            
        ):
        super(Code_prosessor, self).__init__()
        
        self._name = name
        self._path = path
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._angle = angle
        self._custom_event_queue = custom_event_queue
        self._framerate = 60
        self._time = 0.5
        self._steps = int(self._framerate * self._time)
        self._step_dist = int(200/self._steps)
        self._image_path = Path(__file__).parent / Path('sprites') / Path(sprite)
        self._multiprocessing_draw_queue = multiprocessing_draw_queue
        self._multiprocessing_draw_queue.put(
            (
                self._name,             #0
                self._image_path,       #1
                self._x,                #2
                self._y,                #3
                self._width,            #4
                self._height,           #5  
                self._angle             #6
            )
        )
        self._keypress_queue = keypress_queue
        self._event_queue = event_queue
        self._on_hit = False
        self._mouse_coords = (0,0)
    
    def run(self):
        self._timer = time.time()
        try:
            with open(self._path, 'r') as file:
                lines = file.read()
            exec(lines, 
                {
                    'move': Add__str__func(self.move), 
                    'move_to': Add__str__func(self.move_to),
                    'move_to_cursor': Add__str__func(self.move_to_cursor),
                    'sleep': Add__str__func(self.sleep), 
                    'timer': Add__str__func(self.timer), 
                    'scale': Add__str__func(self.scale),
                    'set_sprite': Add__str__func(self.set_sprite),
                    'random': Add__str__func(self.random), 
                    'turn': Add__str__func(self.turn), 
                    'print': Add__str__func(self.print),
                    'keypress': Add__str__func(self.keypress),
                    'on_hit': Add__str__func(self.on_hit),
                    'play_sound': Add__str__func(self.play_sound),
                }
            )
        except Exception as e:
            print(
                f'##############################################################################\n'
                f'{e}\n'
                f'\n'
                f'{traceback.format_exc()}'
                f'##############################################################################\n'
            )
        finally:
            self._custom_event_queue.put((self._name, ('end'), None))
        
    def move(self, distance: Optional[float] = None, time: Optional[float] = None, direction: Optional[str] = None):
        """
        Moves the sprite

        Args:
            distance (float, optional): Distance the sprite is moved.
            time (float, optional): Time the sprite takes to move the spesified distance
            direction (str, optional): Direction the sprite is moved in. 
                If None the sprite moves in the direction spessified by the turn() function

        Examples:
            >>> move(distance=100, time=1, direction='rught')
            Moves the sprite 100 pixels to the right for a duration of 1 second.
            
            >>> move(100, 1, 'rught')
            Moves the sprite 100 pixels to the right for a duration of 1 second.
            
            >>> move(100, 1)
            Moves the sprite 100 pixels in the direction of the sprite for 1 a duration of 1 second.
            
            >>> move(100)
            Moves the sprite 100 pixels instantaniusly.
        """
        if time:
            self._time = time
            self._steps = int(self._framerate * self._time)
        else:
            self._time = 0
            self._steps = 1
        
        if distance:
            self._step_dist = int(distance/self._steps)
            
        clock = pygame.time.Clock()
        if direction == 'up':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_UP'].set()
                self._y -= self._step_dist
                self._multiprocessing_draw_queue.put(
                    (
                        self._name, 
                        self._image_path, 
                        self._x, self._y, 
                        self._width, 
                        self._height, 
                        self._angle
                    )
                ) 
                if self._time:               
                    clock.tick(self._framerate)
        elif direction == 'right':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_RIGHT'].set()
                self._x += self._step_dist
                self._multiprocessing_draw_queue.put(
                    (
                        self._name, 
                        self._image_path, 
                        self._x, self._y, 
                        self._width, 
                        self._height, 
                        self._angle
                    )
                )                
                clock.tick(self._framerate)
        elif direction == 'down':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_DOWN'].set()
                self._y += self._step_dist
                self._multiprocessing_draw_queue.put(
                    (
                        self._name, 
                        self._image_path, 
                        self._x, self._y, 
                        self._width, 
                        self._height, 
                        self._angle
                    )
                )
                clock.tick(self._framerate)
        elif direction == 'left':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_LEFT'].set()
                self._x -= self._step_dist
                self._multiprocessing_draw_queue.put(
                    (
                        self._name, 
                        self._image_path, 
                        self._x, self._y, 
                        self._width, 
                        self._height, 
                        self._angle
                    )
                )                
                clock.tick(self._framerate)
        else:
            for _ in range(self._steps):
                self._x += self._step_dist * math.cos(math.radians(self._angle))
                self._y -= self._step_dist * math.sin(math.radians(self._angle))
                self._multiprocessing_draw_queue.put(
                    (
                        self._name, 
                        self._image_path, 
                        self._x, self._y, 
                        self._width, 
                        self._height, 
                        self._angle
                    )
                )                
                clock.tick(self._framerate)
    
    def move_to(self, x: int, y: int):
        '''
        moves the sprite to the specified coordinates
        
        Args:
            x (int): x coordinate
            y (int): y coordinate
        
        Example:
            >>> move_to(100,100)
                The sprite telleports to coordinates 100x, 100y
        '''
        self._x = x
        self._y = y
        self._multiprocessing_draw_queue.put(
            (
                self._name, 
                self._image_path, 
                self._x, self._y, 
                self._width, 
                self._height, 
                self._angle
            )
        )
    
    def move_to_cursor(self, distance: int, time: float = None):
        '''
        moves and rotates the sprite towards the cursor
        
        Args:
            distance (int): distance to move
            time (float, optional): time to move. Defaults to None.
            
        Example:
            >>> move_to_cursor(100, 1)
                The sprite rotates and moves 100 pixels towards the cursor over 1 second
        '''
        self._handle_event_value()
        # print(self._mouse_coords)
        relative_x = self._mouse_coords[0] - self._x
        relative_y = self._mouse_coords[1] - self._y
        angle = math.degrees(math.atan2(-relative_y, relative_x))
        self.turn(angle, True)
        self.move(distance, time)
    
    def turn(self, angle, absolute = False):
        '''
        turnes the sprite eather by a relative or absolute angle
        
        Args:
            angle (int): angle to turn
            absolute (bool, optional): defines if the angle is absolute or relative. Defaults to False.
        
        Example:
            >>> turn(90)
                The sprite turns 90 degrees rellative to current rotation
            >>> turn(90, True)
                The sprite turns to 90 degrees rellative to the display
        '''
        if absolute:
            self._angle = angle
        else:  
            self._angle += angle
            
        while 0 > self._angle < 360:
            if self._angle > 360:
                self._angle -= 360
            elif self._angle < 0:
                self._angle += 360
                
        self._multiprocessing_draw_queue.put((self._name, self._image_path, self._x, self._y, self._width, self._height, self._angle))
     
    def scale(self, width: int, height: int):
        '''
        changes the scale of the sprite

        Args:
            width (int): new width
            height (int): new height
            
        Example:
            >>> scale(100, 100)
                The sprite is scaled to 100x100 pixels
        '''
        self._width = width
        self._height = height
        self._multiprocessing_draw_queue.put(
            (
                self._name,             #0
                self._image_path,       #1
                self._x,                #2
                self._y,                #3
                self._width,            #4
                self._height,           #5  
                self._angle             #6
            )
        )
    
    def set_sprite(self, image_name: str):
        '''
        tries to find a sprite with image_name in the folder 'sprites' and sets it as the sprite
        if image has been loaded earlier the image is searched for in ram.
        
        Args:
            image_name (str): name of the sprite
            
        Example:
            >>> set_sprite('icon.png')
                The 'icon.png' image file is searched for and loaded as the new sprite.
        '''
        self._image_path = Path(__file__).parent / Path('sprites') / Path(image_name)
        self._multiprocessing_draw_queue.put(
            (
                self._name,             #0
                self._image_path,       #1
                self._x,                #2
                self._y,                #3
                self._width,            #4
                self._height,           #5  
                self._angle             #6
            )
        )
        
    def sleep(self, secounds):
        '''
        Runs a sleep comand pausing the file execution.
        
        Args:
            secounds (float): The amount of secounds to pause the file execution.
        
        Examples:
            >>> sleep(1)
                Pauses the program for 1 secound
            >>> sleep(0.1)
                Pauses the program for 0.1 secounds
        '''
        time.sleep(secounds)
    
    def timer(self, reset = False):
        '''
        A timer returning time since timer start or resets the timer
        
        Args:
            reset (bool, optional): If True, resets the timer.
        
        Examples:
            >>> timer()
                Returns the time since the timer was started
            >>> timer(True)
                Resets the timer
        '''
        if reset:
            self._timer = time.time()
        else:
            return time.time() - self._timer
    
    def random(self, min_value = None, max_value = None, float_value = False):
        '''
        Returns a random number.
        
        Args:
            min_value (float, optional): The minimum value of the random number.
            max_value (float, optional): The maximum value of the random number.
            float_value (bool, optional): If True, returns a float (desimal) value.
            
        Examples:
            >>> random()
                Returns a random number between 0 and 1. [0 or 1]
            >>> random(1, 10)  
                Returns a random number between 1 and 10. [1 or 3 or 7 or 4 or 10 or 2 or 5]
            >>> random(1, 10, True)
                Returns a random float between 1 and 10. [1.234 or 3.456 or 7.890 or 4.321 or 9.123 or 2.345 or 5.678]
        '''
        random_num =  random.random()
        if min_value and max_value:
            random_num = random_num*(max_value-min_value) + min_value
        elif min_value:
            random_num = random_num + min_value
        elif max_value:
            random_num = random_num*max_value
        if not float_value:
            random_num = int(random_num)
        return random_num
    
    def print(self, string: str = '', time_delay: Optional[float] = 1):
        '''
        
        
        Args:
            string (str, optional): The text to print.
            time_delay (float, optional): The amount of secounds to wait before printing the next character.
            
        Examples:
            >>> print('Hello World')
                Prints 'Hello World' at the current sprite posistion the text lasts for 1 secound
            >>> print('Hello World', 0.5)
                Prints 'Hello World' at the current sprite posistion the text lasts for 0.5 secounds
        '''
        self._custom_event_queue.put((self._name, ('print'), (str(string), self._x, self._y, time_delay)))
        # time.sleep(time_delay)
    
    def keypress(self):
        '''
        listens for a players keyboard innput
        the keypress que stores the last 4 keys and returns the first key in the queue
        '''
        if self._keypress_queue.empty():
            return None
        else:
            return self._keypress_queue.get()

    def on_hit(self, target):
        '''
        returns True if the sprite of the file edditor spesified overlaps the current sprite.
        Due to multiprossesing this functionality currentleuy onley workes reliabley in one direction.
        '''
        self._custom_event_queue.put((self._name, 'on_hit', target))
        time.sleep(0.006) # allows the main code to try to execute leading to the some false negatives.
        # The test will return correctley on the next frame. but the function neads to re runn
        self._handle_event_value()
        if self._on_hit:
            self._on_hit = False
            return True
        else:
            return False
        
    def _handle_event_value(self):
        while not self._event_queue.empty():
            print('test')
            event, value = self._event_queue.get()
            if event == 'mouse_coords':
                self._mouse_coords = value
            elif event == 'on_hit':
                self._on_hit = True
            
    def play_sound(self, sound_file: str, volume: float = 1):
        '''
        plays a sound file
        
        Args:
            sound_file (str): The name of the sound file to play.
            volume (float, optional): The volume of the sound.
        
        Examples:
            >>> play_sound('jump.wav')
                Plays the sound file 'thump.mp3' volume of 1
            >>> play_sound('jump.wav', 0.5)
                Plays the sound file 'thump.mp3' volume of 0.5
        '''
        path = Path(__file__).parent/ Path('sounds') / Path(sound_file)
        self._custom_event_queue.put((self._name, 'sound', (path, volume)))
                                
class Add__str__func:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return self.__doc__
    