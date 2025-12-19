import pytest
from pathlib import Path
from storage import save_tasks, load_tasks

def test_save_and_load(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr("storage.DATA_FILE", test_file)

    tasks = [{"title": "Test", "priority": 1, "done": False}]
    save_tasks(tasks)
    loaded = load_tasks()
    assert loaded == tasks

def test_load_missing_file(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"
    monkeypatch.setattr("storage.DATA_FILE", test_file)
    tasks = load_tasks()
    assert tasks == []

def test_save_empty_list(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr("storage.DATA_FILE", test_file)
    save_tasks([])
    loaded = load_tasks()
    assert loaded == []
