# Please run the program using a python 3.13.1 interpreter
# Make sure that the console that the program is run in supports colour codes.
# C0lecodes has no rights to any movies and take no responsibility for HDtodays unauthorized access.
import console
import ui
import movie_database as db

if __name__ == "__main__":
    db.setup() # setup data base
    ui.create_pages() # create the pages
    console.setup(ui.render_current_page) # set up the current render 
    console.run() # start the loop view_all