import ui
import console
from commands import commands, Command
import movie_database as db

class MoviePage(ui.Page):
    """Home page class"""
    def __init__(self, movie_id):
        """Name of the page"""
        super().__init__("Movie")
        self.movie_id = movie_id
        self.movie = db.get(movie_id)

    @staticmethod
    def setup():
        """Appends starting command"""
        commands.append(Command("View", MoviePage.command))

    @staticmethod
    def command(movie_id):
        """The command its self"""
        ui.current_page = MoviePage(movie_id)

    def render(self):
        """Renders the home pages ui"""

        if self.movie is None:
            self.error_message = f"A movie with an ID of '{self.movie_id}' doesn't exist"
            return
        # creating list of felids
        fields = [["ID", str(self.movie.id)]]

        if self.movie.genre is not None:
            fields.append(["Genre", str(self.movie.genre)])

        if self.movie.rating is not None:
            fields.append(["Rating", str(self.movie.rating)])
        
        if self.movie.watch_time is not None:
            fields.append(["Watch time", str(self.movie.watch_time)])

        if self.movie.year is not None:
            fields.append(["Year", str(self.movie.year)])

        # sets the x and y values
        y = 3
        x = 2
        # Gets the name
        name = self.movie.name
        # Writes the info to console
        console.write(x, y, name, ui.COLOUR_GREEN)

        y += 1

        for field in fields:
            prefix = f"{field[0]}: "
            console.write(x, y, prefix, ui.COLOUR_BLUE)
            console.write(x + len(prefix), y, field[1])
            y += 1