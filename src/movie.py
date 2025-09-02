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
                message = "What is the audience rating of the movie?"
                message += "\nPress Enter to skip"
                message += db.movie_ratings
                return message
            case MovieField.WATCH_TIME:
                message = "What is the runtime of the movie in minutes?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 1 and 600 minutes"
                return message
            case MovieField.GENRE:
                message = "What are the genres of the movie? (comma-separated)"
                message += "\nPress Enter to skip"
                message += db.genres
                return message
            case MovieField.STAR_RATING:
                message = "What is the star rating of the movie?"
                message += "\nPress Enter to skip"
                message += "\nMust be between 0 and 5"
                return message
            case _:
                return "???"


# Define the "enum" members
MovieField.NAME = MovieField("NAME")
MovieField.YEAR = MovieField("YEAR")
MovieField.RATING = MovieField("RATING")
MovieField.WATCH_TIME = MovieField("WATCH_TIME")
MovieField.GENRE = MovieField("GENRE")
MovieField.STAR_RATING = MovieField("STAR_RATING")
