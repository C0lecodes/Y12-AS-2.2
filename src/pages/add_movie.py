import ui
import console
from commands import commands, Command
import movie_database as db
from movie import Movie, MovieField

class AddMovie(ui.Page):
    """Add movie page class"""
    MOVIE_FIELDS = [
        MovieField.NAME,
        MovieField.YEAR,
        MovieField.RATING,
        MovieField.WATCH_TIME,
        MovieField.GENRE,
        MovieField.STAR_RATING
    ]

    def __init__(self):
        """Create a page."""
        super().__init__("Insert")
        self.getting_input = True
        # The index in MOVIE_FIELDS we are currently searching for
        self.current_field_index = 0
        # Dictionary of all of the movie fields
        self.movie_fields = {}
        # Used to render the final page
        self.movie_added = False
        self.movie = None
        # Stops us wrongly using "insert" as the initial user input
        self.first_open = True
        # Make sure the name is enforced
        self.enforce_name = True

    @staticmethod
    def setup():
        """Appends starting command"""
        commands.append(Command("Add", AddMovie.command))

    @staticmethod
    def command():
        """The command its self"""
        ui.current_page = AddMovie()
    @property
    def current_field(self) -> MovieField:
        """Get the class for current field the user is inputting."""
        return AddMovie.MOVIE_FIELDS[self.current_field_index]

    def get_prompt(self):
        """Get the prompt for the user for the given movie field."""
        return self.current_field.get_insert_prompt()
    
    def get_input(self) -> str:
        input = console.user_input.strip()

    def render(self):
        """Add Movie pages ui"""
        message_x = 2
        message_y = 2

        self.get_input()

        # Draw the prompt for the user
        message = self.get_prompt()
        for line in message.split("\n"):
            console.write(message_x, message_y, line, ui.COLOUR_BLUE)
            message_y += 1