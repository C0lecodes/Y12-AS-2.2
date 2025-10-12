import inspect
import console as console
import ui as ui

class Command:
    """Commands layout"""
    def __init__(self, name: str, action: callable) -> None:
        """Basic command parameters"""
        self._name = name
        self._action = action

        self._argsc = len(inspect.signature(action).parameters)

    def __str__(self):
        """Output when the class it printed"""
        output = self.name

        # Finds the names of the arguments
        parameters = inspect.signature(self.action).parameters.keys()

        # Adds the names to the output string
        for parameter in parameters:
            output += f" [{parameter}]"

        return output

    @property
    def name(self):
        """Returns the name"""
        return self._name
    @property
    def action(self):
        """Returns the action"""
        return self._action
    @property
    def argsc(self):
        """Returns the args count"""
        return self._argsc

    def invoke_cmd(self, args):
        """Run the command"""
        # Make sure that the commands have the correct amount of arguments
        if len(args) != self.argsc:
            ui.current_page.error_message = f"Wrong amount of args {len(args)} instead of {self.argsc}"
            return
        # calls the function with any vars needed
        self.action(*args)

# --- Basic command ---
def exit_program():
    """Exit program"""
    console.is_running = False
# --- End ---

# Global list of commands the base commands are entered into here at boot up
commands = [
    Command("Quit", exit_program)
]

# Find if a command is valid return the command object if it is
def find_command(name: str) -> Command | None:
    """Function used to find a command"""
    for command in get_current_commands():
        if command.name.lower() == name.lower():
            return command
    return None

# Returns a list of all currently active commands
def get_current_commands() -> list[Command]:
    """Function used to get the current commands"""
    if not ui.current_page.GlobalCommandsAvailable:
        return ui.current_page.commands
    else:
        return ui.current_page.commands + commands