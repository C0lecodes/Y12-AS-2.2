import ui as ui
import console as console
from commands import commands, Command
import movie_database as db

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
        # gets all movies
        movies = db.movies()
        # writes the command prompts
        console.write(2, 2, "Type 'w' or 's' and press enter to scroll up or down", ui.COLOUR_BLUE)
        console.write(2, 3, "Top 5 movies marked with ★", ui.COLOUR_BLUE)
        # gets the number of movies and number of rows
        movies_num = len(movies)
        rows_num =  MoviesPage.get_number_of_rows()
        # defines the max index
        max_index = movies_num - rows_num
        # adds a buffer
        max_index += 1
        # makes sure the value if positive or 0
        if self.index < 0:
            self.index = 0
        # makes sure the value if positive or 0
        if max_index < 0:
            max_index = 0
        # makes sure the current idex isent more than the max index
        if self.index > max_index:
            self.index = max_index
        # adds a y padding so that the text and movies dont over lap
        index_y = MoviesPage.PADDING + 2
        # draws the movies
        for i in range(self.index, movies_num + 1):
            if movies_num <=1 :
                return
            # find the index to draw
            index_drawn_in_list = i - self.index
            # if we over stepped we break
            if index_drawn_in_list >= rows_num:
                break
            # if the iteration = the number of movies its the end of the list
            if i == movies_num:
                text = "[End of List]"
            # if we over stepped we break
            elif i > movies_num:
                break
            # set text to the current movie
            else:
                text = movies[i]
            # draw the movie to the buffer
            console.write(2, index_y, text, ui.COLOUR_WHITE)
            # update index
            index_y += 1


