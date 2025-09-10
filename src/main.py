import console
import ui
import movie_database as db

if __name__ == "__main__":
    db.setup() # setup data base
    ui.create_pages() # create the pages
    console.setup(ui.render_current_page) # set up the current render 
    console.run() # start the loop
