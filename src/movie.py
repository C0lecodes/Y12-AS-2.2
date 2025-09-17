import movie_database as db

class Movie:
    """An object that details a movie."""
    def __init__(self, 
        id: int,
        name: str,
        year: int | None = None,
        rating: str | None = None,
        watch_time: int | None = None,
        genre: str | None = None,
        star_rating: int | None = None
        ):
        """Create a movie with the given parameters."""
        self.id = id
        self.name = name
        self.year = year
        self.rating = rating
        self.watch_time = watch_time
        self.genre = genre
        self.star_rating = star_rating
        # check if the movie is in the top 5
        self.highest_rated = db.highest_rated()
        self.recommended = self.id in self.highest_rated

    def __str__(self):
        """Turn the movie into a string"""
        output = f"[{self.id}] {self.name}"
        if self.year is not None:
            output += f" ({self.year})"
        if self.recommended:
            output += " ★"
        return output


class MovieField:
    """Emulate an enum for movie fields with match support."""

    _instances = [] # holds all instances of the field types

    def __init__(self, name: str):
        """Variables that create a movie instance."""
        self.name = name
        MovieField._instances.append(self)

    def __repr__(self):
        """Return the object of an instance."""
        return f"<MovieField.{self.name}>"

    @staticmethod
    def all_fields():
        """Return all defined MovieFields."""
        return MovieField._instances

    def database_name(self) -> str:
        """Return the database field name."""
        match self:
            case MovieField.NAME: return "Name"
            case MovieField.YEAR: return "Year"
            case MovieField.RATING: return "Rating"
            case MovieField.WATCH_TIME: return "WatchTime"
            case MovieField.GENRE: return "Genre"
            case MovieField.STAR_RATING: return "StarRating"
            case _: return "???"

    def get_insert_prompt(self) -> str:
        """Return the insert prompt for the user."""
        match self:
            # matches the current movie field to a case--this gives the user a prompt.
            case MovieField.NAME:
                message = "What is the name of the movie?"
                message += "\nRequired"
                message += "\nMax 100 characters"
                return message
            case MovieField.YEAR:
                message = "What is the release year of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1900 and 2100"
                return message
            case MovieField.RATING:
                message = "What is the audience rating of the movie?\n"
                message += "Available ratings:\n"
                ratings = db.movie_ratings
                for rating in ratings:
                    message += f"{rating} "
                message += "\nPress Enter to skip"
                return message
            case MovieField.WATCH_TIME:
                message = "What is the runtime of the movie in minutes?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1 and 600 minutes"
                return message
            case MovieField.GENRE:
                message = "What is the genre of the movie?\n"
                message += "Available Genres:\n"
                genres = db.genres
                # ---Makes nice lines for the genres---
                line_length = len(genres) // 4 + (1 if len(genres) % 4 else 0)
                for i in range(line_length):
                    row = ""
                    for j in range(4):
                        idx = i + j * line_length
                        if idx < len(genres):
                            row += f"{genres[idx]:20}"
                    message += row + "\n"
                # ---End---
                message += "\nPress Enter to skip"
                return message
            case MovieField.STAR_RATING:
                message = "What is the star rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 0 and 10"
                return message
            case _:
                return "???"

    def verify_field(self, user_input: str, enforce_name: bool = False) -> tuple[bool, any, str | None]:
        """Check if the given user input is valid for this movie field."""
        user_input = user_input.strip() # get the user input
        if user_input == "":
            user_input = None # if the user enters a blank string sets to None

        match self:
            case MovieField.NAME:
                if user_input is None:
                    # Makes sure that the user inputs a name
                    if enforce_name:
                        return (False, user_input, "No name was given")
                    return (True, None, None)
                # Makes sure the name is the correct length
                if len(user_input) > 100:
                    return (False, user_input, "Name is too long")
                return (True, user_input, None)

            case MovieField.YEAR:
                # Alowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    # makes sure the input in between the correct values
                    value = int(user_input)
                    if 1900 > value > 2100:
                        return (False, user_input, "Please enter a year between the correct values")
                    return (True, value, None)
                except:
                    # fall back if the input is not a number or something happens
                    return (False, user_input, "Please enter a number")
            case MovieField.RATING:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)
                # matches rating to make sure the user has input a valid one
                for rating in db.movie_ratings:
                    if rating.lower() == user_input.lower():
                        return (True, user_input, None)
                return (False, user_input, "Enter a valid rating")
            case MovieField.WATCH_TIME:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    # makes sure the user has input a correct value for watch time
                    value = int(user_input)
                    if value < 1 or value > 600:
                        return (False, user_input, "Please enter a year between the correct values")
                    return (True, value, None)
                except:
                    # fall back if input is'ent a number or something goes wrong
                    return (False, user_input, "Please enter a number")
            case MovieField.GENRE:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)
                # matches genres from the database to make sure the user inputs a correct one
                for genre in db.genres:
                    if genre.lower() == user_input.lower():
                        return (True, user_input, None)
                return (False, user_input, "Enter a genre rating")
            case MovieField.STAR_RATING:
                # Alowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    # makes sure the star rating is between the correct values
                    value = float(user_input) # alow float input IE: 5.5
                    if value < 0 or value > 10:
                        return (False, user_input, "Please rating between 0 and 10")
                    return (True, value, None)
                except:
                    # fall back if the input is'ent a number or something goes wrong
                    return (False, user_input, "Please enter a number")
            case _:
                return "???"

    def get_edit_prompt(self, current_value) -> str:
        """Return the insert prompt for the user."""
        match self:
            # matches the current movie field to a case--this gives the user a prompt.
            case MovieField.NAME:
                message = "What is the name of the movie?\n"
                message += f"Current name: {str(current_value)}"
                message += "\nPress Enter to skip"
                message += "\nMax 100 characters"
                return message
            case MovieField.YEAR:
                message = "What is the release year of the movie?\n"
                message += f"Current year: {str(current_value)}"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1900 and 2100"
                return message
            case MovieField.RATING:
                message = "What is the audience rating of the movie?\n"
                message += f"Current rating: {str(current_value)}"
                message += "\nAvailable ratings:\n"
                ratings = db.movie_ratings
                for rating in ratings:
                    message += f"{rating} "
                message += "\nPress Enter to skip"
                return message
            case MovieField.WATCH_TIME:
                message = "What is the runtime of the movie in minutes?\n"
                message += f"Current watch time: {str(current_value)}"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1 and 600 minutes"
                return message
            case MovieField.GENRE:
                message = "What is the genre of the movie?\n"
                message += f"Current genre: {str(current_value)}"
                message += "\nAvailable Genres:\n"
                genres = db.genres
                # ---Makes nice lines for the genres---
                line_length = len(genres) // 4 + (1 if len(genres) % 4 else 0)
                for i in range(line_length):
                    row = ""
                    for j in range(4):
                        idx = i + j * line_length
                        if idx < len(genres):
                            row += f"{genres[idx]:20}"
                    message += row + "\n"
                # ---End---
                message += "\nPress Enter to skip"
                return message
            case MovieField.STAR_RATING:
                message = "What is the star rating of the movie?\n"
                message += f"Current star rating: {str(current_value)}"
                message += "\nPress Enter to skip"
                message += "\nMust be between 0 and 10"
                return message
            case _:
                return "???"


# Define the "enum" members--this allows our class to match the inputs to cases
MovieField.NAME = MovieField("NAME")
MovieField.YEAR = MovieField("YEAR")
MovieField.RATING = MovieField("RATING")
MovieField.WATCH_TIME = MovieField("WATCH_TIME")
MovieField.GENRE = MovieField("GENRE")
MovieField.STAR_RATING = MovieField("STAR_RATING")
