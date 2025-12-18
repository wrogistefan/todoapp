import pytest
from pathlib import Path
from datetime import date, timedelta
from storage import save_tasks, load_tasks
from tasks import (
    parse_due_date,
    days_left_str,
    show_tasks,
    add_task,
    toggle_task,
    change_priority,
    set_due_date,
)

TEST_FILE = Path("test_tasks.json")

@pytest.fixture
def sample_tasks():
    return [
        {"title": "Zrobić zakupy w Biedronce", "done": False, "priority": 2, "due_date": None},
        {"title": "Przygotować prezentację o Mickiewiczu", "done": True, "priority": 3, "due_date": None},
        {"title": "Kupić śmietanę i chleb", "done": False, "priority": 1, "due_date": None},
    ]

# --- STORAGE TESTS ---

def test_save_and_load_polish_characters(sample_tasks, monkeypatch):
    monkeypatch.setattr("storage.DATA_FILE", TEST_FILE)
    save_tasks(sample_tasks)

    content = TEST_FILE.read_text(encoding="utf-8")
    assert "śmietanę" in content
    assert "Mickiewiczu" in content
    assert "Biedronce" in content

    loaded = load_tasks()
    assert loaded == sample_tasks

    TEST_FILE.unlink()

# --- TASKS TESTS ---

def test_parse_due_date_valid():
    assert parse_due_date("31.12.2025") == "2025-12-31"

def test_parse_due_date_invalid(capfd):
    result = parse_due_date("31-12-2025")
    out, _ = capfd.readouterr()
    assert result is None
    assert "Invalid date format" in out

def test_days_left_str_future():
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    assert "days left" in days_left_str(tomorrow)

def test_days_left_str_today():
    today = date.today().isoformat()
    assert "(due today)" in days_left_str(today)

def test_days_left_str_past():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    assert "overdue" in days_left_str(yesterday)

def test_show_tasks_prints(sample_tasks, capfd):
    show_tasks(sample_tasks)
    out, _ = capfd.readouterr()
    assert "Zrobić zakupy" in out
    assert "Przygotować prezentację" in out

def test_add_task(monkeypatch):
    tasks = []
    inputs = iter(["Nowe zadanie", "3", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = add_task(tasks)
    assert tasks[0]["title"] == "Nowe zadanie"
    assert tasks[0]["priority"] == 3
    assert tasks[0]["done"] is False

def test_toggle_task(monkeypatch, sample_tasks):
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = toggle_task(sample_tasks)
    assert tasks[0]["done"] is True

def test_change_priority(monkeypatch, sample_tasks):
    inputs = iter(["1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = change_priority(sample_tasks)
    assert tasks[0]["priority"] == 3

def test_set_due_date(monkeypatch, sample_tasks):
    inputs = iter(["1", "31.12.2025"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tasks = set_due_date(sample_tasks)
    assert tasks[0]["due_date"] == "2025-12-31"
