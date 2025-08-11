import inspect
import console
import ui

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
            output += f"[{parameter}]"

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
        self.action(*args)

def exit_program():
    """Exit program"""
    console.is_running = False

commands = [
    Command("Quit", exit_program)
]

