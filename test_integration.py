import pytest
from pathlib import Path
from storage import save_tasks, load_tasks
from tasks import add_task, toggle_task, change_priority, set_due_date

TEST_FILE = Path("test_tasks.json")

def test_full_task_cycle(monkeypatch):
    # Podmieniamy plik na testowy
    monkeypatch.setattr("storage.DATA_FILE", TEST_FILE)

    tasks = []

    # 1. Dodajemy zadanie z polskimi znakami
    inputs = iter(["Przygotować świąteczną kolację", "2", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = add_task(tasks)
    assert tasks[0]["title"] == "Przygotować świąteczną kolację"
    assert tasks[0]["priority"] == 2
    assert tasks[0]["done"] is False

    # 2. Toggle (zmiana statusu)
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = toggle_task(tasks)
    assert tasks[0]["done"] is True

    # 3. Zmiana priorytetu
    inputs = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = change_priority(tasks)
    assert tasks[0]["priority"] == 3

    # 4. Ustawienie daty
    inputs = iter(["1", "31.12.2025"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = set_due_date(tasks)
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

    # Sprzątanie po teście
    TEST_FILE.unlink()
