#import multiprocessing.process
import multiprocessing
import multiprocessing.context
import multiprocessing.queues
import pygame
import imports.interfacec as interfacec
from pathlib import Path
import traceback
from typing import Optional, Union
import time
import multiprocessing
import functools
import random
import math


class Game:
    def __init__(self, surface: pygame.Surface, width = 0, height = 0, custom_event_dict: dict[str, pygame.event.Event] = {}):
        self._width = width
        self._height = height
        self._surface = surface
        self._file_dict: dict[str, File_wiewer] = {}
        
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
        
        self._multiprocessing_draw_queue = multiprocessing.Queue(128)
        self._multiprocessing_draw_dict = {}
        self._custom_event_queue= multiprocessing.Queue(128)
        
    def draw(self):
        while not self._custom_event_queue.empty():
            file, comand = self._custom_event_queue.get()
            if comand == 'end':
                self._file_dict[file].join(self._multiprocessing_draw_dict[file])
        
        for values in self._multiprocessing_draw_dict.values():
            image = self.load_image(values[0])
            image = pygame.transform.scale(image, (values[3], values[4]))
            surface = pygame.transform.rotate(image, values[5])
            new_rect = surface.get_rect(center = image.get_rect(center = (values[1], values[2])).center)
            self._surface.blit(surface, new_rect)
            
        for button in self._button_list:
            button.draw(self._surface)
            
        for file in self._file_dict.values():
            file.draw(self._surface)
            
        while not self._multiprocessing_draw_queue.empty():
            self._multiprocessing_draw_queue_handler(self._multiprocessing_draw_queue.get())
    
    @functools.lru_cache(maxsize=128)        
    def _multiprocessing_draw_queue_handler(self, values: tuple):
        self._multiprocessing_draw_dict[values[0]] = (values[1], values[2], values[3], values[4], values[5], values[6])
        
    def _append_file(self):
        file_name = f'code_file_{len(self._file_dict)}'
        path = Path(__file__).parent.parent \
            / Path('save') / Path('save_1') \
            / Path(file_name + '.py')
            
        self._file_dict[file_name] = File_wiewer(
            file_name, 
            path, 
            self._custom_event_dict, 
            self._multiprocessing_draw_queue, 
            self._custom_event_queue
        )
    
    def eddit_file(self, keystroke: str):
        for file in self._file_dict.values():
            if file.selected:
                file.text_edditer(keystroke)
                break
    
    def send_key_to_file_wiewer(self, event):
        for file in self._file_dict.values():
            if file.selected:
                file.move_cursor(event)
    
    def on_mouse_press(self, coordinate):
        for button in self._button_list:
            button.test_button_press(coordinate)
            
        for file in self._file_dict.values():
            file.test_file_select(coordinate)
    
    def move_file_wiewer(self, rel_coordinate):
        for file in self._file_dict.values():
            if file.movable:
                file.move_text_edditer(rel_coordinate)
    
    @functools.lru_cache(maxsize=128)
    def load_image(self, path):
        return pygame.image.load(path)
    
    def pause(self):
        self._button_list = []
        
    def resume(self):
        self._button_list = [self._button_new_file]
     
    def kill(self):
        for file in self._file_dict.values():
            file.kill()   
        
class File_wiewer:
    def __init__(self, name, path, custom_event_dict, multiprocessing_draw_queue, custom_event_queue):
        self._path = path
        self._name = name
        
        self._x = 100
        self._y = 100
        self._width = 1000
        self._height = 1000
        self._rectvalue = [0, 0, self._width, self._height]
        self._coordinate = (self._x, self._y)
        
        self._text_surface = pygame.Surface((self._width, self._height))
        self._custom_event_dict = custom_event_dict
        self._multiprocessing_draw_queue = multiprocessing_draw_queue
        self._custom_event_queue = custom_event_queue
        self._code_prosessor = Code_prosessor(self._name, self._path, self._custom_event_queue, self._multiprocessing_draw_queue)
        
        self._button_play = \
            interfacec.Button(
                0, 0, 64, 32, 
                "play",
                lambda: self.run_code(), 
            )
        
        self._button_save = \
            interfacec.Button(
                64, 0, 64, 32, 
                "save",
                lambda: self.save(), 
            )
        
        self.selected = False
        self.movable = False
        if not Path.is_file(self._path):
            with open(self._path, 'x'):
                pass
        with open(self._path, 'r') as file:
            self._text_list = list(file.read())
            
        self._text_surface = pygame.Surface((self._width, self._height))
        self._text_lines: list[str] = []
        self._font= pygame.font.Font(Path(__file__).parent / Path('Consolas.ttf'), 20)
        
        self._cursor = self._font.render('|', True, 'white')
        self._cursor_index = 0
        self._cursor_line = 0
        self._text_list_index = 0
        
    def draw(self, surface: pygame.Surface):
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
        self._height = len(self._text_lines) * 20 + 40 + 10
        self._rectvalue[2] = self._width
        self._text_surface = pygame.transform.scale(self._text_surface, (self._width, self._height))
        pygame.draw.rect(self._text_surface, (170,170,170), self._rectvalue)
        pygame.draw.rect(self._text_surface, (30-15, 63-15, 90-15), (0, 0, self._width, 32))
        
        self._text_surface.blit(self._font.render(self._name, True, 'white'), (130, 7))
        
        text_list: list[pygame.font.Font.render] = [self._font.render(text, True, 'white') for i, text in enumerate(self._text_lines)]
        line_numbers = [self._font.render(str(i), True, 'white') for i in range(len(self._text_lines))]
        
        for i, text in enumerate(text_list):
            self._text_surface.blit(text, (40, i*20 + 40))
        
        for i, number in enumerate(line_numbers):
            self._text_surface.blit(number, (0, i*20 + 40))
            
        self._button_play.draw(self._text_surface)
        self._button_save.draw(self._text_surface)
        self._draw_cursor()
        surface.blit(self._text_surface, self._coordinate)
                
    def test_file_select(self, coordinate):
        if self._x < coordinate[0] < self._x + self._width and self._y < coordinate[1] < self._y + self._height:
            self.selected = True
            pygame.event.post(pygame.event.Event(self._custom_event_dict['TEXT_MODE']))
            if self._y < coordinate[1] < self._y + 32:
                self.movable = True
        else:
            if self.selected:
                self.selected = False
                pygame.event.post(pygame.event.Event(self._custom_event_dict['GAME_MODE']))
                self.movable = False
        
        self._button_play.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
        self._button_save.test_button_press((coordinate[0]-self._x, coordinate[1]-self._y))
        
    def run_code(self):
        self.save()
        if not self._code_prosessor.is_alive():
            self._code_prosessor.start()
        
    def save(self):
        with open(self._path, 'w') as file:
            file.write(''.join(self._text_list))
    
    def text_edditer(self, keystroke: str):
        # Gets keystroces as unicode character and inserts these in the string representation of the file
        # both the index of the string and the position of the cursor is changed
        
        #some keyes do not have a asci representation and to remove buggs this if statement i pased
        if keystroke == '':
            pass
        # the backspace button has to both delete indexes and move the cursor. if a newline character 
        # is deleted the cursor haas to move upp one line
        elif keystroke == '\x08': # backspace
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
        # Enter is used to add a newline to the dokkument          
        elif keystroke == '\r':
            self._text_list.insert(self._text_list_index, '\n')
            self._text_list_index += 1
            # the cursor has to be moved down one line and back to index 0
            self._cursor_index = 0
            self._cursor_line += 1
        #every other char is simly printed to the dokument. 
        #This means that button presses like delete or CapsLock will be printed
        #More finetuneing neaded
        else:
            self._text_list.insert(self._text_list_index, keystroke)
            self._text_list_index += 1
            self._cursor_index += 1 
    
    def move_text_edditer(self, rel_coordinate):
        if pygame.mouse.get_pressed(3)[0]:
            self._x, self._y = self._coordinate = rel_coordinate[0] + self._coordinate[0], rel_coordinate[1] + self._coordinate[1]
    
    def move_cursor(self, event):
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
            if len(self._text_lines[self._cursor_line]) < self._cursor_index:
                self._cursor_index = len(self._text_lines[self._cursor_line])
            elif len(self._text_lines[self._cursor_line]) == self._cursor_index:
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
            
    def _draw_cursor(self):
        self._text_surface.blit(self._cursor, (self._cursor_index * 11 + 35, self._cursor_line*20 + 40))
            
    def kill(self):
        if self._code_prosessor.is_alive():
            self._code_prosessor.kill()
    
    def join(self, values):
        self._code_prosessor.join()
        self._code_prosessor = Code_prosessor(
            self._name, 
            self._path, 
            self._custom_event_queue, 
            self._multiprocessing_draw_queue, 
            values[1], 
            values[2],
            values[3], 
            values[4], 
            values[5]
        )
            
class Code_prosessor(multiprocessing.Process):
    def __init__(self, name, path, custom_event_queue: multiprocessing.Queue, multiprocessing_draw_queue: multiprocessing.Queue, x: float = 500, y: float = 300, width: float = 100, height: float = 100, angle: float = 0):
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
        print(self._framerate)
        self._image_path = Path(__file__).parent / Path('sprites') / Path('icon.png')
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
    
    def run(self):
        self._timer = time.time()
        try:
            with open(self._path, 'r') as file:
                lines = file.read()
                exec(lines, {'move': self.move, 'wait': self.wait, 'timer': self.timer, 'turn': self.turn})
        except Exception as e:
            print(
                f'##############################################################################\n'
                f'{e}\n'
                f'\n'
                f'{traceback.format_exc()}'
                f'##############################################################################\n'
            )
        finally:
            self._custom_event_queue.put((self._name, ('end')))
        
    def move(self, distance: Optional[float] = None, time: Optional[float] = None, direction: Optional[str] = None):
        if time:
            self._time = time
            self._steps = int(self._framerate * self._time)
        if distance:
            self._step_dist = int(distance/self._steps)
            
        clock = pygame.time.Clock()
        if direction == 'up':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_UP'].set()
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
        elif direction == 'right':
            for _ in range(self._steps):
                #self._custom_event_dict['MOVE_RIGHT'].set()
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
    
    def wait(self, secounds):
        time.sleep(secounds)
    
    def timer(self, reset = False):
        if reset:
            self._timer = time.time()
        else:
            return time.time() - self._timer
    
    def random(self, min = None, max = None, float_value = False):
        random_num =  random.random()
        if min:
            random_num = random_num + min
        elif min and max:
            random_num = random_num*(max-min) + min
        elif max:
            random_num = random_num*max
        if not float_value:
            random_num = int(random_num)
        return random_num
    
    def turn(self, angle, absolute = False):
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
            

            