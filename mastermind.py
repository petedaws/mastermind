import random
import curses
from curses import wrapper


# GAME PARAMS
CODE_LENGTH = 5
MAX_CONJECTURES = 20
CODE_VALUES = ['A','B','C','D','E','F','G','H']
CORRECT_VALUE = '!'
CORRECT_VALUE_AND_POSITION = 'X'
INCORRECT_VALUE = ' '

# SCREEN PARAMS
Y_SCREEN_CURSOR_OFFSET = MAX_CONJECTURES + 5
Y_SCREEN_CONJECTOR_OFFSET = MAX_CONJECTURES


def get_clue(code,secret):
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
    for element in copy_code:
        if element in copy_secret:
            clue.append(CORRECT_VALUE)
            copy_secret.remove(element)


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
        self.clues = []
    
    def make_conjecture(self,conjecture):
        cj = Code(conjecture.copy())
        self.conjectures.append(cj)
        self.clues.append(get_clue(cj,self.secret))
    
    def __str__(self):
        output = []
        
        for i,conjecture in enumerate(reversed(self.conjectures)):
            output.append(f'#:{len(self.conjectures)-i}\t{conjecture}\t[{self.clues[i]}]')
        output.append(f'#:S\t{self.secret}')
        return '\n\n'.join(output)
        
class Code():
    def __init__(self,code=[],code_length=CODE_LENGTH):
        self.code_length = code_length
        self.code = code
        
    def generate_random(self):
        for i in range(self.code_length):
            self.code.append(random.choice(CODE_VALUES))
    
    def __str__(self):
        output = ' '.join([a for a in self.code])
        return output
    
    def copy(self):
        return self.code.copy()
    
    def str_hidden(self):
        output = ' '.join(['\u2588' for a in self.code])
        return output
        
    def hidden(self):
        return ['\u2588' for a in self.code]


def gamescreen(screen):
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    screen.clear()
    screen_dimensions = screen.getmaxyx()
    y_cursor_position = Y_SCREEN_CURSOR_OFFSET
    X_SCREEN_OFFSET = int(screen_dimensions[1] / 2) - CODE_LENGTH # the game is played in the middle of the screen
    x_cursor_position = X_SCREEN_OFFSET
    input_key = -1
    selection_position = 0
    selection = 0
    current_conjecture = Code([' '] * CODE_LENGTH)
    gs = GameState()
    show_answer = False
    while input_key != 'q':
        screen.clear()
        screen.addstr(y_cursor_position, x_cursor_position, '\u25B2') # This is the position of the small triangle cursor
        screen.addstr(y_cursor_position-1, X_SCREEN_OFFSET, ' '.join(['\u203E'] * CODE_LENGTH)) # This is the position of the overscores
        

        for i,code_value in enumerate(current_conjecture.code): # this is where the current conjection gets placed
            if i == selection_position:
                screen.addstr(y_cursor_position-2, X_SCREEN_OFFSET+i*2, CODE_VALUES[selection])
            else:
                screen.addstr(y_cursor_position-2, X_SCREEN_OFFSET+i*2, current_conjecture.code[i])
                
        if show_answer:
            screen.addstr(y_cursor_position+1, X_SCREEN_OFFSET, ' '.join(gs.secret.code))
        else:
            screen.addstr(y_cursor_position+1, X_SCREEN_OFFSET, ' '.join(gs.secret.hidden()))
        
        screen.addstr(y_cursor_position-4-len(gs.conjectures), X_SCREEN_OFFSET-3, '>') # this is an arrow pointing to the next conjecture location
        for i,conj in enumerate(gs.conjectures): # These are the historical conjectures
            screen.addstr(y_cursor_position-5-i, X_SCREEN_OFFSET-4, f'{i:02}| {conj}\t[{gs.clues[i]}]')
        
        screen.refresh()
        input_key = screen.getkey()
        if input_key == 'd':
            selection_position += 1
            if selection_position > CODE_LENGTH-1:
                selection_position = 0
                
        elif input_key == 'a':
            selection_position -= 1
            if selection_position < 0:
                selection_position = CODE_LENGTH-1
                
        elif input_key == 'w':
            selection += 1
            if selection > len(CODE_VALUES)-1:
                selection = 0
                
        elif input_key == 's':
            selection -= 1
            if selection < 0:
                selection = len(CODE_VALUES)-1
                
        elif input_key == ' ':
            current_conjecture.code[selection_position] = CODE_VALUES[selection]
            
        elif input_key == 'e':
            gs.make_conjecture(current_conjecture)
            current_conjecture = Code([' '] * CODE_LENGTH)
            
        elif input_key == 'h':
            show_answer = not show_answer
            
        x_cursor_position = X_SCREEN_OFFSET + selection_position * 2
        
            
    curses.endwin()

if __name__ == '__main__':
    wrapper(gamescreen)