import ui
import console
from commands import commands, Command
import movie_database

class MoviesPage(ui.Page):
    """Home page class"""
    PADDING = 3
    def __init__(self):
        """Name of the page"""
        super().__init__("Movies Page")
        self.index = 0
        self.commands.append(Command("w", MoviesPage.scroll_up))
        self.commands.append(Command("s", MoviesPage.scroll_down))

    @staticmethod
    def setup():
        """Appends starting command"""
        commands.append(Command("View_all", MoviesPage.command))

    @staticmethod
    def command():
        """The command its self"""
        ui.current_page = MoviesPage()
    @staticmethod
    def scroll_up():
        """The command its self"""
        ui.current_page.index -= MoviesPage.get_number_of_rows()
    @staticmethod
    def scroll_down():
        """The command its self"""
        ui.current_page.index += MoviesPage.get_number_of_rows()
    @staticmethod
    def get_number_of_rows():
        return console.height - MoviesPage.PADDING * 2

    def render(self):
        """Renders the home pages ui"""
        movie_database.setup()
        movies = movie_database.movies()

        console.write(2, 2, "Type 'w' or 's' and press enter to scroll up or down", ui.COLOUR_BLUE)

        movies_num = len(movies)
        rows_num =  MoviesPage.get_number_of_rows()

        max_index = movies_num - rows_num
        max_index += 1

        if self.index < 0:
            self.index = 0

        if max_index < 0:
            max_index = 0

        if self.index > max_index:
            self.index = max_index

        index_y = MoviesPage.PADDING + 1

        for i in range(self.index, movies_num + 1):

            if movies_num <=1 :
                return

            index_drawn_in_list = i - self.index

            if index_drawn_in_list >= rows_num:
                break

            if i == movies_num:
                text = "[End of List]"
            elif i > movies_num:
                break
            else:
                text = movies[i]

            console.write(2, index_y, text, ui.COLOUR_WHITE)
            index_y += 1


