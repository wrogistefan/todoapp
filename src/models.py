from datetime import date, datetime


def parse_due_date(text: str) -> str | None:
    """Konwertuje tekst DD.MM.RRRR na ISO (YYYY-MM-DD)."""
    text = text.strip()
    if not text:
        return None
    try:
        dt = datetime.strptime(text, "%d.%m.%Y").date()
        return dt.isoformat()
    except ValueError:
        return None


def days_left_str(due_iso: str | None) -> str:
    """Zwraca opis ile dni zostało / czy termin minął."""
    if not due_iso:
        return ""
    try:
        due = date.fromisoformat(due_iso)
    except ValueError:
        return ""
    today = date.today()
    delta = (due - today).days
    if delta > 0:
        return f" ({delta} days left)"
    elif delta == 0:
        return " (due today)"
    else:
        return f" ({-delta} days overdue)"


def filter_tasks(tasks, filter_done=None, min_priority=None):
    """Zwraca listę zadań po filtrach (done, priorytet)."""
    filtered = tasks
    if filter_done is not None:
        filtered = [t for t in filtered if t["done"] is filter_done]
    if min_priority is not None:
        filtered = [t for t in filtered if t.get("priority", 2) >= min_priority]
    return filtered


def add_task(tasks, title: str, priority: int = 2, due_date: str | None = None):
    """Dodaje nowe zadanie do listy."""
    if not title.strip():
        return tasks
    tasks.append({
        "title": title.strip(),
        "done": False,
        "priority": priority if priority in (1, 2, 3) else 2,
        "due_date": due_date,
    })
    return tasks


def toggle_task(tasks, index: int):
    """Zmienia status zadania (done/undone)."""
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
    return tasks


def change_priority(tasks, index: int, new_priority: int):
    """Zmienia priorytet zadania."""
    if 0 <= index < len(tasks) and new_priority in (1, 2, 3):
        tasks[index]["priority"] = new_priority
    return tasks


def set_due_date(tasks, index: int, due_date: str | None):
    """Ustawia lub czyści termin zadania."""
    if 0 <= index < len(tasks):
        tasks[index]["due_date"] = due_date
    return tasks


def sort_tasks(tasks, by="priority", reverse=True):
    """Sortuje listę zadań według wybranego kryterium."""
    if by == "priority":
        return sorted(tasks, key=lambda t: t.get("priority", 2), reverse=reverse)
    elif by == "due_date":
        return sorted(tasks, key=lambda t: (t.get("due_date") or ""), reverse=reverse)
    elif by == "title":
        return sorted(tasks, key=lambda t: t.get("title", "").lower(), reverse=reverse)
    else:
        return tasks
