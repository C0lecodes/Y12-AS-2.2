
class Movie:
    """An object that details a movie."""

    def __init__(self, 
        id: int,
        name: str,
        year: int | None = None,
        rating: str | None = None,
        watch_time: int | None = None,
        genre: str | None = None
        ):
        """Create a movie with the given parameters."""
        self.id = id
        self.name = name
        self.year = year
        self.rating = rating
        self.watch_time = watch_time
        self.genre = genre
    
    def __str__(self):
        """Turn the movie into a string"""
        output = f"[{self.id}] {self.name}"

        if self.year is not None:
            output += f" ({self.year})"
        if self.rating is not None:
            output += f" {self.rating}"
        if self.watch_time is not None:
            output += f" {self.watch_time}"
        return output

