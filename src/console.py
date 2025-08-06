# https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/introduction/
# https://www.asciitable.com/
# https://en.wikipedia.org/wiki/ANSI_escape_code
# These are links to reading material of escape codes. My Idea for this came from a previous Y12's project.

import shutil

ESCAPE_CHAR = chr(27) # Char for escape

buffer = []

width = 0
height = 0

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
        char = char[0]

    buffer[x][y] = char

def write(x: int,
        y: int,
        text: str,
        ):
    """"Set a position in the buffers for strings"""

    while x < 0:
        x += width
    while y < 0:
        y += height

    for i, char in enumerate(str(text)):
        set(x + i, y, char)

def display():

    create_buffer()

    write(0, 0, "TEST")

    for y in range(height):
        for x in range(width):
            print(buffer[x][y], end="", flush=False)
    print("", flush=False)

display()
