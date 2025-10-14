import ui as ui
import console as console
from commands import commands, Command
import movie_database as db
from movie import Movie, MovieField

class FilterMoviesPage(ui.Page):
    """Home page class."""
    PADDING = 3
    def __init__(self):
        """Name of the page."""
        super().__init__("Search Page")
        self.index = 0
        self.commands.append(Command("w", FilterMoviesPage.scroll_up))
        self.commands.append(Command("s", FilterMoviesPage.scroll_down))
        self.commands.append(Command("Filter", FilterMoviesPage.filter))
        self.commands.append(Command("Help", FilterMoviesPage.help))
        self.commands.append(Command("Return", FilterMoviesPage.back))
        self.filtered_movies = db.movies()
        self.help_active = False
        self.GlobalCommandsAvailable = False

    @staticmethod
    def setup():
        """Appends starting command."""
        commands.append(Command("Search", FilterMoviesPage.command))

    @staticmethod
    def command():
        """The command its self."""
        ui.current_page = FilterMoviesPage()
    @staticmethod
    def scroll_up():
        """The command its self."""
        ui.current_page.index -= FilterMoviesPage.get_number_of_rows()
    @staticmethod
    def scroll_down():
        """The command its self."""
        ui.current_page.index += FilterMoviesPage.get_number_of_rows()
    @staticmethod
    def get_number_of_rows():
        return console.height - FilterMoviesPage.PADDING * 2
    @staticmethod
    def check_categories(category):
        """Return database equivalent."""
        # category database values
        categories = {
            "name": MovieField.NAME,
            "year": MovieField.YEAR,
            "rating": MovieField.RATING,
            "watch_time": MovieField.WATCH_TIME,
            "genre": MovieField.GENRE,
            "star_rating": MovieField.STAR_RATING
        }

        # Normalize input to lowercase
        category_key = category.lower()

        # Validate input and return error if invalid
        if category_key not in categories:
            ui.current_page.error_message = "Please enter correct filter settings. Type help for all commands"
            return None
        # get the category
        category_col = categories[category_key]

        return category_col
        
    @staticmethod
    def filter(category, value):
        """Filters movies based on category, order, and direction."""
        # verify category
        category_col = FilterMoviesPage.check_categories(category)
        # make sure it's not none
        if category_col is None:
            return
        # set current page
        ui.current_page.filtered_movies = db.filter(category_col, value)
    @staticmethod
    def help():
        """Displays a compact help menu for the Filter Movies page."""
        ui.current_page.help_active = True
        # --instructions--
        console.clear()
        console.write(2, 2, "=== Filter Movies Help ===", ui.COLOUR_YELLOW)

        console.write(2, 4, "Navigation: w=up, s=down, Return=main menu", ui.COLOUR_BLUE)
        console.write(2, 6, "Filter movies: Filter <category> <value>", ui.COLOUR_BLUE)
        console.write(4, 7, "Example: Filter Name Star")

        console.write(2, 9, "Categories: Name, Year, Rating, Watch_time, Genre, Star_rating", ui.COLOUR_BLUE)
        console.write(2, 11, "Tips: Filtering is case-insensitive and supports partial matches.", ui.COLOUR_BLUE)

        console.write(2, 13, "Press Enter to return to the list...", ui.COLOUR_BLUE)
        # --end--

    @staticmethod
    def back():
        """lets the user exit."""
        ui.current_page.commands.clear()
        ui.current_page.GlobalCommandsAvailable = True

    def render(self):
        """Renders the home pages ui."""
        if self.help_active:
            self.help_active = False
            return
        # gets all movies
        movies = self.filtered_movies
        # writes the command prompts
        console.write(2, 2, "Type 'w' or 's' and press enter to scroll up or down", ui.COLOUR_BLUE)
        # gets the number of movies and number of rows
        movies_num = len(movies)
        rows_num =  FilterMoviesPage.get_number_of_rows()
        # adds no movie message
        if movies_num == 0:
            movies = ["No movie found."]
            movies_num += 1
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
        # makes sure the current idex is'ent more than the max index
        if self.index > max_index:
            self.index = max_index
        # adds a y padding so that the text and movies dont over lap
        index_y = FilterMoviesPage.PADDING + 2
        # draws the movies
        for i in range(self.index, movies_num + 1):
            if movies_num < 1 :
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


