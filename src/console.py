# https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/introduction/
# https://www.asciitable.com/
# https://en.wikipedia.org/wiki/ANSI_escape_code
# These are links to reading material of escape codes. My Idea for this came from a previous Y12's project.

import shutil

ESCAPE_CHAR = chr(27) # Char for escape
CLEAR_COLOUR = "[0m" # Resets colour changes

# Buffers
buffer = []
bg_buffer = []
fg_buffer = []

# Screen dimensions
width = 0
height = 0

# Misilanous vars 
user_input = None
is_running = True
render = None

def run():
    while is_running:
        display()

def clear():
    """Clears the screen"""
    print_escape_sequence("c")
    print_escape_sequence(CLEAR_COLOUR)

def setup(render_input: callable):
    global render
    render = render_input

def print_escape_sequence(sequence: str):
    """Prints ASCII sequences"""
    print(f"{ESCAPE_CHAR}{sequence}", end="")

def set_text_colour(current_col, colour, fg_col=True):
    """Sets the text colour"""
    if current_col == colour:
        return current_col
    if colour is None:
        print_escape_sequence(f"[{39 if fg_col else 49}m")
    else:
        r, g, b = colour
        print_escape_sequence(f"[{38 if fg_col else 48};2;{r};{g};{b}m")
    return colour

def get_size() -> tuple[int, int]:
    """Return terminal size"""
    try:
        size = shutil.get_terminal_size()
        return (size.columns, size.lines - 1) # leaves at the bottom of the screen
    except OSError:
        return (80, 24) # returns the default size

def create_buffer():
    """Creates the buffers"""
    global fg_buffer, bg_buffer, buffer, height, width
    width, height = get_size() # get current terminal size

    buffer = [[" " for _ in range(height)] for _ in range(width)] # creates an empty buffer/resets the buffer
    bg_buffer = [[None for _ in range(height)] for _ in range(width)] # creates an empty bg buffer/resets the bg buffer
    fg_buffer = [[None for _ in range(height)] for _ in range(width)] # creates an empty fg buffer/resets the fg buffer

def set(x: int,
        y: int,
        char: str,
        fg_col: tuple[int, int, int] | None = None,
        bg_col: tuple[int, int, int] | None = None
        ):
    """"Set a position in the buffers"""
    if x >= width or y >= height or x < -width or y < -height: # return if out of bounds
        return
    if len(char) > 1:
        char = char[0] # if the function gets more than 1 char we use the first char

    buffer[x][y] = char # sets the cords in the buffer to the char
    bg_buffer[x][y] = bg_col # sets the cords in the bg buffer to the colour
    fg_buffer[x][y] = fg_col # sets the cords in the fg buffer to the colour

def write(x: int,
        y: int,
        text: str,
        fg_col: tuple[int, int, int] | None = None,
        bg_col: tuple[int, int, int] | None = None
        ):
    """"Set a position in the buffers for strings"""
    # Makes sure the text can fit on screen
    while x < 0:
        x += width
    while y < 0:
        y += height
    # calls the set function on each char
    for i, char in enumerate(str(text)):
        set(x + i, y, char, fg_col, bg_col)

def display():
    """"Display loop"""
    global is_running, user_input

    create_buffer() # makes a fresh buffer
    render() # renders custom frames
    clear() # resets effects

    if not is_running:
        clear()
        return

    current_bg_col = None
    current_fg_col = None

    # Draws the loaded frames
    for y in range(height):
        for x in range(width):
            bg_col = bg_buffer[x][y]
            fg_col = fg_buffer[x][y]
            current_fg_col = set_text_colour(current_fg_col, fg_col, True)
            current_bg_col = set_text_colour(current_bg_col, bg_col, False)
            print(buffer[x][y], end="", flush=False)  
        print("", flush=False)
    print_escape_sequence(CLEAR_COLOUR)
    print(" > ", end="", flush=True)
    try:    
        user_input = input()
    except KeyboardInterrupt:
        is_running = False
        return