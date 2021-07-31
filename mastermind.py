import pygame, sys
from pygame.locals import *
import random
import os

DEFAULT_CODE_LENGTH=5

WHITE={'name':'white','rbg':(255,255,255),'ansi':'\033[38;2;255;255;255m\u2588\033[0m'}
RED={'name':'red','rbg':(255,0,0),'ansi':'\033[38;2;255;0;0m\u2588\033[0m'}
BLACK={'name':'black','rbg':(0,0,0),'ansi':'\033[38;2;0;0;0m\u2588\033[0m'}

BLUE={'name':'blue','rbg':(0,0,255),'ansi':'\033[38;2;0;0;255m\u2588\033[0m'}
LTGRN={'name':'ltgrn','rbg':(22,221,53),'ansi':'\033[38;2;22;221;53m\u2588\033[0m'}   #
GREEN={'name':'green','rbg':(0,117,58),'ansi':'\033[38;2;0;117;58m\u2588\033[0m'}
ORANGE={'name':'orange','rbg':(255,169,0),'ansi':'\033[38;2;255;169;0m\u2588\033[0m'}
PURPLE={'name':'purple','rbg':(127, 0, 255),'ansi':'\033[38;2;127;0;255m\u2588\033[0m'}
YELLOW={'name':'yellow','rbg':(255,255,0),'ansi':'\033[38;2;255;255;0m\u2588\033[0m'}
GREY={'name':'grey','rbg':(128,128,128),'ansi':'\033[38;2;128;128;128m\u2588\033[0m'}
PINK={'name':'pink','rbg':(241,179,179),'ansi':'\033[38;2;241;179;179m\u2588\033[0m'}

CODE_COLORS = [BLUE,LTGRN,GREEN,ORANGE,PURPLE,YELLOW,GREY,PINK]
CLUE_COLORS = [RED,WHITE]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        output = ' '.join([a['ansi'] for a in self.code])
        return output
        
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