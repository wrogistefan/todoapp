# Release v1.1.0 - Project Restructuring & Quality Improvements

**Tag:** `v1.1.0` | **Date:** 2025-12-19

## Overview
Major restructuring with professional project layout, comprehensive testing, and zero code quality violations.

## What's New

### ✨ Added
- Professional project structure with `src/`, `tests/`, and `.github/workflows/`
- GitHub Actions CI/CD pipeline for automated testing (Python 3.10, 3.11)
- Comprehensive test suite with 12 passing tests
- Flake8 configuration for code quality enforcement (max-line-length 100, complexity ≤ 11)
- Root-level `main.py` wrapper for easier execution
- `pyproject.toml` for modern Python packaging
- `requirements.txt` for dependency management
- Professional README with full documentation
- MIT LICENSE file
- Status badges (CI, License, Python, Coverage)
- CHANGELOG.md tracking all releases

### 🔄 Changed
- Reorganized codebase: `tasks.py` → `src/models.py`
- Moved all source files to `src/` directory
- Moved all tests to `tests/` directory
- Updated imports across all modules to use new package structure
- Refactored `ConsoleTodoApp.run()` method for lower complexity
- Updated minimum Python requirement to 3.10+
- Removed Python 3.8 and 3.9 from CI test matrix

### 🐛 Fixed
- Fixed all 41 flake8 violations
- Fixed line length issues (all lines ≤ 100 characters)
- Fixed blank line spacing (PEP 8 compliance)
- Fixed import ordering and formatting
- Fixed end-of-file whitespace issues
- Fixed module imports in `gui.py` and `console_app.py`

### 🗑️ Removed
- Removed `wrogistefan/` directory from main repo

## Installation & Usage

### Quick Start
```bash
git clone https://github.com/wrogistefan/todoapp.git
cd todoapp
pip install -r requirements.txt
```

### Run Application
```bash
# From project root (easiest)
python main.py

# Or run specific interface
python src/main.py       # Interactive mode selector
python src/console_app.py  # Console only
python src/gui.py        # GUI only
```

### Run Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
flake8 src tests
```

## Project Structure
```
todoapp/
├── src/                    # Main application code
│   ├── main.py            # Entry point
│   ├── console_app.py     # CLI interface
│   ├── gui.py             # Tkinter GUI
│   ├── models.py          # Business logic
│   └── storage.py         # JSON persistence
├── tests/                 # Test suite (12 passing tests)
├── .github/workflows/ci.yml # CI/CD pipeline
├── pyproject.toml         # Project config
├── requirements.txt       # Dependencies
├── CHANGELOG.md          # Release notes
├── LICENSE               # MIT license
└── README.md             # Documentation
```

## Python Support
- **Minimum:** Python 3.10
- **Tested:** Python 3.10, 3.11
- **Compatibility:** Windows, macOS, Linux

## License
MIT License © 2025 Łukasz Perek

---

**Full Changelog:** See [CHANGELOG.md](../../CHANGELOG.md) for all release history.
