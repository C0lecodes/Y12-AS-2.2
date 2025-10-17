import ui
import console
from commands import commands, Command

class HomePage(ui.Page):
    """Home page class"""
    def __init__(self):
        """Name of the page"""
        super().__init__("Home Page")

    @staticmethod
    def setup():
        """Appends starting command"""
        commands.append(Command("Home", HomePage.command))

    @staticmethod
    def command():
        """The command its self"""
        ui.current_page = HomePage()

    def render(self):
        """Renders the home pages ui"""

        # logo cords
        logo_x = 2
        logo_y = 3

        # prints the Logo
        for x in range(ui.LOGO_WIDTH):
            for y in range(ui.LOGO_HEIGHT):
                console.set(x + logo_x, y + logo_y, ui.LOGO[y][x], ui.COLOUR_GREEN)
        # --- End --- 
        # name positions
        name_x = logo_x + 8
        name_y = logo_y + 1 + ui.LOGO_HEIGHT
        # owner tag
        console.write(name_x, name_y, "Made by Cole Lobban")
