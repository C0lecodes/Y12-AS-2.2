import sqlite3
from movie import Movie

MOVIE_TABLE = "MOVIES"
GENRES_TABLE = "GENRES"
RATINGS_TABLE = "RATINGS"

database: sqlite3.Connection = None

def setup():
    global database
    database = sqlite3.connect(MOVIE_TABLE)
    setup_database()

def setup_database():
    response = database.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{MOVIE_TABLE}';")

    if len(response.fetchall()) > 0:
        return
    
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
        FOREIGN KEY (Genre_ID) REFERENCES {GENRES_TABLE}(Genre_ID),
        FOREIGN KEY (Rating_ID) REFERENCES {RATINGS_TABLE}(Rating_ID)
    );
    """)

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
    for genre in genres:
        insert_link_tables(genre)

    movie_ratings = [
    "G",
    "PG",
    "M",
    "R",
    "R13",
    "R16",
    "R18"
    ]
    for rating in movie_ratings:
        insert_link_tables(rating, False)
    
    movies = [
    Movie(1, "Ghostbusters", 2016, "PG", 116, "Comedy"),
    Movie(2, "The Legend of Tarzan", 2016, "PG", 109, "Action"),
    Movie(3, "Jason Bourne", 2016, "PG", 123, "Action"),
    Movie(4, "The Nice Guys", 2016, "R", 116, "Crime"),
    Movie(5, "The Secret Life of Pets", 2016, "G", 91, "Animation"),
    Movie(6, "Star Trek Beyond", 2016, "PG", 120, "Action"),
    Movie(7, "Batman v Superman", 2016, "PG", 151, "Action"),
    Movie(8, "Finding Dory", 2016, "G", 103, "Animation"),
    Movie(9, "Zootopia", 2016, "G", 108, "Animation"),
    Movie(10, "The BFG", 2016, "PG", 90, "Fantasy"),
    Movie(11, "A Monster Calls", 2016, "PG", 108, "Fantasy"),
    Movie(12, "Independence Day: Resurgence", 2016, "PG", 120, "Action"),
    Movie(13, "The Green Room", 2016, "R", 94, "Crime"),
    Movie(14, "Doctor Strange", 2016, "PG", 130, "Fantasy"),
    Movie(15, "The Jungle Book", 2016, "PG", 105, "Fantasy"),
    Movie(16, "Alice Through the Looking Glass", 2016, "PG", 118, "Fantasy"),
    Movie(17, "Imperium", 2016, "R", 109, "Crime"),
    Movie(18, "The Infiltrator", 2016, "R", 127, "Crime"),
    Movie(19, "Mad Max: Fury Road", 2015, "R", 120, "Action"),
    Movie(20, "Spectre", 2015, "PG", 145, "Action"),
    Movie(21, "Jurassic World", 2015, "PG", 100, "Action"),
    Movie(22, "The Intern", 2015, "PG", 121, "Comedy"),
    Movie(23, "Ted 2", 2015, "R", 121, "Comedy"),
    Movie(24, "Trainwreck", 2015, "R", 122, "Comedy"),
    Movie(25, "Inside Out", 2015, "PG", 94, "Animation"),
    Movie(26, "The Good Dinosaur", 2015, "G", 101, "Animation"),
    Movie(27, "Divergent", 2014, "PG", 121, "Action"),
    Movie(28, "The Max Runner", 2014, "PG", 115, "Action"),
    Movie(29, "Birdman", 2014, "R", 119, "Comedy"),
    Movie(30, "Guardians of the Galaxy", 2014, "PG", 121, "Fantasy"),
    Movie(31, "The Lego Movie", 2014, "PG", 100, "Animation"),
    Movie(32, "Big Hero 6", 2014, "PG", 108, "Animation"),
    Movie(33, "The Drop", 2014, "R", 106, "Crime")
    ]
    for movie in movies:
        insert(movie)


def insert_link_tables(string, genres_table=True):
    query = f" INSERT INTO {GENRES_TABLE if genres_table else RATINGS_TABLE} ({"Genre" if genres_table else "Rating"}) VALUES (?)"
    database.execute(query,(string,))
    database.commit()

def insert(movie: Movie) -> int:
    query = f" INSERT INTO {MOVIE_TABLE} (Name, Year, Rating_ID, Watch_time, Genre_ID) VALUES (?,?,?,?,?)"

    parameters = (
        movie.name,
        movie.year,
        match_rating(movie.rating),
        movie.watch_time,
        match_genre(movie.genre)
    )
    database.execute(query, parameters)
    database.commit()

def get_all_links(genres=True) -> list:
    response = database.execute(f"SELECT {"Genre_ID" if genres else "Rating_ID"}, {"Genre" if genres else "Rating"} FROM {GENRES_TABLE if genres else RATINGS_TABLE}")
    return response.fetchall()

def match_genre(movie_genre: str) -> int | None:
    for genre in get_all_links():
        if genre[1] == movie_genre:
            return genre[0]
    return None

def match_rating(movie_rating: str) -> int | None:
    for rating in get_all_links(False):
        if rating[1] == movie_rating:
            return rating[0]
    return None

def movies() -> list[Movie]:
    query = f"""
        SELECT m.ID, m.Name, m.Year, r.Rating, m.Watch_time, g.Genre
        FROM {MOVIE_TABLE} m
        INNER JOIN {RATINGS_TABLE} r ON m.Rating_ID = r.Rating_ID
        INNER JOIN {GENRES_TABLE} g ON m.Genre_ID = g.Genre_ID;
    """
    response = database.execute(query)

    return [Movie(*row) for row in response.fetchall()]
