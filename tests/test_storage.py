import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from models import (
    add_task,
    change_priority,
    days_left_str,
    parse_due_date,
    set_due_date,
    toggle_task,
)
from storage import load_tasks, save_tasks

TEST_FILE = Path("test_tasks.json")


@pytest.fixture
def sample_tasks():
    return [
        {
            "title": "Zrobić zakupy w Biedronce",
            "done": False,
            "priority": 2,
            "due_date": None,
        },
        {
            "title": "Przygotować prezentację o Mickiewiczu",
            "done": True,
            "priority": 3,
            "due_date": None,
        },
        {
            "title": "Kupić śmietanę i chleb",
            "done": False,
            "priority": 1,
            "due_date": None,
        },
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


def test_parse_due_date_invalid():
    result = parse_due_date("31-12-2025")
    assert result is None


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
    # Removed - show_tasks function was removed in refactoring
    pass


def test_add_task():
    tasks = []
    tasks = add_task(tasks, "Nowe zadanie", priority=3)
    assert tasks[0]["title"] == "Nowe zadanie"
    assert tasks[0]["priority"] == 3
    assert tasks[0]["done"] is False


def test_toggle_task(sample_tasks):
    tasks = toggle_task(sample_tasks, 0)
    assert tasks[0]["done"] is True


def test_change_priority(sample_tasks):
    tasks = change_priority(sample_tasks, 0, 3)
    assert tasks[0]["priority"] == 3


def test_set_due_date(sample_tasks):
    tasks = set_due_date(sample_tasks, 0, "2025-12-31")
    assert tasks[0]["due_date"] == "2025-12-31"


def test_set_due_date(sample_tasks):
    tasks = set_due_date(sample_tasks, 0, "2025-12-31")
    assert tasks[0]["due_date"] == "2025-12-31"
