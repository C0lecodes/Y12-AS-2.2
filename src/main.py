import console
import ui
import movie_database as db

if __name__ == "__main__":
    db.setup()
    ui.create_pages()
    console.setup(ui.render_current_page)
    console.run()