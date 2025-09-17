import ui
import console
from commands import commands, Command, get_current_commands
import movie_database as db
import movie_link as link

class DeleteMovie(ui.Page):
    """Delete movie page class"""
    def __init__(self, movie_id: int):
        """Name of the page"""
        super().__init__("Delete Movie")
        self.movie_id = movie_id
        self.movie = db.get(movie_id)
        self.commands.append(Command("Yes", DeleteMovie.command_yes))
        self.commands.append(Command("No", DeleteMovie.command_no))
        self.GlobalCommandsAvailable = False
        self.movie_deleted = None

    @staticmethod
    def setup():
        """Appends starting command"""
        commands.append(Command("Delete", DeleteMovie.command))

    @staticmethod
    def command(movie_id):
        """The command its self"""
        # stops the deletion if no id exists
        if db.get(movie_id) is None:
            ui.current_page.error_message = f"A movie with an ID of '{movie_id}' doesn't exist"
            return
        # sets current page
        ui.current_page = DeleteMovie(movie_id)

    @staticmethod
    def command_yes():
        """Yes commands depiction"""
        # deletes the movie
        db.delete(ui.current_page.movie_id)
        ui.current_page.movie_deleted = "Deleted"
        # lets the user leave the page
        ui.current_page.GlobalCommandsAvailable = True
        ui.current_page.commands.clear()

    @staticmethod
    def command_no():
        """No commands depiction"""
        ui.current_page.movie_deleted = "Not deleted"
        # lets the user leave the page
        ui.current_page.GlobalCommandsAvailable = True
        ui.current_page.commands.clear()

    def render(self):
        """Renders the delete movie ui"""

        # creating list of felids
        fields = [["ID", str(self.movie.id)]]
        # ---makes sure the property exists---
        if self.movie.genre is not None:
            fields.append(["Genre", str(self.movie.genre)])

        if self.movie.rating is not None:
            fields.append(["Rating", str(self.movie.rating)])
        
        if self.movie.watch_time is not None:
            fields.append(["Watch time", str(self.movie.watch_time)])

        if self.movie.year is not None:
            fields.append(["Year", str(self.movie.year)])
        
        if self.movie.star_rating is not None:
            fields.append(["Star rating", str(self.movie.star_rating) + "/10"])
        
        fields.append(["Movie deletion status",str(self.movie_deleted)])

        if self.movie_deleted is None:
            fields.append(["Delete movie: "," Yes/No"])
        # --- end ---

        # sets the x and y values
        height = 2 + len(fields) + 2
        # Get the max width
        width = len(self.movie.name)
        # finds the max width if its larger than names width
        for field in fields:
            field_width = len(f"{field[0]}: {field[1]}")
            if field_width > width:
                width = field_width

        # add white spaces
        for field in fields:
            field_width = len(f"{field[0]}: {field[1]}")
            field[1] = (width - field_width) * " " + field[1]
        # adds a buffer to the width
        width += 4
        # defines cmd_x as a temp value
        cmd_x = 0
        # gets all available commands
        available_cmds = get_current_commands()
        if len(available_cmds) > 0:
            # Find the widest command and make sure that there is a buffer around it
            widest_cmd = max([len(str(cmd)) for cmd in available_cmds + ["Commands"]])
            widest_cmd += 2
            # Make sure that the commands are drawn of the left side of the screen
            cmd_x = -widest_cmd

        # Calculate the x and y position
        x = round((console.width - width + cmd_x) / 2)
        y = round((console.height - height) / 2)

        # draw boarder
        for boarder_hoz in range(width):
            console.set(x + boarder_hoz, y, ui.MOVIE_HORIZONTAL_BAR_CHAR)
            console.set(x + boarder_hoz, y + height -1, ui.MOVIE_HORIZONTAL_BAR_CHAR)

        for boarder_vet in range(height):
            console.set(x, y + boarder_vet, ui.MOVIE_VERTICAL_BAR_CHAR)
            console.set(x + width - 1, y + boarder_vet, ui.MOVIE_VERTICAL_BAR_CHAR)

        console.set(x, y, ui.MOVIE_CORNER_BAR_CHARS[0])
        console.set(x + width -1, y, ui.MOVIE_CORNER_BAR_CHARS[1])
        console.set(x, y + height -1, ui.MOVIE_CORNER_BAR_CHARS[2])
        console.set(x + width -1, y + height -1, ui.MOVIE_CORNER_BAR_CHARS[3])
        # --- end ---
        # updates the x and y pos for writing
        x += 2
        y += 1
        # Gets the name
        name = self.movie.name
        name_off_set = round((width - len(name)) / 2) 
        # Writes the info to console
        console.write(x - 2 + name_off_set, y, name, ui.COLOUR_GREEN)
        # updates y pos
        y += 2
        # draws all the fields
        for field in fields:
            prefix = f"{field[0]}: "
            console.write(x, y, prefix, ui.COLOUR_BLUE)
            console.write(x + len(prefix), y, field[1])
            y += 1
