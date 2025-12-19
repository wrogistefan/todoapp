import tkinter as tk
from gui import TodoApp

def test_gui_init():
    root = tk.Tk()
    app = TodoApp(root)
    assert isinstance(app, TodoApp)
    root.destroy()
