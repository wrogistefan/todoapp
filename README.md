# TodoApp (Python)

A simple task management application written in Python.  
It supports two interfaces:
- **Console** (`ConsoleTodoApp`)
- **Graphical (GUI)** in Tkinter (`TodoApp`)

## ✨ Features
- Add new tasks (title, priority, due date)
- Mark tasks as done/undone
- Change priority
- Set and clear due date
- Edit task title
- Delete tasks
- Filter (done, not done, high-priority)
- Sort (priority, due date, title)
- Save and load tasks from JSON file

## 🚀 How to run
1. Make sure you have **Python 3.11+** installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/wrogistefan/todoapp.git
   cd todoapp

todoapp/
├── tasks.py        # core logic
├── storage.py      # JSON save/load
├── console_app.py  # console interface (class-based)
├── gui.py          # Tkinter GUI interface
├── main.py         # entry point
└── README.md       # project description
