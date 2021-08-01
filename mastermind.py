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
    copy_code = code.copy()
    copy_secret = secret.copy()
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
    while len(clue) < len(secret):
        clue.append(INCORRECT_VALUE)
    
    #output the clue results in a random order
    random.shuffle(clue)
    return clue
        
def generate_random(code_length):
    code = []
    for i in range(code_length):
        code.append(random.choice(CODE_VALUES))
    return code

def str_code(code):
    output = ' '.join([a for a in code])
    return output
    
def str_hidden(code):
    output = ' '.join(['\u2588' for a in code])
    return output

class GameState():
    def __init__(self):
        self.code_length = CODE_LENGTH
        self.code_values = CODE_VALUES
        self.max_conjectures = MAX_CONJECTURES
        self.secret = generate_random(self.code_length)
        self.conjectures = []
        self.clues = []
    
    def make_conjecture(self,conjecture):
        self.conjectures.append(conjecture.copy())
        self.clues.append(get_clue(conjecture,self.secret))

def curses_setup():
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
  
class GameScreen():

    def __init__(self):
        
        self.cursor_position = 0
        self.selection = 0
        self.gs = GameState()
        self.show_answer = False
        self.current_conjecture = [' '] * self.gs.code_length

        # assign_callbacks
        self.assign_callbacks()

    def setup_screen(self,screen):
        self.screen = screen
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        
        self.screen_dimensions = self.screen.getmaxyx()
        
        # this is so we have enough room for the max number of conjectures
        self.game_botton = self.gs.max_conjectures
        
        # the means the game is in the middle of the screen
        self.game_left = int(self.screen_dimensions[1] / 2) - self.gs.code_length
        
        self.mainloop()
    
    def assign_callbacks(self):
        self.callback = {'a':self.move_cursor_left,
                         'd':self.move_cursor_right,
                         'w':self.cycle_selection_up,
                         's':self.cycle_selection_down,
                         ' ':self.enter_selection,
                         'e':self.submit_conjecture,
                         'h':self.toggle_show_answer}
    
    def mainloop(self):
        input_key = -1
        while input_key != 'q':
            self.screen.clear()
            self.draw_cursor()
            self.draw_current_conjecture()
            self.draw_historical_conjectures() 
            self.draw_secret()            
            input_key = self.screen.getkey()
            self.handle_keypress(input_key)
            self.screen.refresh()
        curses.endwin()
    
    def invalid_key(self):
        pass
    
    def move_cursor_left(self): 
        self.cursor_position -= 1
        if self.cursor_position < 0:
            self.cursor_position = self.gs.code_length-1
           
    def move_cursor_right(self):
        self.cursor_position += 1
        if self.cursor_position > self.gs.code_length-1:
            self.cursor_position = 0
    
    def handle_keypress(self,input_key):
        self.callback.get(input_key,self.invalid_key)()
        
    def cycle_selection_up(self):
        self.selection += 1
        if self.selection > len(self.gs.code_values)-1:
            self.selection = 0
            
    def cycle_selection_down(self):
        self.selection -= 1
        if self.selection < 0:
            self.selection = len(self.gs.code_values)-1
        
    def enter_selection(self):
        self.current_conjecture[self.cursor_position] = self.gs.code_values[self.selection]
        
    def submit_conjecture(self):
        self.gs.make_conjecture(self.current_conjecture)
        self.current_conjecture = [' '] * self.gs.code_length
        
    def toggle_show_answer(self):
            self.show_answer = not self.show_answer
            
    def draw_cursor(self):
        # This is the position of the small triangle cursor
        self.screen.addstr(self.game_botton, self.game_left + self.cursor_position*2, '\u25B2')
        
        # This is the position of the overscores
        self.screen.addstr(self.game_botton-1, self.game_left, ' '.join(['\u203E'] * CODE_LENGTH)) 
        
    def draw_current_conjecture(self):
        for i,_ in enumerate(self.current_conjecture): # this is where the current conjecture gets placed
            if i == self.cursor_position:
                self.screen.addstr(self.game_botton-2, self.game_left+i*2, self.gs.code_values[self.selection])
            else:
                self.screen.addstr(self.game_botton-2, self.game_left+i*2, self.current_conjecture[i])
    
    def draw_historical_conjectures(self):
        for i,conj in enumerate(self.gs.conjectures): # These are the historical conjectures
            self.screen.addstr(self.game_botton-5-i,
                          self.game_left-4,
                          f'{i:02}| {str_code(conj)}\t[{str_code(self.gs.clues[i])}]'
                          )

    def draw_secret(self):
        if self.show_answer:
            self.screen.addstr(self.game_botton+1, self.game_left, str_code(self.gs.secret))
        else:
            self.screen.addstr(self.game_botton+1, self.game_left, str_hidden(self.gs.secret))

if __name__ == '__main__':
    gs = GameScreen()
    wrapper(gs.setup_screen)