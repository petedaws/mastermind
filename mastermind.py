import pygame, sys
from pygame.locals import *
import random
import os

DEFAULT_CODE_LENGTH = 5
MAX_CONJECTURES = 12

CODE_VALUES = ['A','B','C','D','E','F','G','H']

CORRECT_VALUE = '!'
CORRECT_VALUE_AND_POSITION = 'X'
INCORRECT_VALUE = ' '

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
            clue.append(CORRECT_VALUE_AND_POSITION)
            red_index.append(element)
            
    #remove the indexes of items that match from the copy
    for element in red_index:
        copy_secret.remove(element)
        copy_code.remove(element)
    
    #now identify the whites
    for i,element in enumerate(copy_code):
        if element in copy_secret:
            clue.append(CORRECT_VALUE)

    #fill the remaining clue places with black
    while len(clue) < len(secret.code):
        clue.append(INCORRECT_VALUE)
    
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
            output.append(f'#:{len(self.conjectures)-i}\t{conjecture}\t[{get_clue_str(conjecture,self.secret)}]')
        output.append(f'#:S\t{self.secret}')
        return '\n\n'.join(output)
        
class Code():
    def __init__(self,code=[],code_length=DEFAULT_CODE_LENGTH):
        self.code_length = code_length
        self.code = code
        
    def generate_random(self):
        for i in range(self.code_length):
            self.code.append(random.choice(CODE_VALUES))
    
    def __str__(self):
        output = ' '.join([a for a in self.code])
        return output
    
    def str_hidden(self):
        output = ' '.join(['\u2588' for a in self.code])
        return output

def main():
    os.system("") # need to run the systemcommand to make ascii colours work
    gs = GameState()
    gs.make_conjecture(['A','A','A','A','A'])
    gs.make_conjecture(['B','B','B','B','B'])
    gs.make_conjecture(['C','C','C','C','C'])
    gs.make_conjecture(['A','B','C','D','E'])
    gs.make_conjecture(['F','G','H','A','B'])
    print(gs)

if __name__ == '__main__':
    main()