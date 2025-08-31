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
        self.recommended = None

        self.highest_rated = db.highest_rated()

        for id in self.highest_rated:
            if self.id == id:
                self.recommended = True
    
    def __str__(self):
        """Turn the movie into a string"""
        output = f"[{self.id}] {self.name}"

        if self.year is not None:
            output += f" ({self.year})"
        if self.recommended is not None:
            output += f" {"★"}"
        return output


