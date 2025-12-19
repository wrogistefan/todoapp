# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-12-19

### Added
- Professional project structure with `src/`, `tests/`, and `.github/workflows/`
- GitHub Actions CI/CD pipeline for automated testing (Python 3.8-3.11)
- Comprehensive test suite with 12 passing tests
- Flake8 configuration for code quality enforcement (max-line-length 100, complexity ≤ 11)
- Root-level `main.py` wrapper for easier execution
- `pyproject.toml` for modern Python packaging
- `requirements.txt` for dependency management
- Professional README with full documentation

### Changed
- Reorganized codebase: `tasks.py` → `src/models.py`
- Moved all source files to `src/` directory
- Moved all tests to `tests/` directory
- Updated imports across all modules to use new package structure
- Refactored `ConsoleTodoApp.run()` method for lower complexity

### Fixed
- Fixed all flake8 violations (41 total)
- Fixed line length issues (all lines ≤ 100 characters)
- Fixed blank line spacing (PEP 8 compliance)
- Fixed import ordering and formatting
- Fixed end-of-file whitespace issues

### Removed
- Removed `wrogistefan/` directory from main repo

## [1.0.0] - Initial Release
- Console interface for task management
- Tkinter GUI interface
- JSON persistence
- Task filtering and sorting
- Support for Polish characters
