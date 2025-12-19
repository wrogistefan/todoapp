import tkinter as tk

from console_app import ConsoleTodoApp
from gui import TodoApp


def main():
    print("=== Wybierz tryb uruchomienia ===")
    print("1) Konsola")
    print("2) GUI")
    try:
        choice = input("Twój wybór: ").strip()
    except EOFError:
        # fallback dla środowisk testowych bez stdin
        choice = "1"

    if choice == "1":
        from console_app import ConsoleTodoApp
        app = ConsoleTodoApp()
        try:
            app.run()
        except EOFError:
            # jeśli w testach brak stdin, zakończ spokojnie
            return
    elif choice == "2":
        from gui import TodoApp
        import tkinter as tk
        root = tk.Tk()
        app = TodoApp(root)
        root.mainloop()
    else:
        print("Nieznana opcja, domyślnie uruchamiam konsolę.")
        from console_app import ConsoleTodoApp
        app = ConsoleTodoApp()
        try:
            app.run()
        except EOFError:
            return


if __name__ == "__main__":
    main()
