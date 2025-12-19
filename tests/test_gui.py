import os
import pytest
import tkinter as tk

def test_gui_init():
    # Skip test if no display is available (e.g. CI/CD pipelines)
    if os.environ.get("DISPLAY", "") == "":
        pytest.skip("No display available for Tkinter GUI")

    root = tk.Tk()
    root.destroy()
