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

    _instances = []

    def __init__(self, name: str):
        self.name = name
        MovieField._instances.append(self)

    def __repr__(self):
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
            user_input = None

        match self:
            case MovieField.NAME:
                if user_input is None:
                    # Makes sure that the user inputs a name
                    if enforce_name:
                        return (False, user_input, "No name was given")
                # Makes sure the name is the correct length
                if len(user_input) > 100:
                    return (False, user_input, "Name is too long")
                
                return (True, user_input, None)

            case MovieField.YEAR:
                # Alowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    value = int(user_input)
                    if value < 1900 or value > 2100:
                        return (False, user_input, "Please enter a year between the correct values")
                    return (True, value, None)
                except:
                    return (False, user_input, "Please enter a number")
            case MovieField.RATING:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)

                for rating in db.movie_ratings:
                    if rating == user_input:
                        return (True, user_input, None)
                return (False, user_input, "Enter a valid rating")
            case MovieField.WATCH_TIME:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    value = int(user_input)
                    if value < 1 or value > 600:
                        return (False, user_input, "Please enter a year between the correct values")
                    return (True, value, None)
                except:
                    return (False, user_input, "Please enter a number")
            case MovieField.GENRE:
                # Allowing the user not to input
                if user_input is None:
                    return (True, None, None)

                for rating in db.genres:
                    if rating == user_input:
                        return (True, user_input, None)
                return (False, user_input, "Enter a genre rating")
            case MovieField.STAR_RATING:
                # Alowing the user not to input
                if user_input is None:
                    return (True, None, None)
                try:
                    value = float(user_input)
                    if value < 0 or value > 10:
                        return (False, user_input, "Please rating between 0 and 10")
                    return (True, value, None)
                except:
                    return (False, user_input, "Please enter a number")
            case _:
                return "???"


# Define the "enum" members
MovieField.NAME = MovieField("NAME")
MovieField.YEAR = MovieField("YEAR")
MovieField.RATING = MovieField("RATING")
MovieField.WATCH_TIME = MovieField("WATCH_TIME")
MovieField.GENRE = MovieField("GENRE")
MovieField.STAR_RATING = MovieField("STAR_RATING")
