import console

# boarder characters
HORIZONTAL_BAR_CHAR = "─"
VERTICAL_BAR_CHAR = "│"
PLUS_BAR_CHAR = "┼"
CORNER_BAR_CHARS = "┌┐└┘"
T_BAR_CHARS = "├┤┬┴"

# colours that can be used
COLOUR_BLACK = (15, 15, 15)
COLOUR_WHITE = (243, 244, 246)
COLOUR_GRAY = (107, 114, 128)
COLOUR_RED = (239, 68, 68)
COLOUR_YELLOW = (255, 245, 100)
COLOUR_GREEN = (34, 197, 94)
COLOUR_BLUE = (59, 130, 246)

# Logo that is displayed on the home page
LOGO = (
    r" _____ ______   ________  ___      ___ ___  _______                                   ",
    r"|\   _ \  _   \|\   __  \|\  \    /  /|\  \|\  ___ \                                  ",
    r"\ \  \\\__\ \  \ \  \|\  \ \  \  /  / | \  \ \   __/|                                 ",
    r" \ \  \\|__| \  \ \  \\\  \ \  \/  / / \ \  \ \  \_|/__                               ",
    r"  \ \  \    \ \  \ \  \\\  \ \    / /   \ \  \ \  \_|\ \                              ",
    r"   \ \__\    \ \__\ \_______\ \__/ /     \ \__\ \_______\                             ",
    r"    \|__|     \|__|\|_______|\|__|/       \|__|\|_______|                             ",
    r"                                                                                      ",
    r"                                                                                      ",
    r"                                                                                      ",
    r" ________  ________  _________  ________  ________  ________  ________  _______       ",
    r"|\   ___ \|\   __  \|\___   ___\\   __  \|\   __  \|\   __  \|\   ____\|\  ___ \      ",
    r"\ \  \_|\ \ \  \|\  \|___ \  \_\ \  \|\  \ \  \|\ /\ \  \|\  \ \  \___|\ \   __/|     ",
    r" \ \  \ \\ \ \   __  \   \ \  \ \ \   __  \ \   __  \ \   __  \ \_____  \ \  \_|/__   ",
    r"  \ \  \_\\ \ \  \ \  \   \ \  \ \ \  \ \  \ \  \|\  \ \  \ \  \|____|\  \ \  \_|\ \  ",
    r"   \ \_______\ \__\ \__\   \ \__\ \ \__\ \__\ \_______\ \__\ \__\____\_\  \ \_______\ ",
    r"    \|_______|\|__|\|__|    \|__|  \|__|\|__|\|_______|\|__|\|__|\_________\|_______| ",
    r"                                                                \|_________|          ",
    r"                                                                                      ",
    r"                                                                                      "
)
# Logo dimensions
LOGO_WIDTH = len(LOGO[0])
LOGO_HEIGHT =  len(LOGO)

class Page:
    """Basic page description"""
    def __init__(self, name: str):
        """Mother variables"""
        self.name = name
        self.renderMessage = None
        self.commands = []
        self.GlobalCommandsAvailable = True
    def render(self):
        """Render function"""
        self.error_message = "No page available!!!"

current_page = None

def create_pages():
    """Creates all pages"""
    import pages.home_page

    global current_page
    current_page = pages.home_page.HomePage()

def render_current_page():
    """Renders the current page"""

    min_width = 105
    min_height = 35

    if console.width < min_width or console.height < min_height:
        size_hint = f" Console is {console.width}x {console.height} instead of {min_width}x{min_height}"
        console.write(0, 0, f"Error: Console too small to render page {size_hint}", COLOUR_RED)
        return
    
    current_page.render()
    render_ui()


def render_ui():
    """Renders the common ui for all pages"""
    # --Renders the boarders---
    for x in range(console.width):
        console.set(x, 0, HORIZONTAL_BAR_CHAR, COLOUR_WHITE)
        console.set(x, -1, HORIZONTAL_BAR_CHAR, COLOUR_WHITE)

    for y in range(console.height):
        console.set(0, y, VERTICAL_BAR_CHAR, COLOUR_WHITE)
        console.set(-1, y, VERTICAL_BAR_CHAR, COLOUR_WHITE)

    console.set(0,0,CORNER_BAR_CHARS[0], COLOUR_WHITE)
    console.set(0,-1,CORNER_BAR_CHARS[2], COLOUR_WHITE)
    console.set(-1,0,CORNER_BAR_CHARS[1], COLOUR_WHITE)
    console.set(-1,-1,CORNER_BAR_CHARS[3], COLOUR_WHITE)
    # -- End --
    # renders page name
    console.write(2, 1, current_page.name, COLOUR_YELLOW)