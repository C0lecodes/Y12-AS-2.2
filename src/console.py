# https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/introduction/
# https://www.asciitable.com/
# https://en.wikipedia.org/wiki/ANSI_escape_code
# These are links to reading material of escape codes. My Idea for this came from a previous Y12's project.

import shutil

ESCAPE_CHAR = chr(27) # Char for escape

buffer = []

width = 0
height = 0

def setup(render_input: callable):
    global render
    render = render_input

def get_size() -> tuple[int, int]:
    """Return terminal size"""
    try:
        size = shutil.get_terminal_size()
        return (size.columns, size.lines - 1) # leaves at the bottom of the screen
    except OSError:
        return (80, 24) # returns the default size

def create_buffer():
    """Creates the buffers"""
    global buffer, height, width
    width, height = get_size() # get current terminal size

    buffer = [[" " for _ in range(height)] for _ in range(width)] # creates an empty buffer/resets the buffer

def set(x: int,
        y: int,
        char: str,
        ):
    """"Set a position in the buffers"""
    if x >= width or y >= height or x < -width or y < -height: # return if out of bounds
        return
    if len(char) > 1:
        char = char[0] # if the function gets more than 1 char we use the first char

    buffer[x][y] = char # sets the cords in the buffer to the char

def write(x: int,
        y: int,
        text: str,
        ):
    """"Set a position in the buffers for strings"""
    # Makes sure the text can fit on screen
    while x < 0:
        x += width
    while y < 0:
        y += height
    # calls the set function on each char
    for i, char in enumerate(str(text)):
        set(x + i, y, char)

def display():
    """"Display loop"""

    create_buffer() # makes a fresh buffer
    render() # renders custom frames

    # Draws the loaded frames
    for y in range(height):
        for x in range(width):
            print(buffer[x][y], end="", flush=False)
    print("", flush=False)
