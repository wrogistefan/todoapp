from tasks import (
    filter_tasks,
    add_task,
    toggle_task,
    change_priority,
    set_due_date,
    sort_tasks,
    days_left_str,
)
from storage import save_tasks, load_tasks

def display_tasks(tasks):
    """Pomocnicza funkcja do wypisywania zadań w konsoli."""
    if not tasks:
        print("No tasks yet.")
        return
    print("\nYour tasks:")
    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        prio_map = {1: "low", 2: "med", 3: "high"}
        prio_label = prio_map.get(task.get("priority", 2), "med")
        due_text = days_left_str(task.get("due_date"))
        print(f"{index}. [{status}] ({prio_label}) {task['title']}{due_text}")


def run_menu(tasks):
    while True:
        print("\n=== Todo List ===")
        print("1) Show all tasks")
        print("2) Add task")
        print("3) Toggle done/undone")
        print("4) Change task priority")
        print("5) Set/change task due date")
        print("6) Save tasks")
        print("7) Load tasks")
        print("8) Show only done tasks")
        print("9) Show only not-done tasks")
        print("10) Show only high-priority tasks")
        print("11) Sort tasks by priority")
        print("12) Sort tasks by due date")
        print("13) Sort tasks by title")
        print("0) Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            title = input("Task description: ").strip()
            prio_text = input("Priority (1=low, 2=med, 3=high, default 2): ").strip()
            priority = int(prio_text) if prio_text.isdigit() and int(prio_text) in (1, 2, 3) else 2
            due_input = input("Due date (DD.MM.RRRR, optional): ").strip()
            from tasks import parse_due_date
            due_iso = parse_due_date(due_input) if due_input else None
            tasks = add_task(tasks, title, priority, due_iso)
        elif choice == "3":
            display_tasks(tasks)
            idx = int(input("Enter task number to toggle: ")) - 1
            tasks = toggle_task(tasks, idx)
        elif choice == "4":
            display_tasks(tasks)
            idx = int(input("Enter task number to change priority: ")) - 1
            new_prio = int(input("New priority (1=low, 2=med, 3=high): "))
            tasks = change_priority(tasks, idx, new_prio)
        elif choice == "5":
            display_tasks(tasks)
            idx = int(input("Enter task number to set/change due date: ")) - 1
            due_input = input("New due date (DD.MM.RRRR, empty to clear): ").strip()
            from tasks import parse_due_date
            due_iso = parse_due_date(due_input) if due_input else None
            tasks = set_due_date(tasks, idx, due_iso)
        elif choice == "6":
            save_tasks(tasks)
        elif choice == "7":
            tasks = load_tasks()
        elif choice == "8":
            display_tasks(filter_tasks(tasks, filter_done=True))
        elif choice == "9":
            display_tasks(filter_tasks(tasks, filter_done=False))
        elif choice == "10":
            display_tasks(filter_tasks(tasks, min_priority=3))
        elif choice == "11":
            tasks = sort_tasks(tasks, by="priority")
            display_tasks(tasks)
        elif choice == "12":
            tasks = sort_tasks(tasks, by="due_date", reverse=False)
            display_tasks(tasks)
        elif choice == "13":
            tasks = sort_tasks(tasks, by="title", reverse=False)
            display_tasks(tasks)
        elif choice == "0":
            save_tasks(tasks)
            print("Goodbye.")
            break
        else:
            print("Unknown option, try again.")

    return tasks
