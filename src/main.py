import console
import ui

if __name__ == "__main__":
    ui.create_pages()
    console.setup(ui.render_current_page)
    console.run()