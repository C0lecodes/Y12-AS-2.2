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
        # the current field that is bing entered
        self.current_field_index = 0
        # holds the accepted entrees
        self.movie_fields = {}
        # Used to render the final page
        self.movie_added = False
        self.movie = None
        self.movie_id = None
        # Stops us wrongly using "insert" as the initial user input
        self.first_open = True
        # Make sure the name is enforced--bug where is skips anyway
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
        """Get the input for the user for the given movie field."""
        if self.first_open or self.movie_added:
            return
        
        (is_valid, user_input, error_message) = self.current_field.verify_field(console.user_input, self.enforce_name)

        self.error_message = error_message
        if not is_valid:
            return
        
        self.movie_fields[self.current_field] = user_input

        self.current_field_index += 1

        if self.current_field_index >= len(self.MOVIE_FIELDS):
            self.on_finish_input()

    def on_finish_input(self):
        """Add the movie to the database once the user is done giving input."""
        # Add the movie
        movie = Movie(0, *self.movie_fields.values())
        self.movie_id = db.insert(movie)

        # Get the movie (with the updated ID from inserting it)
        self.getting_input = False
        self.movie_added = True
        self.movie = db.get(self.movie_id)

    def render(self):
        """Add Movie pages ui"""
        message_x = 2
        message_y = 2

        self.get_input()

        if self.first_open:
            self.first_open = False

        if self.movie_added:
            message_y += 1
            console.write(message_x, message_y, "Movie added successfully!", ui.COLOUR_BLUE)
            console.write(message_x, message_y + 1, self.movie)
            return

        # Draw the prompt for the user
        message = self.get_prompt()
        for line in message.split("\n"):
            console.write(message_x, message_y, line, ui.COLOUR_LIGHT_BLUE)
            message_y += 1