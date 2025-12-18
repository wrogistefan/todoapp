import tkinter as tk
from console_app import ConsoleTodoApp
from gui import TodoApp

def main():
    print("=== Wybierz tryb uruchomienia ===")
    print("1) Konsola")
    print("2) GUI (Tkinter)")
    choice = input("Twój wybór: ").strip()

    if choice == "1":
        app = ConsoleTodoApp()
        app.run()
    elif choice == "2":
        root = tk.Tk()
        app = TodoApp(root)
        root.mainloop()
    else:
        print("Nieznana opcja. Uruchom ponownie i wybierz 1 lub 2.")

if __name__ == "__main__":
    main()
