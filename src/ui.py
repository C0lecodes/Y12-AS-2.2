import console
import commands

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
COLOUR_LIGHT_BLUE = (158, 203, 242)

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
        self.error_message = None
        self.commands = []
        self.GlobalCommandsAvailable = True
    def render(self):
        """Render function"""
        self.error_message = "No page available!!!"

current_page = None

def create_pages():
    """Creates all pages"""
    # import the pages
    import pages.home_page
    import pages.movies
    import pages.movie
    # setup the pages
    pages.home_page.HomePage.setup()
    pages.movies.MoviesPage.setup()
    pages.movie.MoviePage.setup()
    # set current page
    global current_page
    current_page = pages.home_page.HomePage()

def handle_inputs():
    # make sure the inputs is not None
    if console.user_input is None:
        return
    
    # Splitting the input in to separate tokens
    cmd = console.user_input.split()

    # make sure the input is longer than 0 chars
    if len(cmd) <= 0:
        current_page.error_message = "No command provided"
        return

    # Separate it into the different parts
    command_name = cmd[0].lower()
    parameters = cmd[1:]

    # makes sure the commands is a valid one returns false if its not
    cmd = commands.find_command(command_name)

    # invokes if not false
    if cmd is not None:
        cmd.invoke_cmd(parameters)
    else:
        current_page.error_message = f"'{console.user_input}' is not a vaild command"

def render_current_page():
    """Renders the current page"""

    # gets inputs and uses them correctly
    handle_inputs()

    # min width and heights for the terminal
    min_width = 105
    min_height = 35
    # --- Makes sure the terminal is the correct size
    if console.width < min_width or console.height < min_height:
        size_hint = f" Console is {console.width}x {console.height} instead of {min_width}x{min_height}"
        console.write(0, 0, f"Error: Console too small to render page {size_hint}", COLOUR_RED)
        return
    # --- end ---
    # renders the current pages content
    current_page.render()
    # renders the common ui
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

    # Write the error message if one is there
    if current_page.error_message is not None:
        console.write(2, -2, f"Error: {current_page.error_message}", COLOUR_RED)

    # Get all commands that are currently in use
    available_cmds =  commands.get_current_commands()

    # Find the widest command and make sure that there is a buffer around it
    widest_cmd = max([len(str(cmd)) for cmd in available_cmds + ["Commands"]])
    widest_cmd += 4

    # Make sure that the commands are drawn of the left side of the screen
    cmd_x = -widest_cmd
    cmd_y = 1

    # Draw the line to make the command box
    for y in range(console.height):
        console.set(cmd_x, cmd_y + y, VERTICAL_BAR_CHAR, COLOUR_WHITE)
    console.set(cmd_x, 0, T_BAR_CHARS[2], COLOUR_WHITE)
    console.set(cmd_x, -1, T_BAR_CHARS[3], COLOUR_WHITE)

    # Move to the correct position to draw the title
    cmd_x += 2

    console.write(cmd_x, cmd_y, "Commands", COLOUR_YELLOW)

    # Move to the correct position to draw the commands
    cmd_y += 2

    # Draws the commands
    for cmd in available_cmds:
        console.write(cmd_x, cmd_y, cmd, COLOUR_LIGHT_BLUE)
        cmd_y += 1