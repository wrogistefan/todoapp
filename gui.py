import tkinter as tk
from tkinter import messagebox, simpledialog
from tasks import (
    add_task, toggle_task, change_priority, set_due_date,
    sort_tasks, filter_tasks, days_left_str, parse_due_date
)
from storage import save_tasks, load_tasks


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List (Tkinter)")
        self.tasks = load_tasks()

        # State for filters and sorting
        self.filter_done_var = tk.StringVar(value="all")  # all | done | not_done | high
        self.sort_by_var = tk.StringVar(value="none")     # none | priority | due_date | title

        # Layout using grid
        # Left: list
        self.listbox = tk.Listbox(root, width=65, height=18)
        self.listbox.grid(row=0, column=0, rowspan=8, padx=10, pady=10, sticky="nsw")

        # Right: form controls
        tk.Label(root, text="Opis zadania:").grid(row=0, column=1, sticky="w")
        self.title_entry = tk.Entry(root, width=32)
        self.title_entry.grid(row=1, column=1, sticky="we", padx=4, pady=2)

        tk.Label(root, text="Priorytet (1/2/3):").grid(row=2, column=1, sticky="w")
        self.priority_var = tk.IntVar(value=2)
        self.priority_menu = tk.OptionMenu(root, self.priority_var, 1, 2, 3)
        self.priority_menu.grid(row=3, column=1, sticky="w", padx=4)

        tk.Label(root, text="Termin (DD.MM.RRRR):").grid(row=4, column=1, sticky="w")
        self.due_entry = tk.Entry(root, width=20)
        self.due_entry.grid(row=5, column=1, sticky="we", padx=4, pady=2)

        # Action buttons (right panel)
        tk.Button(root, text="Dodaj zadanie", command=self.add_task_gui).grid(row=6, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Toggle done", command=self.toggle_task_gui).grid(row=7, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Zmień priorytet", command=self.change_priority_gui).grid(row=8, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Ustaw termin", command=self.set_due_date_gui).grid(row=9, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Wyczyść termin", command=self.clear_due_date_gui).grid(row=10, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Edytuj opis", command=self.edit_title_gui).grid(row=11, column=1, sticky="we", padx=4, pady=2)
        tk.Button(root, text="Usuń zadanie", command=self.delete_task_gui).grid(row=12, column=1, sticky="we", padx=4, pady=2)

        # Bottom: filters, sorting, persistence
        tk.Label(root, text="Filtr:").grid(row=13, column=0, sticky="w", padx=10)
        tk.OptionMenu(root, self.filter_done_var, "all", "done", "not_done", "high", command=lambda _: self.refresh_list()).grid(row=13, column=0, sticky="w", padx=60)

        tk.Label(root, text="Sortuj wg:").grid(row=13, column=1, sticky="w", padx=4)
        tk.OptionMenu(root, self.sort_by_var, "none", "priority", "due_date", "title", command=lambda _: self.apply_sort_and_refresh()).grid(row=13, column=1, sticky="e", padx=4)

        tk.Button(root, text="Zapisz", command=self.save_gui).grid(row=14, column=0, sticky="w", padx=10, pady=8)
        tk.Button(root, text="Wczytaj", command=self.load_gui).grid(row=14, column=1, sticky="e", padx=4, pady=8)

        # Configure columns to stretch nicely
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)

        self.refresh_list()

    # Core rendering logic
    def refresh_list(self, tasks_override=None):
        self.listbox.delete(0, tk.END)
        # Apply filter first
        tasks_to_render = tasks_override if tasks_override is not None else self.apply_filter(self.tasks)
        # Apply sort if needed (without mutating self.tasks unless explicitly requested)
        tasks_to_render = self.apply_sort(tasks_to_render)

        for idx, task in enumerate(tasks_to_render):
            status = "✓" if task["done"] else " "
            prio_map = {1: "low", 2: "med", 3: "high"}
            prio_label = prio_map.get(task.get("priority", 2), "med")
            due_text = days_left_str(task.get("due_date"))
            self.listbox.insert(tk.END, f"[{status}] ({prio_label}) {task['title']}{due_text}")

            # Color-coding per item index
            if task["done"]:
                self.listbox.itemconfig(idx, {'fg': 'green'})
            elif task.get("due_date") and "overdue" in due_text:
                self.listbox.itemconfig(idx, {'fg': 'orange'})
            elif task.get("priority") == 3:
                self.listbox.itemconfig(idx, {'fg': 'red'})

    def apply_filter(self, tasks):
        mode = self.filter_done_var.get()
        if mode == "all":
            return tasks
        if mode == "done":
            return filter_tasks(tasks, filter_done=True)
        if mode == "not_done":
            return filter_tasks(tasks, filter_done=False)
        if mode == "high":
            return filter_tasks(tasks, min_priority=3)
        return tasks

    def apply_sort(self, tasks):
        by = self.sort_by_var.get()
        if by == "none":
            return tasks
        reverse = True if by == "priority" else False
        return sort_tasks(tasks, by=by, reverse=reverse)

    def apply_sort_and_refresh(self):
        self.refresh_list()

    # Actions
    def add_task_gui(self):
        title = self.title_entry.get().strip()
        prio = self.priority_var.get()
        due_input = self.due_entry.get().strip()
        due_iso = parse_due_date(due_input) if due_input else None

        if not title:
            messagebox.showwarning("Błąd", "Opis zadania nie może być pusty.")
            return

        self.tasks = add_task(self.tasks, title, prio, due_iso)
        self.title_entry.delete(0, tk.END)
        self.refresh_list()
        save_tasks(self.tasks)

    def get_selected_index_global(self):
        """Map selected filtered/sorted index back to original self.tasks index."""
        sel = self.listbox.curselection()
        if not sel:
            return None
        # Build the currently rendered list to find mapping
        current_render = self.apply_sort(self.apply_filter(self.tasks))
        selected_task = current_render[sel[0]]
        # Find the matching task in self.tasks by identity
        for i, t in enumerate(self.tasks):
            if t is selected_task or (
                t["title"] == selected_task["title"]
                and t.get("priority") == selected_task.get("priority")
                and t.get("due_date") == selected_task.get("due_date")
                and t.get("done") == selected_task.get("done")
            ):
                return i
        return None

    def toggle_task_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        self.tasks = toggle_task(self.tasks, idx)
        self.refresh_list()
        save_tasks(self.tasks)

    def change_priority_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        new_prio = self.priority_var.get()
        self.tasks = change_priority(self.tasks, idx, new_prio)
        self.refresh_list()
        save_tasks(self.tasks)

    def set_due_date_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        due_input = self.due_entry.get().strip()
        due_iso = parse_due_date(due_input) if due_input else None
        self.tasks = set_due_date(self.tasks, idx, due_iso)
        self.refresh_list()
        save_tasks(self.tasks)

    def clear_due_date_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        self.tasks = set_due_date(self.tasks, idx, None)
        self.refresh_list()
        save_tasks(self.tasks)

    def edit_title_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        new_title = simpledialog.askstring("Edytuj opis", "Nowy opis zadania:", initialvalue=self.tasks[idx]["title"])
        if new_title is None:
            return
        new_title = new_title.strip()
        if not new_title:
            messagebox.showwarning("Błąd", "Opis nie może być pusty.")
            return
        self.tasks[idx]["title"] = new_title
        self.refresh_list()
        save_tasks(self.tasks)

    def delete_task_gui(self):
        idx = self.get_selected_index_global()
        if idx is None:
            messagebox.showinfo("Info", "Zaznacz zadanie na liście.")
            return
        if messagebox.askyesno("Potwierdź", "Na pewno usunąć zadanie?"):
            del self.tasks[idx]
            self.refresh_list()
            save_tasks(self.tasks)

    def save_gui(self):
        save_tasks(self.tasks)
        messagebox.showinfo("OK", "Zapisano zadania.")

    def load_gui(self):
        self.tasks = load_tasks()
        self.refresh_list()
        messagebox.showinfo("OK", "Wczytano zadania.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
