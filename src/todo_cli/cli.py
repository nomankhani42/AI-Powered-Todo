"""Command-line interface for todo-cli application."""
from todo_cli.commands import CommandResult, TodoCommands
from todo_cli.models import Task
from todo_cli.store import TaskStore


class TodoCLI:
    """Interactive command-line interface for the todo application.

    Manages user input, command routing, and output display. Provides a REPL
    (Read-Eval-Print Loop) for users to interact with their tasks.
    """

    HELP_TEXT = """Todo CLI - Available Commands
-----------------------------
add <description>        Add a new task
list                     View all tasks
complete <id>            Mark a task as done
update <id> <description> Update task description
delete <id>              Delete a task
help                     Show this help message
exit                     Exit the application
"""

    def __init__(self) -> None:
        """Initialize TodoCLI with TaskStore and TodoCommands."""
        self._store = TaskStore()
        self._commands = TodoCommands(self._store)
        self.running = True

    def run(self) -> None:
        """Start the interactive REPL loop.

        Displays welcome message and continuously reads user input until
        the user exits the application.
        """
        print("Todo CLI - Type 'help' for available commands")
        print("-" * 45)

        while self.running:
            try:
                user_input = input("> ").strip()
                if user_input:
                    self._process_input(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.running = False
            except EOFError:
                print("\nGoodbye!")
                self.running = False

    def _process_input(self, user_input: str) -> None:
        """Parse and route user input to appropriate command handler.

        Args:
            user_input: Raw user input string.
        """
        parts = user_input.split(maxsplit=1)
        if not parts:
            return

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "add":
            self._handle_add(args)
        elif command == "list":
            self._handle_list(args)
        elif command == "complete":
            self._handle_complete(args)
        elif command == "update":
            self._handle_update(args)
        elif command == "delete":
            self._handle_delete(args)
        elif command == "help":
            self._handle_help()
        elif command == "exit":
            self._handle_exit()
        else:
            print("Unknown command. Type 'help' for available commands.")

    def _handle_add(self, args: str) -> None:
        """Handle add command.

        Args:
            args: Description of the task to add.
        """
        if not args.strip():
            msg = "Error: Description cannot be empty"
            result = CommandResult(success=False, message=msg)
        else:
            result = self._commands.add(args.strip())
        self._display_result(result)

    def _handle_list(self, args: str) -> None:
        """Handle list command.

        Args:
            args: Not used for list command.
        """
        result = self._commands.list_all()
        if result.data:
            self._display_tasks(result.data)
        else:
            print(result.message)

    def _handle_complete(self, args: str) -> None:
        """Handle complete command.

        Args:
            args: Task ID to mark complete.
        """
        task_id = self._parse_id(args)
        if task_id is None:
            return
        result = self._commands.complete(task_id)
        self._display_result(result)

    def _handle_update(self, args: str) -> None:
        """Handle update command.

        Args:
            args: Task ID and new description.
        """
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            print("Error: Missing required argument. Usage: update <id> <description>")
            return

        task_id = self._parse_id(parts[0])
        if task_id is None:
            return

        description = parts[1].strip()
        result = self._commands.update(task_id, description)
        self._display_result(result)

    def _handle_delete(self, args: str) -> None:
        """Handle delete command.

        Args:
            args: Task ID to delete.
        """
        task_id = self._parse_id(args)
        if task_id is None:
            return
        result = self._commands.delete(task_id)
        self._display_result(result)

    def _handle_help(self) -> None:
        """Handle help command."""
        print(self.HELP_TEXT)

    def _handle_exit(self) -> None:
        """Handle exit command."""
        print("Goodbye!")
        self.running = False

    def _parse_id(self, arg: str) -> int | None:
        """Parse and validate a task ID from string input.

        Args:
            arg: String to parse as task ID.

        Returns:
            Integer ID if valid, None otherwise (prints error).
        """
        arg = arg.strip()
        if not arg:
            print("Error: Missing required argument. Usage: <command> <id>")
            return None

        try:
            return int(arg)
        except ValueError:
            print("Error: Please provide a valid task ID (number)")
            return None

    def _display_result(self, result: CommandResult) -> None:
        """Display command result to user.

        Args:
            result: CommandResult to display.
        """
        if result.success:
            print(f"* {result.message}")
        else:
            print(f"! {result.message}")

    def _display_tasks(self, tasks: list[Task]) -> None:
        """Display tasks in formatted table.

        Args:
            tasks: List of Task objects to display.
        """
        if not tasks:
            print("No tasks found.")
            return

        # Print header
        print("\nID | Description      | Status")
        print("-" * 40)

        # Print tasks
        for task in tasks:
            # Truncate description to 50 chars if needed
            desc = task.description
            if len(desc) > 50:
                desc = desc[:47] + "..."

            # Format status (ASCII-compatible for Windows)
            status = "[X] Done" if task.completed else "[ ] Todo"

            print(f"{task.id:<2} | {desc:<20} | {status}")

        print()
