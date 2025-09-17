import sqlite3
from movie import Movie

# constants
MOVIE_TABLE = "MOVIES"
GENRES_TABLE = "GENRES"
RATINGS_TABLE = "RATINGS"

# list containing all valid rating/genres
movie_ratings = [
    "G",
    "PG",
    "M",
    "R",
    "R13",
    "R16",
    "R18"
    ]
genres = [
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Horror",
    "Thriller",
    "Mystery",
    "Romance",
    "Science Fiction (Sci-Fi)",
    "Fantasy",
    "Animation",
    "Documentary",
    "Musical",
    "Crime",
    "Family"
    ]

database: sqlite3.Connection = None # define the connection 

def setup():
    """Set up the database."""
    global database
    # create a connection
    database = sqlite3.connect("Database.db")
    # set up the data base
    setup_database()

def setup_database():
    """Creates the data base."""
    global genres, movie_ratings
    # finds out if the database exists 
    response = database.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{MOVIE_TABLE}';")
    # if the database exists return
    if len(response.fetchall()) > 0:
        return
    # --- table creation prompts ---
    database.execute(f"""
    CREATE TABLE {GENRES_TABLE} (
        Genre_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Genre TEXT NOT NULL
    );
    """)

    database.execute(f"""
    CREATE TABLE {RATINGS_TABLE} (
        Rating_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Rating TEXT NOT NULL
    );
    """)

    database.execute(f"""
    CREATE TABLE {MOVIE_TABLE} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK(length(Name) > 0 AND length(Name) <= 100),
        Year INTEGER CHECK(Year > 1900 AND Year < 2100),
        Rating_ID INTEGER,
        Watch_time INTEGER CHECK(Watch_time > 0 AND Watch_time <= 600),
        Genre_ID INTEGER,
        Star_rating INTEGER CHECK(Star_rating > 0 AND Star_rating <= 10),
        FOREIGN KEY (Genre_ID) REFERENCES {GENRES_TABLE}(Genre_ID),
        FOREIGN KEY (Rating_ID) REFERENCES {RATINGS_TABLE}(Rating_ID)
    );
    """)
    # --- end ---

    # inserts the data for the linked tables
    for genre in genres:
        insert_link_tables(genre)

    for rating in movie_ratings:
        insert_link_tables(rating, False)
    # default movies
    movies = [
    Movie(1, "Ghostbusters", 2016, "PG", 116, "Comedy", 6.9),
    Movie(2, "The Legend of Tarzan", 2016, "PG", 109, "Action", 6.2),
    Movie(3, "Jason Bourne", 2016, "PG", 123, "Action", 6.6),
    Movie(4, "The Nice Guys", 2016, "R", 116, "Crime", 7.4),
    Movie(5, "The Secret Life of Pets", 2016, "G", 91, "Animation", 6.5),
    Movie(6, "Star Trek Beyond", 2016, "PG", 120, "Action", 6.7),
    Movie(7, "Batman v Superman", 2016, "PG", 151, "Action", 6.4),
    Movie(8, "Finding Dory", 2016, "G", 103, "Animation", 7.3),
    Movie(9, "Zootopia", 2016, "G", 108, "Animation", 8.0),
    Movie(10, "The BFG", 2016, "PG", 90, "Fantasy", 6.4),
    Movie(11, "A Monster Calls", 2016, "PG", 108, "Fantasy", 7.5),
    Movie(12, "Independence Day: Resurgence", 2016, "PG", 120, "Action", 5.2),
    Movie(13, "The Green Room", 2016, "R", 94, "Crime", 7.0),
    Movie(14, "Doctor Strange", 2016, "PG", 130, "Fantasy", 7.5),
    Movie(15, "The Jungle Book", 2016, "PG", 105, "Fantasy", 7.4),
    Movie(16, "Alice Through the Looking Glass", 2016, "PG", 118, "Fantasy", 6.2),
    Movie(17, "Imperium", 2016, "R", 109, "Crime", 6.5),
    Movie(18, "The Infiltrator", 2016, "R", 127, "Crime", 7.0),
    Movie(19, "Mad Max: Fury Road", 2015, "R", 120, "Action", 8.1),
    Movie(20, "Spectre", 2015, "PG", 145, "Action", 6.8),
    Movie(21, "Jurassic World", 2015, "PG", 100, "Action", 7.0),
    Movie(22, "The Intern", 2015, "PG", 121, "Comedy", 7.1),
    Movie(23, "Ted 2", 2015, "R", 121, "Comedy", 6.3),
    Movie(24, "Trainwreck", 2015, "R", 122, "Comedy", 6.2),
    Movie(25, "Inside Out", 2015, "PG", 94, "Animation", 8.1),
    Movie(26, "The Good Dinosaur", 2015, "G", 101, "Animation", 6.7),
    Movie(27, "Divergent", 2014, "PG", 121, "Action", 6.6),
    Movie(28, "The Max Runner", 2014, "PG", 115, "Action", 6.8),
    Movie(29, "Birdman", 2014, "R", 119, "Comedy", 7.7),
    Movie(30, "Guardians of the Galaxy", 2014, "PG", 121, "Fantasy", 8.0),
    Movie(31, "The Lego Movie", 2014, "PG", 100, "Animation", 7.7),
    Movie(32, "Big Hero 6", 2014, "PG", 108, "Animation", 7.8),
    Movie(33, "The Drop", 2014, "R", 106, "Crime", 6.8),
    Movie(34, "The Shawshank Redemption", 1994, "R", 142, "Drama", 9.3)
    ]
    # inserts the movies
    for movie in movies:
        insert(movie)


def insert_link_tables(string, genres_table=True):
    """Inserts the options into link tables."""
    query = f" INSERT INTO {GENRES_TABLE if genres_table else RATINGS_TABLE} ({"Genre" if genres_table else "Rating"}) VALUES (?)"
    database.execute(query,(string,))
    database.commit()

def insert(movie: Movie) -> int:
    """Defines a movies insert."""
    query = f" INSERT INTO {MOVIE_TABLE} (Name, Year, Rating_ID, Watch_time, Genre_ID, Star_rating) VALUES (?,?,?,?,?,?)"
    # creates a tuple of parameters
    parameters = (
        movie.name,
        movie.year,
        match_rating(movie.rating),
        movie.watch_time,
        match_genre(movie.genre),
        movie.star_rating
    )
    # inserts the tuple
    cursor = database.cursor()
    cursor.execute(query, parameters)
    database.commit()

    return cursor.lastrowid

def get_all_links(genres=True) -> list:
    """Returns the valid link data."""
    # gets a list of the valid genre and ratings
    response = database.execute(f"SELECT {"Genre_ID" if genres else "Rating_ID"}, {"Genre" if genres else "Rating"} FROM {GENRES_TABLE if genres else RATINGS_TABLE}")
    return response.fetchall()

def match_genre(movie_genre: str) -> int | None:
    """Matches genre to number."""
    for genre in get_all_links():
        if genre[1] == movie_genre:
            return genre[0]
    return None

def match_rating(movie_rating: str) -> int | None:
    """Matches rating to number."""
    for rating in get_all_links(False):
        if rating[1] == movie_rating:
            return rating[0]
    return None

def movies() -> list[Movie]:
    """Returns all movies."""
    query = f"""
        SELECT m.ID, m.Name, m.Year, r.Rating, m.Watch_time, g.Genre, m.Star_rating
        FROM {MOVIE_TABLE} m
        LEFT JOIN {RATINGS_TABLE} r ON m.Rating_ID = r.Rating_ID
        LEFT JOIN {GENRES_TABLE} g ON m.Genre_ID = g.Genre_ID;
    """
    response = database.execute(query)
    return [Movie(*row) for row in response.fetchall()] # returns as a list of the movie class

def get(id: int) -> Movie:
    """Returns one movie."""
    query = f"""
        SELECT m.ID, m.Name, m.Year, r.Rating, m.Watch_time, g.Genre, m.Star_rating
        FROM {MOVIE_TABLE} m
        LEFT JOIN {RATINGS_TABLE} r ON m.Rating_ID = r.Rating_ID
        LEFT JOIN {GENRES_TABLE} g ON m.Genre_ID = g.Genre_ID
        WHERE m.ID = ?;
    """
    response = database.execute(query, (id,))
    row = response.fetchone()
    return Movie(*row) if row else None # returns a movie

def highest_rated() -> list[int]:
    """Returns top five movies."""
    query = f"""
        SELECT Star_rating, ID
        FROM {MOVIE_TABLE}
        WHERE Star_rating IS NOT NULL;
        """

    response = database.execute(query).fetchall()

    top_five = sorted(response, reverse= True)[:5] # sorts the top 5

    return [id[1] for id in top_five] # returns the ids

def delete(id: int):
    """Deletes a movie."""
    database.execute(f"DELETE FROM {MOVIE_TABLE} WHERE ID = ?;", (id,))
    database.commit()

def edit(movie: Movie) -> int:
    """Defines a movies insert."""
    query = f"""
    UPDATE {MOVIE_TABLE}
    SET Name = ?,
        Year = ?,
        Rating_ID = ?,
        Watch_time = ?,
        Genre_ID = ?,
        Star_rating = ?
    WHERE ID = ?
        """
    # creates a tuple of parameters
    parameters = (
        movie.name,
        movie.year,
        match_rating(movie.rating),
        movie.watch_time,
        match_genre(movie.genre),
        movie.star_rating,
        movie.id
    )
    # inserts the tuple
    cursor = database.cursor()
    cursor.execute(query, parameters)
    database.commit()

    return cursor.lastrowid