from pathlib import Path
import json
from typing import List, Dict, Any

DATA_FILE = Path("tasks.json")

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"DEBUG: saved {len(tasks)} tasks to {DATA_FILE}")

def load_tasks() -> List[Dict[str, Any]]:
    """
    Load tasks from DATA_FILE. Always return a list (empty list on missing/corrupt file).
    """
    if not DATA_FILE.exists():
        print(f"DEBUG: {DATA_FILE} not found, returning []")
        return []
    try:
        text = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, list):
            print("DEBUG: tasks file does not contain a list, returning []")
            return []
        print(f"DEBUG: loaded {len(data)} tasks from {DATA_FILE}")
        return data
    except Exception as e:
        print("DEBUG: failed to load tasks:", e)
        return []