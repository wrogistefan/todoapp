import pytest
from models import add_task, toggle_task, change_priority, set_due_date

def test_add_task_defaults():
    tasks = add_task([], "Test")
    assert tasks[0]["title"] == "Test"
    assert tasks[0]["priority"] == 1
    assert tasks[0]["done"] is False

def test_add_task_empty_title():
    with pytest.raises(ValueError):
        add_task([], "")

def test_toggle_task_valid():
    tasks = add_task([], "Test")
    tasks = toggle_task(tasks, 0)
    assert tasks[0]["done"] is True

def test_toggle_task_invalid_index():
    tasks = add_task([], "Test")
    with pytest.raises(IndexError):
        toggle_task(tasks, 99)

def test_change_priority_valid():
    tasks = add_task([], "Test")
    tasks = change_priority(tasks, 0, 3)
    assert tasks[0]["priority"] == 3

def test_change_priority_invalid():
    tasks = add_task([], "Test")
    with pytest.raises(ValueError):
        change_priority(tasks, 0, -1)

def test_set_due_date_valid():
    tasks = add_task([], "Test")
    tasks = set_due_date(tasks, 0, "2025-12-31")
    assert tasks[0]["due_date"] == "2025-12-31"

def test_set_due_date_invalid():
    tasks = add_task([], "Test")
    with pytest.raises(ValueError):
        set_due_date(tasks, 0, "31-12-2025")
