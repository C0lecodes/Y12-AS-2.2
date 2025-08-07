import console

HORIZONTAL_BAR_CHAR = "─"
VERTICAL_BAR_CHAR = "│"
PLUS_BAR_CHAR = "┼"
CORNER_BAR_CHARS = "┌┐└┘"
T_BAR_CHARS = "├┤┬┴"

COLOUR_GREEN_BOARDERS = (0, 100, 0)
COLOUR_GREEN_BG = (0, 15, 0)
COLOUR_BLACK = (0, 0, 0)
COLOUR_GREEN = 	(102, 255, 102)
COLOUR_DARK_GREEN = (0, 128, 0)
COLOUR_WHITE = (192, 192, 192)
COLOUR_GRAY = (96, 96, 96)
COLOUR_RED = (255, 0, 0)

LOGO =(
    r"    ███     ███    █▄   ▄█               ▄█    █▄     ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████ ",
    r"▀█████████▄ ███    ███ ███              ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ",
    r"   ▀███▀▀██ ███    ███ ███▌             ███    ███   ███    ███ ███   ███   ███   ███    █▀  ",
    r"    ███   ▀ ███    ███ ███▌            ▄███▄▄▄▄███▄▄ ███    ███ ███   ███   ███  ▄███▄▄▄     ",
    r"    ███     ███    ███ ███▌           ▀▀███▀▀▀▀███▀  ███    ███ ███   ███   ███ ▀▀███▀▀▀     ",
    r"    ███     ███    ███ ███              ███    ███   ███    ███ ███   ███   ███   ███    █▄  ",
    r"    ███     ███    ███ ███              ███    ███   ███    ███ ███   ███   ███   ███    ███ ",
    r"   ▄████▀   ████████▀  █▀               ███    █▀     ▀██████▀   ▀█   ███   █▀    ██████████ ",
    r"                                                                                              "
) 

LOGO_WIDTH = len(LOGO[0])
LOGO_HEIGHT =  len(LOGO)


def render_ui():
    for x in range(console.width):
        console.set(x, 0, HORIZONTAL_BAR_CHAR)
        console.set(x, -1, HORIZONTAL_BAR_CHAR)

    for y in range(console.height):
        console.set(0, y, VERTICAL_BAR_CHAR)
        console.set(-1, y, VERTICAL_BAR_CHAR)

    console.set(0,0,CORNER_BAR_CHARS[0])
    console.set(0,-1,CORNER_BAR_CHARS[2])
    console.set(-1,0,CORNER_BAR_CHARS[1])
    console.set(-1,-1,CORNER_BAR_CHARS[3])

    logo_x = 2
    logo_y = 3
    for x in range(LOGO_WIDTH):
        for y in range(LOGO_HEIGHT):
            console.set(x + logo_x, y + logo_y, LOGO[y][x])
    
    for y in range(console.height):
        console.set(-15, 1 + y, VERTICAL_BAR_CHAR)
    console.set(-15,0, T_BAR_CHARS[2])
    console.set(-15,-1,T_BAR_CHARS[3])

    console.write(-13, 1, "Commands")

console.setup(render_ui)
console.display()