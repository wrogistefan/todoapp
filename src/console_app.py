from models import (
    add_task,
    change_priority,
    days_left_str,
    filter_tasks,
    parse_due_date,
    set_due_date,
    sort_tasks,
    toggle_task,
)
from storage import load_tasks, save_tasks
import sys


class ConsoleTodoApp:
    def __init__(self):
        self.tasks = load_tasks()

    def display_tasks(self, tasks=None):
        tasks = tasks or self.tasks
        if not tasks:
            print("No tasks yet.")
            return
        print("\nYour tasks:")
        for i, task in enumerate(tasks, start=1):
            status = "✓" if task["done"] else " "
            prio_map = {1: "low", 2: "med", 3: "high"}
            prio_label = prio_map.get(task.get("priority", 2), "med")
            due_text = days_left_str(task.get("due_date"))
            print(f"{i}. [{status}] ({prio_label}) {task['title']}{due_text}")

    def _handle_add_task(self):
        """Handle adding a new task."""
        title = input("Task description: ").strip()
        prio_text = (
            input("Priority (1=low, 2=med, 3=high, default 2): ").strip()
        )
        priority = (
            int(prio_text)
            if prio_text.isdigit() and int(prio_text) in (1, 2, 3)
            else 2
        )
        due_input = input("Due date (DD.MM.RRRR, optional): ").strip()
        due_iso = parse_due_date(due_input) if due_input else None
        self.tasks = add_task(self.tasks, title, priority, due_iso)
        
        print(f"Added task: {title}")

    def _handle_toggle_task(self):
        """Handle toggling a task's done status."""
        self.display_tasks()
        idx = int(input("Enter task number: ")) - 1
        self.tasks = toggle_task(self.tasks, idx)

    def _handle_change_priority(self):
        """Handle changing a task's priority."""
        self.display_tasks()
        idx = int(input("Enter task number: ")) - 1
        new_prio = int(input("New priority (1-3): "))
        self.tasks = change_priority(self.tasks, idx, new_prio)

    def _handle_set_due_date(self):
        """Handle setting a task's due date."""
        self.display_tasks()
        idx = int(input("Enter task number: ")) - 1
        due_input = input(
            "New due date (DD.MM.RRRR, empty to clear): "
        ).strip()
        due_iso = parse_due_date(due_input) if due_input else None
        self.tasks = set_due_date(self.tasks, idx, due_iso)

    def run(self):
        """Main console loop."""
        commands = {
            "1": lambda: self.display_tasks(),
            "2": lambda: self._handle_add_task(),
            "3": lambda: self._handle_toggle_task(),
            "4": lambda: self._handle_change_priority(),
            "5": lambda: self._handle_set_due_date(),
            "6": lambda: save_tasks(self.tasks),
            "7": lambda: setattr(self, "tasks", load_tasks()),
            "8": lambda: self.display_tasks(
                filter_tasks(self.tasks, filter_done=True)
            ),
            "9": lambda: self.display_tasks(
                filter_tasks(self.tasks, filter_done=False)
            ),
            "10": lambda: self.display_tasks(
                filter_tasks(self.tasks, min_priority=3)
            ),
            "11": lambda: self._sort_and_display("priority"),
            "12": lambda: self._sort_and_display("due_date", False),
            "13": lambda: self._sort_and_display("title", False),
        }

        while True:
            self._show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "0":
                save_tasks(self.tasks)
                print("Goodbye.")
                break
            elif choice in commands:
                try:
                    commands[choice]()
                except (ValueError, IndexError) as e:
                    print(f"Invalid input: {e}")
            else:
                print("Unknown option, try again.")

    def _show_menu(self):
        """Display the main menu."""
        menu_items = [
            "1) Show all tasks",
            "2) Add task",
            "3) Toggle done/undone",
            "4) Change task priority",
            "5) Set/change task due date",
            "6) Save tasks",
            "7) Load tasks",
            "8) Show only done tasks",
            "9) Show only not-done tasks",
            "10) Show only high-priority tasks",
            "11) Sort tasks by priority",
            "12) Sort tasks by due date",
            "13) Sort tasks by title",
            "0) Quit",
        ]
        print("\n=== Todo List ===")
        for item in menu_items:
            print(item)

    def _sort_and_display(self, by, reverse=True):
        """Sort tasks and display them."""
        self.tasks = sort_tasks(self.tasks, by=by, reverse=reverse)
        self.display_tasks()




def main():
    # Arg-based CLI (non-interactive) for tests and quick commands
    args = sys.argv[1:]
    tasks = load_tasks()

    if not args:
        print("Usage: console_app.py [add <title>|list|delete <index>|complete <index>]")
        return 0

    cmd = args[0]

    if cmd == "add":
        if len(args) < 2:
            print("Error: missing task title")
            return 1
        title = args[1]
        tasks = add_task(tasks, title)  # default priority, no due date
        save_tasks(tasks)
        print(f"Added task: {title}")
        return 0

    elif cmd == "list":
        if not tasks:
            print("No tasks yet.")
            return 0
        for i, t in enumerate(tasks):
            status = "✓" if t["done"] else " "
            prio = t.get("priority", 2)
            print(f"{i}. [{status}] {t['title']} (prio {prio})")
        return 0

    elif cmd == "complete":
        if len(args) < 2:
            print("Error: missing task index")
            return 1
        idx = int(args[1])
        tasks = toggle_task(tasks, idx)
        save_tasks(tasks)
        print(f"Completed task {idx}: {tasks[idx]['title']}")
        return 0

    elif cmd == "delete":
        if len(args) < 2:
            print("Error: missing task index")
            return 1
        idx = int(args[1])
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"Deleted task {idx}: {removed['title']}")
            return 0
        else:
            print("Invalid index")
            return 1

    else:
        print("Unknown command")
        return 1


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # uruchom tryb argumentów (add/list/complete/delete)
        sys.exit(main())
    else:
        print("Usage: console_app.py [add|list|delete|complete]")
