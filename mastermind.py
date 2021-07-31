import pygame, sys
from pygame.locals import *
import random
import os

DEFAULT_CODE_LENGTH=5

WHITE={'name':'white','rgb':(255,255,255)}
RED={'name':'red','rgb':(255,0,0)}
BLACK={'name':'black','rgb':(0,0,0)}

BLUE={'name':'blue','rgb':(0,0,255)}
LTGRN={'name':'ltgrn','rgb':(22,221,53)}
GREEN={'name':'green','rgb':(0,117,58)}
ORANGE={'name':'orange','rgb':(255,169,0)}
PURPLE={'name':'purple','rgb':(127, 0, 255)}
YELLOW={'name':'yellow','rgb':(255,255,0)}
GREY={'name':'grey','rgb':(128,128,128)}
PINK={'name':'pink','rgb':(241,179,179)}

CODE_COLORS = [BLUE,LTGRN,GREEN,ORANGE,PURPLE,YELLOW,GREY,PINK]
CLUE_COLORS = [RED,WHITE,BLACK]

class GameBoard():
    pass

def get_clue_str(code,secret):
    clue = []
    copy_code = code.code.copy()
    copy_secret = secret.code.copy()
    red_index = []
    
    #identify the reds first and keep track these elements so we can remove them from the copy
    for i,element in enumerate(copy_code):
        if element == copy_secret[i]:
            clue.append(RED)
            red_index.append(element)
            
    #remove the indexes of items that match from the copy
    for element in red_index:
        copy_secret.remove(element)
        copy_code.remove(element)
    
    #now identify the whites
    for i,element in enumerate(copy_code):
        if element in copy_secret:
            clue.append(WHITE)

    #fill the remaining clue places with black
    while len(clue) < len(secret.code):
        clue.append(BLACK)
        
    #output the clue results in a random order
    random.shuffle(clue)
    o = Code(clue)
    return o
        
   
class GameState():
    def __init__(self):
        self.secret = Code()
        self.secret.generate_random()
        self.conjectures = []
    
    def make_conjecture(self,conjecture):
        cj = Code(conjecture)
        self.conjectures.append(cj)
    
    def __str__(self):
        output = []
        
        for i,conjecture in enumerate(reversed(self.conjectures)):
            output.append(f'#:{len(self.conjectures)-i}\t{conjecture.str_ansi()}\t[{get_clue_str(conjecture,self.secret).str_ansi()}]')
        output.append(f'#:S\t{self.secret.str_ansi()}')
        return '\n\n'.join(output)
        
class Code():
    def __init__(self,code=[],code_length=DEFAULT_CODE_LENGTH):
        self.code_length = code_length
        self.code = code
        
    def generate_random(self):
        for i in range(self.code_length):
            self.code.append(random.choice(CODE_COLORS))
    
    def __str__(self):
        output = ' '.join([a['name'] for a in self.code])
        return output
        
    def str_ansi(self):
        output = []
        for a in self.code:
            r = a['rgb'][0]
            g = a['rgb'][1]
            b = a['rgb'][2]
            output.append(f'\033[38;2;{r};{g};{b}m\u2588\033[0m')
        return ' '.join(output)
        
    def str_hidden(self):
        output = ' '.join(['X' for a in self.code])
        return output

def main():
    os.system("") # need to run the systemcommand to make ascii colours work
    gs = GameState()
    gs.make_conjecture([BLUE,LTGRN,GREEN,ORANGE,PURPLE])
    gs.make_conjecture([BLUE,BLUE,BLUE,BLUE,BLUE])
    gs.make_conjecture([GREY,GREY,GREY,GREY,GREY])
    gs.make_conjecture([LTGRN,LTGRN,LTGRN,LTGRN,LTGRN])
    gs.make_conjecture([YELLOW,GREY,PINK,BLUE,LTGRN])
    print(gs)

if __name__ == '__main__':
    main()