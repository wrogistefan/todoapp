# TodoApp

[![CI](https://github.com/wrogistefan/todoapp/actions/workflows/ci.yml/badge.svg)](https://github.com/wrogistefan/todoapp/actions)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2C3.11-blue.svg)](https://www.python.org/)
[![Codecov](https://codecov.io/gh/wrogistefan/todoapp/branch/main/graph/badge.svg)](https://codecov.io/gh/wrogistefan/todoapp)

A lightweight, dual-interface task management application built with Python. Organize your tasks efficiently with both a console CLI and a modern Tkinter graphical interface. Data persists via JSON, ensuring your tasks are always saved.

## Features

- **Dual Interface**: Choose between command-line and graphical user interface
- **Task Management**: Create, read, update, and delete tasks effortlessly
- **Persistent Storage**: All tasks saved to JSON for reliable data persistence
- **Clean Architecture**: Separation of concerns with modular code structure
- **Comprehensive Testing**: Unit and integration tests ensure reliability
- **Cross-Platform**: Runs on Windows, macOS, and Linux

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/wrogistefan/todoapp.git
cd todoapp

# Install dependencies
pip install -r requirements.txt

# Optional: Install development dependencies for testing
pip install -e ".[dev]"
```

### Usage

#### Console Interface

```bash
python src/console_app.py
```

#### GUI Interface

```bash
python src/gui.py
```

#### Main Application

```bash
python src/main.py
```

You can also run the application directly from the project root using the provided wrapper:

```bash
# From project root
python main.py
```


## Project Structure

```
todoapp/
├── src/                          # Main application code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   ├── console_app.py           # Command-line interface
│   ├── gui.py                   # Tkinter graphical interface
│   ├── models.py                # Data models and business logic
│   └── storage.py               # JSON persistence layer
├── tests/                        # Test suite
│   ├── test_integration.py      # Integration tests
│   ├── test_storage.py          # Storage layer tests
│   └── tkinter_test.py          # GUI tests
├── .github/
│   └── workflows/
│       └── ci.yml               # Continuous integration pipeline
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata and configuration
├── tasks.json                  # Task data storage
└── README.md                   # This file
```

## Development

Code style: PEP8 enforced with flake8

Formatting: black

CI/CD: GitHub Actions + Codecov integration

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_storage.py
```

### Project Configuration

See [pyproject.toml](pyproject.toml) for build system configuration and [requirements.txt](requirements.txt) for dependencies.

## Continuous Integration

This project uses GitHub Actions for automated testing. The CI pipeline runs tests across Python 3.10 and 3.11. See [.github/workflows/ci.yml](.github/workflows/ci.yml) for details.

## Architecture

### Storage Layer
- JSON-based persistence in `tasks.json`
- Implemented in `src/storage.py`
- Handles read/write operations with error handling

### Business Logic
- Core task models defined in `src/models.py`
- Clean separation from UI and storage layers

### User Interfaces
- **Console**: `src/console_app.py` - Text-based interactive interface
- **GUI**: `src/gui.py` - Tkinter-based graphical interface
- Both interfaces share the same underlying business logic

## License

This project is open source and available under the MIT License.

## Author

**Łukasz Perek**  
Tech Support Specialist | Python Developer | AI Projects

- **Email**: lukasz.perek@gmail.com
- **LinkedIn**: [linkedin.com/in/lukaszperek](https://www.linkedin.com/in/lukaszperek)
- **GitHub**: [github.com/wrogistefan](https://github.com/wrogistefan)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project.
