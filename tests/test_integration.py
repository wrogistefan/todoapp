import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from models import add_task, change_priority, set_due_date, toggle_task
from storage import load_tasks, save_tasks

TEST_FILE = Path("test_tasks.json")


def test_full_task_cycle(monkeypatch):
    # Podmieniamy plik na testowy
    monkeypatch.setattr("storage.DATA_FILE", TEST_FILE)

    tasks = []

    # 1. Dodajemy zadanie z polskimi znakami
    tasks = add_task(tasks, "Przygotować świąteczną kolację", priority=2)
    assert tasks[0]["title"] == "Przygotować świąteczną kolację"
    assert tasks[0]["priority"] == 2
    assert tasks[0]["done"] is False

    # 2. Toggle (zmiana statusu)
    tasks = toggle_task(tasks, 0)
    assert tasks[0]["done"] is True

    # 3. Zmiana priorytetu
    tasks = change_priority(tasks, 0, 3)
    assert tasks[0]["priority"] == 3

    # 4. Ustawienie daty
    tasks = set_due_date(tasks, 0, "2025-12-31")
    assert tasks[0]["due_date"] == "2025-12-31"

    # 5. Zapis do pliku
    save_tasks(tasks)

    # 6. Odczyt z pliku
    loaded = load_tasks()
    assert loaded == tasks

    # 7. Sprawdzenie polskich znaków w pliku
    content = TEST_FILE.read_text(encoding="utf-8")
    assert "świąteczną" in content
    assert "kolację" in content

    # Cleanup
    TEST_FILE.unlink()
