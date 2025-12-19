"""Entry point for TodoApp - runs from project root."""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from main import main  # noqa: E402

if __name__ == "__main__":
    main()
