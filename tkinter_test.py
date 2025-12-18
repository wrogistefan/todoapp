import tkinter as tk

def say_hello():
    print("Cześć, Łukasz!")

root = tk.Tk()
root.title("Moja pierwsza aplikacja")

label = tk.Label(root, text="Witaj w Tkinterze!")
label.pack()

button = tk.Button(root, text="Kliknij mnie", command=say_hello)
button.pack()

root.mainloop()
