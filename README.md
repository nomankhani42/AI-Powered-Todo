# 📝 Todo CLI - Command-Line Todo Application

A lightweight, fully-documented command-line todo application with in-memory storage, comprehensive type hints, and colorful output. Built with Python 3.13+ and designed for simplicity, testability, and user experience.

## ✨ Features

- **➕ Add Tasks**: Create new tasks with auto-incremented IDs
  - Descriptions up to 200 characters
  - Automatic creation timestamp
  - Input validation with helpful error messages

- **📋 View All Tasks**: Display all tasks in a formatted table
  - Shows task ID, description, and completion status
  - Supports empty task list gracefully
  - Colorful Unicode table formatting

- **✅ Mark Complete**: Mark tasks as done
  - Idempotent operation (can mark complete multiple times)
  - Clear feedback on already-completed tasks
  - Preserves completion status through updates

- **✏️ Update Tasks**: Change task descriptions
  - Preserve completion status during updates
  - Same validation as task creation
  - Clear error messages for invalid updates

- **🗑️ Delete Tasks**: Remove tasks by ID
  - Permanent deletion with confirmation
  - Error handling for non-existent tasks
  - Sequential ID management preserved

## 📦 Requirements

- Python 3.13+
- UV package manager
- Development dependencies: pytest, ruff, mypy (installed via `uv sync`)

## 🚀 Installation

```bash
# Navigate to project directory
cd "E:\Panaversity Hackathon\Todo App"

# Install dependencies with UV
uv sync

# Verify installation
python -c "import sys; print(f'Python {sys.version}')"
```

## 🎯 Usage

### Starting the Application

```bash
# Method 1: Using UV
uv run todo

# Method 2: Using Python module
python -m todo_cli

# Method 3: Direct Python
python -c "from todo_cli.main import main; main()"
```

### Interactive Session

Once started, you'll see the welcome message:
```
Welcome to todo-cli! Type 'help' for available commands.
>
```

### Available Commands

All commands are case-insensitive and support colorful output.

| Command | Description | Example | Output |
|---------|-------------|---------|--------|
| `add <desc>` | Add a new task | `add Buy groceries` | ✓ Task added successfully (ID: 1) |
| `list` | Show all tasks | `list` | Formatted table with ID, Description, Status |
| `complete <id>` | Mark task done | `complete 1` | ✓ Task 1 marked as complete |
| `update <id> <desc>` | Update task description | `update 1 Buy organic groceries` | ✓ Task 1 updated successfully |
| `delete <id>` | Remove a task | `delete 1` | ✓ Task 1 deleted successfully |
| `help` | Show all commands | `help` | Displays command list with syntax |
| `exit` | Quit application | `exit` | Goodbye! |

### Example Interactive Session

```
Welcome to todo-cli! Type 'help' for available commands.
> add Buy groceries
✓ Task added successfully (ID: 1)
> add Clean the house
✓ Task added successfully (ID: 2)
> add Pay bills
✓ Task added successfully (ID: 3)
> list
┌──────┬──────────────────┬────────────┐
│  ID  │   Description    │   Status   │
├──────┼──────────────────┼────────────┤
│  1   │ Buy groceries    │  [ ] Todo  │
│  2   │ Clean the house  │  [ ] Todo  │
│  3   │ Pay bills        │  [ ] Todo  │
└──────┴──────────────────┴────────────┘
> complete 1
✓ Task 1 marked as complete
> update 2 Clean house and yard
✓ Task 2 updated successfully
> list
┌──────┬──────────────────────────┬────────────┐
│  ID  │      Description         │   Status   │
├──────┼──────────────────────────┼────────────┤
│  1   │ Buy groceries            │  [✓] Done  │
│  2   │ Clean house and yard     │  [ ] Todo  │
│  3   │ Pay bills                │  [ ] Todo  │
└──────┴──────────────────────────┴────────────┘
> delete 3
✓ Task 3 deleted successfully
> help
Available commands:
  add <description>       - Add a new task
  delete <id>            - Delete a task by ID
  update <id> <desc>     - Update a task's description
  list                   - View all tasks
  complete <id>          - Mark a task as complete
  help                   - Show this help message
  exit                   - Exit the application
> exit
Goodbye!
```

## 🧪 Development & Testing

### Running Tests

```bash
# Run all tests with verbose output
uv run pytest tests/ -v

# Run specific test module
uv run pytest tests/test_models.py -v

# Run with coverage report
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test function
uv run pytest tests/test_models.py::test_task_creation -v
```

### Code Quality

```bash
# Run linting (code style checks)
uv run ruff check src tests

# Fix common linting issues automatically
uv run ruff check --fix src tests

# Run type checking (static type validation)
uv run mypy src

# Run all checks together
uv run pytest tests/ -v && uv run ruff check src tests && uv run mypy src
```

## 🏗️ Project Structure

```
.
├── src/
│   └── todo_cli/                    # Main application package
│       ├── __init__.py              # Package initialization & metadata
│       ├── __main__.py              # Module entry point (python -m todo_cli)
│       ├── main.py                  # Application bootstrap
│       ├── models.py                # Task dataclass with validation
│       ├── store.py                 # In-memory task storage (CRUD)
│       ├── commands.py              # Business logic layer (command handlers)
│       └── cli.py                   # REPL interface & output formatting
├── tests/
│   ├── __init__.py                  # Test package initialization
│   ├── test_models.py               # Task model validation tests
│   ├── test_store.py                # Storage layer CRUD tests
│   ├── test_commands.py             # Command handler tests
│   └── test_cli.py                  # CLI integration tests
├── pyproject.toml                   # Project configuration, dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── specs/                           # Specification & documentation
    └── 001-todo-cli/
        ├── spec.md                  # Feature specification
        ├── plan.md                  # Implementation plan
        ├── data-model.md            # Data model documentation
        └── tasks.md                 # Task breakdown
```

## 📚 Documentation

### Code Documentation

All functions, classes, and modules include comprehensive docstrings in Google style format:

- **Module docstrings**: Explain purpose, provide usage examples
- **Class docstrings**: Describe what the class does, list attributes
- **Function docstrings**: Document parameters, return values, and exceptions
- **Type hints**: All parameters and return values are fully typed

### Examples of Docstring Style

```python
def add(self, description: str) -> CommandResult:
    """
    Add a new task to the store.

    Creates a task with the provided description, auto-incrementing ID,
    and current timestamp. Validates input before creation.

    Args:
        description: Task description (required, ≤200 chars, non-empty)

    Returns:
        CommandResult with success status, message, and created Task data

    Raises:
        ValueError: If description is empty or exceeds 200 characters

    Example:
        >>> result = store.add("Buy groceries")
        >>> result.success
        True
        >>> result.data.id
        1
    """
```

## 🎨 Output Features

- **Color-coded messages**:
  - ✓ Green for success
  - ✗ Red for errors
  - ℹ Blue for informational messages

- **Formatted tables**: Unicode box-drawing for neat task display

- **Clear prompts**: `>` prompt indicates readiness for input

- **Helpful error messages**: Guide users on correct command syntax

## ⚙️ Configuration

### pyproject.toml Settings

```toml
# Code quality settings
[tool.ruff]
line-length = 100
target-version = "py313"

# Type checking settings
[tool.mypy]
python_version = "3.13"
disallow_untyped_defs = true     # All functions must be typed
check_untyped_defs = true         # Check calls to untyped functions

# Test configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src"
```

## 🧠 Architecture

The application follows a layered architecture for clean separation of concerns:

### Layer Structure

1. **Models Layer** (`models.py`)
   - Pure data structures with validation
   - Task dataclass with `__post_init__` validation
   - No dependencies on other layers

2. **Storage Layer** (`store.py`)
   - In-memory CRUD operations
   - TaskStore class with dict-based storage
   - Sequential ID generation
   - Depends on: Models

3. **Commands Layer** (`commands.py`)
   - Business logic for each operation
   - TodoCommands class wrapping the store
   - Validation and error handling
   - Returns structured CommandResult objects
   - Depends on: Models, Storage

4. **CLI Layer** (`cli.py`)
   - REPL loop and user interaction
   - Input parsing and command routing
   - Output formatting and display
   - TodoCLI class coordinates all layers
   - Depends on: Commands

## 📝 Implementation Notes

### Key Design Decisions

1. **In-Memory Storage**: No persistence layer, data cleared on exit
2. **Simple Input Parsing**: No external CLI frameworks, pure string parsing
3. **Comprehensive Validation**: All inputs validated at CLI boundary
4. **Immutable IDs**: Task IDs sequential and never reused in a session
5. **Type Safety**: 100% type hints across all public functions

### Performance Characteristics

- **Add Task**: O(1) - Direct dictionary insertion
- **Get Task**: O(1) - Dictionary lookup by ID
- **List All**: O(n) - Iterate all tasks
- **Delete Task**: O(1) - Dictionary deletion
- **Update Task**: O(1) - In-place modification
- **Mark Complete**: O(1) - Direct flag update

Where n = number of tasks (designed for up to 10,000 tasks)

## 🐛 Error Handling

All user errors are caught and reported with helpful messages:

```
Empty description → "Error: Description cannot be empty"
Task not found → "Error: Task with ID 999 not found"
Invalid ID format → "Error: Please provide a valid task ID (number)"
Over 200 chars → "Error: Description must not exceed 200 characters"
Unknown command → "Unknown command. Type 'help' for available commands."
```

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

Contributions are welcome! Please ensure:
- All tests pass: `uv run pytest tests/ -v`
- No linting errors: `uv run ruff check src tests`
- No type errors: `uv run mypy src`
- Docstrings added for all public functions
- New features include test coverage

## 📞 Support

For issues or questions, check the available commands with `help` inside the application.
