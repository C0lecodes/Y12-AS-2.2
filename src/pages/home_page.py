import ui
import console

class HomePage(ui.Page):
    def __init__(self):
        super().__init__("Home Page")

    def render(self):
        logo_x = 2
        logo_y = 3
        for x in range(ui.LOGO_WIDTH):
            for y in range(ui.LOGO_HEIGHT):
                console.set(x + logo_x, y + logo_y, ui.LOGO[y][x], ui.COLOUR_BLUE)