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


def add_task(tasks, title: str, priority: int = 1, due_date: str | None = None):
    """Dodaje nowe zadanie do listy.
    Walidacja: tytuł nie może być pusty, priorytet musi być 1–3.
    """
    if not title.strip():
        raise ValueError("Task title cannot be empty")
    if priority not in (1, 2, 3):
        raise ValueError("Priority must be 1, 2 or 3")

    tasks.append({
        "title": title.strip(),
        "done": False,
        "priority": priority,
        "due_date": due_date,
    })
    return tasks


def toggle_task(tasks, index: int):
    """Zmienia status zadania (done/undone)."""
    if index < 0 or index >= len(tasks):
        raise IndexError("Invalid task index")
    tasks[index]["done"] = not tasks[index]["done"]
    return tasks


def change_priority(tasks, index: int, new_priority: int):
    """Zmienia priorytet zadania."""
    if index < 0 or index >= len(tasks):
        raise IndexError("Invalid task index")
    if new_priority not in (1, 2, 3):
        raise ValueError("Priority must be 1, 2 or 3")
    tasks[index]["priority"] = new_priority
    return tasks


def set_due_date(tasks, index: int, due_date: str | None):
    """Ustawia lub czyści termin zadania.
    Walidacja: index poprawny, data w formacie YYYY-MM-DD.
    """
    if index < 0 or index >= len(tasks):
        raise IndexError("Invalid task index")
    if due_date is not None:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    # <- tutaj brakowało faktycznego przypisania
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
